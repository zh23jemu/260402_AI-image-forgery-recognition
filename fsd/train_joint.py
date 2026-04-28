# -*- coding: utf-8 -*-
"""
联合训练入口。

当前版本同时支持两种阶段：

1. 第一阶段：`FSD + Stay-Positive`
2. 第二阶段最小量化版：`FSD + Stay-Positive + LVLM`

其中第二阶段并不让 LVLM 端到端参与训练，而是把已经整理好的
结构化语义标签当作离线监督信号，通过轻量辅助头完成多标签训练。
"""

import os
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange
from torch.amp import autocast, GradScaler
from torchmetrics.classification import Accuracy, AveragePrecision, MultilabelF1Score
from tqdm import tqdm
import timm

from datasets import setup_val_dataloader
from datasets.joint_metadata import LVLM_LABEL_FIELDS, JointMetadataIndex, setup_joint_infinity_train_dataloader
from model.prototypical_utils import compute_prototypical_loss
from util.parser import TrainParser
from util.utils import load_model, save_model, setup_dist
import util.logger as logger


def parse_generator_list(value):
    """把逗号分隔的类别字符串解析成列表。"""

    return [item.strip() for item in value.split(",") if item.strip()]


def resolve_data_root(data_root):
    """
    解析数据根目录。

    保留与原始 `train.py` 一致的查找策略，避免因为不同工作目录
    导致脚本找不到 `data/GenImage`。
    """

    if os.path.isabs(data_root) and os.path.exists(data_root):
        return data_root

    candidates = [
        os.path.abspath(data_root),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", data_root)),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "GenImage")),
    ]

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return os.path.abspath(data_root)


def resolve_optional_path(path_value):
    """解析可选路径参数，例如 checkpoint 或 metadata CSV。"""

    if not path_value:
        return ""

    if os.path.isabs(path_value) and os.path.exists(path_value):
        return path_value

    candidates = [
        os.path.abspath(path_value),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", path_value)),
    ]

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return os.path.abspath(path_value)


class JointFSDModel(nn.Module):
    """
    联合训练模型封装。

    设计思路：

    1. 保留 `FSD` 原主干输出 1024 维表征，继续服务 prototypical 主任务
    2. 新增一个非常轻量的 `LVLM` 多标签辅助头
    3. 不改变主干 few-shot 训练逻辑，只在 feature 上额外挂一个语义预测分支
    """

    def __init__(self, backbone_name="resnet50", pretrained=False, feature_dim=1024, lvlm_label_dim=5):
        super().__init__()
        self.backbone = timm.create_model(backbone_name, pretrained=pretrained, num_classes=feature_dim)
        self.lvlm_head = nn.Sequential(
            nn.LayerNorm(feature_dim),
            nn.Linear(feature_dim, lvlm_label_dim),
        )
        self.feature_dim = feature_dim
        self.lvlm_label_dim = lvlm_label_dim

    def forward(self, x):
        """同时输出主任务特征和 LVLM 辅助头 logits。"""

        features = self.backbone(x)
        lvlm_logits = self.lvlm_head(features)
        return features, lvlm_logits


