# -*- coding: utf-8 -*-
"""
联合训练第一版入口。

当前版本的目标非常明确：

1. 继续使用 `FSD` 作为主干 backbone
2. 在训练阶段接入 `Stay-Positive` 的离线分数监督
3. 先完成 `FSD + SP` 的最小闭环
4. 暂时不把 `LVLM` 作为在线主干训练，而是为第二阶段留接口

这份脚本不是最终完整版三模型系统，而是当前最值得优先落地的第一版。
"""

import os
import random

import torch
import torch.nn.functional as F
from einops import rearrange
from torch.amp import autocast, GradScaler
from torchmetrics.classification import Accuracy, AveragePrecision
from tqdm import tqdm
import timm

from datasets import setup_val_dataloader
from datasets.joint_metadata import JointMetadataIndex, setup_joint_infinity_train_dataloader
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

    保留与原始 `train.py` 一致的查找策略，避免用户因为不同工作目录
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
        help="参与第一版联合训练的类别列表，逗号分隔。",
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
        help="联合训练元数据 CSV 路径，可包含 Stay-Positive 分数和 hard_weight。",
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

    1. 原始 `FSD` 在 episodic task 中输出的是多类原型距离分数
    2. 这里把“是否为 fake”重新解释为一个二分类问题
    3. 通过 `p_fake = 1 - p_real` 构造 fake 概率
    4. 再用离线 `Stay-Positive` 分数去约束这个 fake 概率

    这能在不彻底重写 `FSD` 任务结构的前提下，把 `SP` 的监督接进来。
    """

    probs = scores.softmax(dim=-1)
    p_real = probs[:, real_class_index]
    p_fake = 1.0 - p_real

    flat_sp_probs = rearrange(query_sp_probs, "b q n -> (b q n)")
    flat_sp_valids = rearrange(query_sp_valids, "b q n -> (b q n)")
    flat_hard_weights = rearrange(query_hard_weights, "b q n -> (b q n)")

    # 当前第一版主要希望 `SP` 约束 fake 样本，因此只在：
    # 1. 存在有效离线分数
    # 2. 当前 query 属于 fake 类
    # 这两种条件同时满足时施加损失。
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

    metadata_index = JointMetadataIndex(args.metadata_csv) if args.metadata_csv else None
    if metadata_index is not None:
        logger.info(f"Loaded joint metadata rows: {metadata_index.row_count}")

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
    model = timm.create_model("resnet50", pretrained=args.pretrained_backbone, num_classes=1024)

    if args.init_ckpt_path:
        logger.info(f"Initializing model weights from checkpoint: {args.init_ckpt_path}")
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

    for step in range(1, args.total_training_steps + 1):
        model.train()
        optimizer.zero_grad()

        if args.force_real_in_task and fake_generators:
            sampled_fake_num = max(0, args.num_class_train - 1)
            sampled_fake_num = min(sampled_fake_num, len(fake_generators))
            selected_classes = [args.real_class_name] + random.sample(fake_generators, sampled_fake_num)
        else:
            selected_classes = random.sample(train_generators, min(args.num_class_train, len(train_generators)))

        # 如果某些极端参数下抽样类别数量不足，继续补齐到当前可用类别上限。
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

        labels = torch.arange(0, current_num_classes, device=args.device).repeat(
            args.batch_size * args.num_query_train
        )

        batch_images = rearrange(batch_images, "n b c h w -> (n b) c h w")

        with autocast(enabled=args.use_fp16, device_type="cuda"):
            outputs = model(batch_images)

        outputs = rearrange(
            outputs,
            "(n b t) l -> b t n l",
            n=current_num_classes,
            b=args.batch_size,
        )

        proto_loss, scores = compute_prototypical_loss(outputs, labels, args.num_support_train)

        sp_prob_view = rearrange(batch_sp_probs, "n (b t) -> b t n", b=args.batch_size)
        sp_valid_view = rearrange(batch_sp_valids, "n (b t) -> b t n", b=args.batch_size)
        hard_weight_view = rearrange(batch_hard_weights, "n (b t) -> b t n", b=args.batch_size)

        query_sp_probs = sp_prob_view[:, args.num_support_train :, :]
        query_sp_valids = sp_valid_view[:, args.num_support_train :, :]
        query_hard_weights = hard_weight_view[:, args.num_support_train :, :]

        sp_loss, valid_sp_count = compute_sp_loss(
            scores=scores,
            query_sp_probs=query_sp_probs,
            query_sp_valids=query_sp_valids,
            query_hard_weights=query_hard_weights,
            labels=labels,
            real_class_index=real_class_index,
            loss_type=args.sp_loss_type,
        )

        total_loss = proto_loss + args.sp_loss_weight * sp_loss

        logger.logkv_mean("proto_loss", proto_loss.item())
        logger.logkv_mean("sp_loss", sp_loss.item())
        logger.logkv_mean("total_loss", total_loss.item())
        logger.logkv_mean("valid_sp_samples", valid_sp_count)

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
            logger.dumpkvs()

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

            acc_calculator = Accuracy(task="multiclass", num_classes=2)
            ap_calculator = AveragePrecision(task="multiclass", num_classes=2, thresholds=10)

            with torch.no_grad():
                for fake_folder in eval_generators:
                    prob_list = []
                    label_list = []
                    iterator = zip(val_dataloaders[args.real_class_name], val_dataloaders[fake_folder])

                    for (real_batch, _), (fake_batch, _) in tqdm(iterator):
                        batch_data = torch.stack([real_batch, fake_batch], dim=0).to(args.device)
                        batch_data = rearrange(batch_data, "n b c h w -> (n b) c h w")
                        labels = torch.arange(0, 2, device=args.device).repeat(args.num_query_val)

                        with autocast(enabled=args.use_fp16, device_type="cuda"):
                            outputs = model(batch_data)

                        outputs = rearrange(outputs, "(n b) l -> 1 b n l", n=2)
                        _, scores = compute_prototypical_loss(outputs, labels, args.num_support_val)

                        prob_list.append(scores.softmax(dim=-1))
                        label_list.append(labels)

                    probs = torch.cat(prob_list, dim=0)
                    labels = torch.cat(label_list, dim=0)

                    acc = acc_calculator(probs.cpu(), labels.cpu()).item()
                    ap = ap_calculator(probs.cpu(), labels.cpu()).item()
                    logger.info(
                        "Evaluation on %s done. accuracy: %.6f, average precision: %.6f.",
                        fake_folder,
                        acc,
                        ap,
                    )


if __name__ == "__main__":
    main()