def build_parser():
    """
    在原始 `TrainParser` 基础上扩展联合训练专用参数。

    这样可以最大程度复用当前 FSD 的训练参数和运行方式。
    """

    parser = TrainParser().parser
    parser.add_argument(
        "--train_generators",
        type=str,
        default="real,ADM,SD,Midjourney",
        help="参与联合训练的类别列表，逗号分隔。",
    )
    parser.add_argument(
        "--real_class_name",
        type=str,
        default="real",
        help="主任务中的真实图像类别名称。",
    )
    parser.add_argument(
        "--metadata_csv",
        type=str,
        default="",
        help="联合训练元数据 CSV 路径，可包含 Stay-Positive 分数、LVLM 标签和 hard_weight。",
    )
    parser.add_argument(
        "--sp_loss_weight",
        type=float,
        default=0.3,
        help="Stay-Positive 辅助监督损失权重。",
    )
    parser.add_argument(
        "--sp_loss_type",
        type=str,
        default="mse",
        choices=["mse", "bce"],
        help="Stay-Positive 辅助监督损失类型。",
    )
    parser.add_argument(
        "--force_real_in_task",
        type=TrainParser._str2bool,
        default=True,
        help="是否强制每个 episodic task 都包含 real 类别。",
    )
    parser.add_argument(
        "--eval_generators",
        type=str,
        default="",
        help="评估时使用的 fake 类别列表；为空时沿用 train_generators 中的 fake 类别。",
    )
    parser.add_argument(
        "--enable_lvlm_head",
        type=TrainParser._str2bool,
        default=False,
        help="是否启用第二阶段 LVLM 轻量辅助头。",
    )
    parser.add_argument(
        "--lvlm_loss_weight",
        type=float,
        default=0.2,
        help="LVLM 结构化语义辅助损失权重。",
    )
    parser.add_argument(
        "--lvlm_loss_on_fake_only",
        type=TrainParser._str2bool,
        default=True,
        help="是否只在 fake query 样本上计算 LVLM 语义辅助损失。",
    )
    return parser


def compute_sp_loss(
    scores,
    query_sp_probs,
    query_sp_valids,
    query_hard_weights,
    labels,
    real_class_index,
    loss_type,
):
    """
    计算 `Stay-Positive` 辅助损失。

    设计逻辑如下：

    1. 原始 `FSD` 输出的是多类原型判别分数
    2. 这里把“是否为 fake”重新解释为一个二分类概率
    3. 通过 `p_fake = 1 - p_real` 构造 fake 概率
    4. 再用离线 `Stay-Positive` 概率去约束这个 fake 概率
    """

    probs = scores.softmax(dim=-1)
    p_real = probs[:, real_class_index]
    p_fake = 1.0 - p_real

    flat_sp_probs = rearrange(query_sp_probs, "b q n -> (b q n)")
    flat_sp_valids = rearrange(query_sp_valids, "b q n -> (b q n)")
    flat_hard_weights = rearrange(query_hard_weights, "b q n -> (b q n)")

    fake_targets = (labels != real_class_index).float()
    valid_mask = (flat_sp_valids > 0.5) & (fake_targets > 0.5)

    if not torch.any(valid_mask):
        zero = torch.zeros((), device=scores.device, dtype=scores.dtype)
        return zero, 0

    pred = torch.clamp(p_fake[valid_mask], min=1e-6, max=1.0 - 1e-6)
    target = torch.clamp(flat_sp_probs[valid_mask], min=0.0, max=1.0)
    weights = torch.clamp(flat_hard_weights[valid_mask], min=1.0)

    if loss_type == "bce":
        per_sample = F.binary_cross_entropy(pred, target, reduction="none")
    else:
        per_sample = (pred - target) ** 2

    weighted_loss = (per_sample * weights).sum() / weights.sum().clamp_min(1.0)
    return weighted_loss, int(valid_mask.sum().item())


def compute_lvlm_loss(
    lvlm_logits,
    query_lvlm_labels,
    query_lvlm_valids,
    query_lvlm_confidences,
    query_hard_weights,
    labels,
    real_class_index,
    fake_only=True,
):
    """
    计算第二阶段最小量化版的 LVLM 多标签辅助损失。

    关键点：

    1. 只把已经结构化好的离线标签当作监督来源
    2. 默认仅在 fake query 样本上计算
    3. 用 `hard_weight * lvlm_confidence` 做轻量加权
    """

    flat_logits = rearrange(lvlm_logits, "b q n c -> (b q n) c")
    flat_labels = rearrange(query_lvlm_labels, "b q n c -> (b q n) c")
    flat_valids = rearrange(query_lvlm_valids, "b q n -> (b q n)")
    flat_confidences = rearrange(query_lvlm_confidences, "b q n -> (b q n)")
    flat_hard_weights = rearrange(query_hard_weights, "b q n -> (b q n)")

    valid_mask = flat_valids > 0.5
    if fake_only:
        valid_mask = valid_mask & (labels != real_class_index)

    if not torch.any(valid_mask):
        zero = torch.zeros((), device=lvlm_logits.device, dtype=lvlm_logits.dtype)
        return zero, 0

    selected_logits = flat_logits[valid_mask]
    selected_labels = flat_labels[valid_mask]
    selected_confidences = torch.clamp(flat_confidences[valid_mask], min=0.2, max=1.0)
    selected_weights = torch.clamp(flat_hard_weights[valid_mask], min=1.0) * selected_confidences

    per_sample = F.binary_cross_entropy_with_logits(
        selected_logits,
        selected_labels,
        reduction="none",
    ).mean(dim=-1)
    weighted_loss = (per_sample * selected_weights).sum() / selected_weights.sum().clamp_min(1.0)
    return weighted_loss, int(valid_mask.sum().item())


def build_query_views(batch_tensor, current_num_classes, batch_size, label_dim=None):
    """
    把按类打包的 batch tensor 重排成 query 可对齐形状。

    对于标量字段，输出形状为：
    - `(batch_size, task_size, num_class)`

    对于多标签字段，输出形状为：
    - `(batch_size, task_size, num_class, label_dim)`
    """

    if label_dim is None:
        return rearrange(batch_tensor, "n (b t) -> b t n", n=current_num_classes, b=batch_size)
    return rearrange(batch_tensor, "n (b t) c -> b t n c", n=current_num_classes, b=batch_size, c=label_dim)


def evaluate_joint_model(model, val_dataloaders, eval_generators, args):
    """
    评估主任务指标；如果启用 LVLM 辅助头，则同步输出语义头 F1。

    说明：
    - 主任务仍然按原先闭集二分类协议输出 `accuracy / AP`
    - 语义头指标只在存在标签的 fake query 上统计
    """

    acc_calculator = Accuracy(task="multiclass", num_classes=2)
    ap_calculator = AveragePrecision(task="multiclass", num_classes=2, thresholds=10)
    lvlm_f1_calculator = MultilabelF1Score(num_labels=len(LVLM_LABEL_FIELDS), threshold=0.5)

    with torch.no_grad():
        for fake_folder in eval_generators:
            prob_list = []
            label_list = []
            lvlm_pred_list = []
            lvlm_target_list = []

            iterator = zip(val_dataloaders[args.real_class_name], val_dataloaders[fake_folder])

            for real_batch, fake_batch in tqdm(iterator):
                real_images = real_batch[0]
                fake_images = fake_batch[0]

                batch_data = torch.stack([real_images, fake_images], dim=0).to(args.device)
                batch_data = rearrange(batch_data, "n b c h w -> (n b) c h w")
                labels = torch.arange(0, 2, device=args.device).repeat(args.num_query_val)

                with autocast(enabled=args.use_fp16, device_type="cuda"):
                    features, lvlm_logits = model(batch_data)

                features = rearrange(features, "(n b) l -> 1 b n l", n=2)
                _, scores = compute_prototypical_loss(features, labels, args.num_support_val)

                prob_list.append(scores.softmax(dim=-1))
                label_list.append(labels)

                if args.enable_lvlm_head:
                    fake_lvlm_labels = fake_batch[6][args.num_support_val :, :]
                    fake_lvlm_valids = fake_batch[7][args.num_support_val :]

                    fake_query_logits = lvlm_logits[real_images.shape[0] + args.num_support_val :]
                    valid_mask = fake_lvlm_valids > 0.5
                    if torch.any(valid_mask):
                        lvlm_pred_list.append(torch.sigmoid(fake_query_logits[valid_mask]).cpu())
                        lvlm_target_list.append(fake_lvlm_labels[valid_mask].cpu())

            probs = torch.cat(prob_list, dim=0)
            labels = torch.cat(label_list, dim=0)

            acc = acc_calculator(probs.cpu(), labels.cpu()).item()
            ap = ap_calculator(probs.cpu(), labels.cpu()).item()

            if args.enable_lvlm_head and lvlm_pred_list:
                lvlm_preds = torch.cat(lvlm_pred_list, dim=0)
                lvlm_targets = torch.cat(lvlm_target_list, dim=0)
                lvlm_f1 = lvlm_f1_calculator(lvlm_preds, lvlm_targets.int()).item()
                logger.info(
                    "Evaluation on %s done. accuracy: %.6f, average precision: %.6f, lvlm_f1: %.6f.",
                    fake_folder,
                    acc,
                    ap,
                    lvlm_f1,
                )
            else:
                logger.info(
                    "Evaluation on %s done. accuracy: %.6f, average precision: %.6f.",
                    fake_folder,
                    acc,
                    ap,
                )


def main():
    args = build_parser().parse_args()
    setup_dist(args)
    args.data_root = resolve_data_root(args.data_root)
    args.init_ckpt_path = resolve_optional_path(args.init_ckpt_path)
    args.metadata_csv = resolve_optional_path(args.metadata_csv)

    logger.setup(log_dir=args.output_dir, device=args.device)

    train_generators = parse_generator_list(args.train_generators)
    if args.real_class_name not in train_generators:
        train_generators = [args.real_class_name] + train_generators

    fake_generators = [name for name in train_generators if name != args.real_class_name]
    eval_generators = parse_generator_list(args.eval_generators) if args.eval_generators else list(fake_generators)

    logger.info("Creating joint training data loader...")
    logger.info(f"Resolved data root: {args.data_root}")
    logger.info(f"Train generators: {train_generators}")
    logger.info(f"Eval generators: {eval_generators}")
    logger.info(f"Metadata CSV: {args.metadata_csv if args.metadata_csv else 'None'}")
    logger.info(f"SP loss weight: {args.sp_loss_weight}")
    logger.info(f"SP loss type: {args.sp_loss_type}")
    logger.info(f"Force real in task: {args.force_real_in_task}")
    logger.info(f"Enable LVLM head: {args.enable_lvlm_head}")
    logger.info(f"LVLM loss weight: {args.lvlm_loss_weight}")
    logger.info(f"LVLM label dim: {len(LVLM_LABEL_FIELDS)}")

    metadata_index = JointMetadataIndex(args.metadata_csv) if args.metadata_csv else None
    if metadata_index is not None:
        logger.info(f"Loaded joint metadata rows: {metadata_index.row_count}")
    else:
        logger.info("Joint metadata is disabled for this run.")

    train_iters = {
        folder: setup_joint_infinity_train_dataloader(
            folder_path=os.path.join(args.data_root, folder, "train"),
            metadata_index=metadata_index,
            batch_size=(args.num_support_train + args.num_query_train) * args.batch_size,
            num_workers=args.num_workers,
        )
        for folder in train_generators
    }

    val_dataloaders = {
        folder: setup_val_dataloader(
            folder_path=os.path.join(args.data_root, folder, "val"),
            batch_size=args.num_support_val + args.num_query_val,
            num_workers=args.num_workers,
        )
        for folder in [args.real_class_name] + eval_generators
    }

    logger.info("Creating joint model 'resnet50'...")
    logger.info(f"Use pretrained backbone: {args.pretrained_backbone}")
    model = JointFSDModel(
        backbone_name="resnet50",
        pretrained=args.pretrained_backbone,
        feature_dim=1024,
        lvlm_label_dim=len(LVLM_LABEL_FIELDS),
    )

    if args.init_ckpt_path:
        logger.info(f"Initializing model weights from checkpoint: {args.init_ckpt_path}")
        try:
            load_model(args.init_ckpt_path, model=model.backbone)
        except Exception:
            # 兼容历史 checkpoint 键名不完全匹配的情况。
            load_model(args.init_ckpt_path, model=model)

    print(model)
    model = model.to(args.device)

    logger.info("Creating optimizer and scheduler...")
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    print(optimizer)

    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer=optimizer,
        gamma=args.lr_scheduler_gamma,
        step_size=args.lr_scheduler_step,
    )
    print(scheduler)

    logger.info("Start joint training for %d steps.", args.total_training_steps)
    scaler = GradScaler(enabled=args.use_fp16)
    effective_step = 0
    steps_with_valid_sp = 0
    steps_with_valid_lvlm = 0
    running_valid_sp_total = 0
    running_valid_lvlm_total = 0

    for step in range(1, args.total_training_steps + 1):
        model.train()
        optimizer.zero_grad()

        if args.force_real_in_task and fake_generators:
            sampled_fake_num = max(0, args.num_class_train - 1)
            sampled_fake_num = min(sampled_fake_num, len(fake_generators))
            selected_classes = [args.real_class_name] + random.sample(fake_generators, sampled_fake_num)
        else:
            selected_classes = random.sample(train_generators, min(args.num_class_train, len(train_generators)))

        if len(selected_classes) < min(args.num_class_train, len(train_generators)):
            remaining = [name for name in train_generators if name not in selected_classes]
            need = min(args.num_class_train, len(train_generators)) - len(selected_classes)
            selected_classes.extend(remaining[:need])

        real_class_index = selected_classes.index(args.real_class_name) if args.real_class_name in selected_classes else 0
        current_num_classes = len(selected_classes)

        class_batches = [next(train_iters[class_name]) for class_name in selected_classes]

        batch_images = torch.stack([batch[0] for batch in class_batches], dim=0).to(args.device)
        batch_sp_probs = torch.stack([batch[3] for batch in class_batches], dim=0).to(args.device)
        batch_sp_valids = torch.stack([batch[4] for batch in class_batches], dim=0).to(args.device)
        batch_hard_weights = torch.stack([batch[5] for batch in class_batches], dim=0).to(args.device)
        batch_lvlm_labels = torch.stack([batch[6] for batch in class_batches], dim=0).to(args.device)
        batch_lvlm_valids = torch.stack([batch[7] for batch in class_batches], dim=0).to(args.device)
        batch_lvlm_confidences = torch.stack([batch[8] for batch in class_batches], dim=0).to(args.device)

        labels = torch.arange(0, current_num_classes, device=args.device).repeat(
            args.batch_size * args.num_query_train
        )

        batch_images = rearrange(batch_images, "n b c h w -> (n b) c h w")

        with autocast(enabled=args.use_fp16, device_type="cuda"):
            features, lvlm_logits = model(batch_images)

        outputs = rearrange(
            features,
            "(n b t) l -> b t n l",
            n=current_num_classes,
            b=args.batch_size,
        )
        lvlm_logits_view = rearrange(
            lvlm_logits,
            "(n b t) c -> b t n c",
            n=current_num_classes,
            b=args.batch_size,
        )

        proto_loss, scores = compute_prototypical_loss(outputs, labels, args.num_support_train)

        sp_prob_view = build_query_views(batch_sp_probs, current_num_classes, args.batch_size)
        sp_valid_view = build_query_views(batch_sp_valids, current_num_classes, args.batch_size)
        hard_weight_view = build_query_views(batch_hard_weights, current_num_classes, args.batch_size)
        lvlm_label_view = build_query_views(
            batch_lvlm_labels,
            current_num_classes,
            args.batch_size,
            label_dim=len(LVLM_LABEL_FIELDS),
        )
        lvlm_valid_view = build_query_views(batch_lvlm_valids, current_num_classes, args.batch_size)
        lvlm_confidence_view = build_query_views(batch_lvlm_confidences, current_num_classes, args.batch_size)

        query_sp_probs = sp_prob_view[:, args.num_support_train :, :]
        query_sp_valids = sp_valid_view[:, args.num_support_train :, :]
        query_hard_weights = hard_weight_view[:, args.num_support_train :, :]
        query_lvlm_labels = lvlm_label_view[:, args.num_support_train :, :, :]
        query_lvlm_valids = lvlm_valid_view[:, args.num_support_train :, :]
        query_lvlm_confidences = lvlm_confidence_view[:, args.num_support_train :, :]
        query_lvlm_logits = lvlm_logits_view[:, args.num_support_train :, :, :]

        sp_loss, valid_sp_count = compute_sp_loss(
            scores=scores,
            query_sp_probs=query_sp_probs,
            query_sp_valids=query_sp_valids,
            query_hard_weights=query_hard_weights,
            labels=labels,
            real_class_index=real_class_index,
            loss_type=args.sp_loss_type,
        )

        if args.enable_lvlm_head:
            lvlm_loss, valid_lvlm_count = compute_lvlm_loss(
                lvlm_logits=query_lvlm_logits,
                query_lvlm_labels=query_lvlm_labels,
                query_lvlm_valids=query_lvlm_valids,
                query_lvlm_confidences=query_lvlm_confidences,
                query_hard_weights=query_hard_weights,
                labels=labels,
                real_class_index=real_class_index,
                fake_only=args.lvlm_loss_on_fake_only,
            )
        else:
            lvlm_loss = torch.zeros((), device=args.device, dtype=proto_loss.dtype)
            valid_lvlm_count = 0

        total_loss = proto_loss + args.sp_loss_weight * sp_loss + args.lvlm_loss_weight * lvlm_loss

        if valid_sp_count > 0:
            steps_with_valid_sp += 1
        if valid_lvlm_count > 0:
            steps_with_valid_lvlm += 1
        running_valid_sp_total += valid_sp_count
        running_valid_lvlm_total += valid_lvlm_count

        logger.logkv_mean("proto_loss", proto_loss.item())
        logger.logkv_mean("sp_loss", sp_loss.item())
        logger.logkv_mean("lvlm_loss", lvlm_loss.item())
        logger.logkv_mean("total_loss", total_loss.item())
        logger.logkv_mean("valid_sp_samples", valid_sp_count)
        logger.logkv_mean("valid_lvlm_samples", valid_lvlm_count)

        scaler.scale(total_loss / args.accumulation_steps).backward()

        if step % args.accumulation_steps == 0:
            effective_step += 1

            scaler.unscale_(optimizer)
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad()

            if scheduler is not None:
                scheduler.step()

        if step % args.log_interval == 0:
            logger.logkv("step", step)
            logger.logkv("effective_step", effective_step)
            logger.logkv("lr", scheduler.get_last_lr()[0] if scheduler is not None else args.lr)
            logger.logkv("steps_with_valid_sp", steps_with_valid_sp)
            logger.logkv("steps_with_valid_lvlm", steps_with_valid_lvlm)
            logger.logkv("avg_valid_sp_samples_per_step", running_valid_sp_total / max(step, 1))
            logger.logkv("avg_valid_lvlm_samples_per_step", running_valid_lvlm_total / max(step, 1))
            logger.dumpkvs()

            logger.info(
                "Joint debug step=%d proto_loss=%.6f sp_loss=%.6f lvlm_loss=%.6f total_loss=%.6f valid_sp_samples=%d valid_lvlm_samples=%d steps_with_valid_sp=%d steps_with_valid_lvlm=%d avg_valid_sp_samples_per_step=%.4f avg_valid_lvlm_samples_per_step=%.4f",
                step,
                proto_loss.item(),
                sp_loss.item(),
                lvlm_loss.item(),
                total_loss.item(),
                valid_sp_count,
                valid_lvlm_count,
                steps_with_valid_sp,
                steps_with_valid_lvlm,
                running_valid_sp_total / max(step, 1),
                running_valid_lvlm_total / max(step, 1),
            )

        if step % args.save_interval == 0:
            logger.info("Save checkpoint at step: %d", step)

            kwargs = {
                "step": step,
                "effective_step": effective_step,
                "model": model,
                "optimizer": optimizer,
                "scheduler": scheduler,
                "scaler": scaler,
                "args": args,
            }
            save_model(os.path.join(args.output_dir, "ckpt"), args.model, **kwargs)
            torch.cuda.empty_cache()

        if step % args.eval_interval == 0:
            logger.info("Evaluating at step: %d", step)
            model.eval()
            evaluate_joint_model(model, val_dataloaders, eval_generators, args)


if __name__ == "__main__":
    main()
