import csv
import math
import os
import warnings

from PIL import UnidentifiedImageError
from torch.utils.data import DataLoader, DistributedSampler
from torchvision import transforms
from torchvision.datasets import ImageFolder
import torch
import torch.distributed as dist


LVLM_LABEL_FIELDS = [
    "lvlm_has_text_artifact",
    "lvlm_has_layout_conflict",
    "lvlm_has_structure_error",
    "lvlm_has_bio_detail_error",
    "lvlm_has_patch_or_smooth",
]


def _normalize_path(path):
    """
    统一路径格式，尽量减少 Windows / Linux / 远端服务器之间的路径差异。

    这里不强行要求路径必须存在，因为很多分析 CSV 是在远端服务器导出的，
    当前本地环境下同一路径未必真实存在。我们只做：

    1. 统一分隔符为 `/`
    2. 去掉重复分隔符
    3. 去掉末尾分隔符
    4. 在 Windows 上做小写归一化，减少盘符大小写带来的不匹配
    """

    normalized = str(path).replace("\\", "/").strip()
    while "//" in normalized:
        normalized = normalized.replace("//", "/")
    normalized = normalized.rstrip("/")

    if os.name == "nt":
        normalized = normalized.lower()

    return normalized


def _suffix_key(path):
    """
    提取路径后缀键，用于跨机器路径映射。

    典型问题是：
    - 远端 CSV 中的路径形如 `/net/.../data/GenImage/...`
    - 本地路径形如 `C:/Coding/.../data/GenImage/...`

    只要 `data/GenImage/...` 之后的部分一致，就可以做匹配。
    如果找不到 `data/GenImage` 这段，就退化为使用最后 5 段路径。
    """

    normalized = _normalize_path(path)
    parts = normalized.split("/")
    lowered = [part.lower() for part in parts]

    for index in range(len(parts) - 1):
        if lowered[index] == "data" and lowered[index + 1] == "genimage":
            return "/".join(parts[index:])

    return "/".join(parts[-5:])


def _to_float(value, default=float("nan")):
    """把字符串安全转成浮点数；失败时返回默认值。"""

    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class JointMetadataIndex:
    """
    读取联合训练元数据 CSV，并提供样本路径到监督信息的查询能力。

    当前版本同时支持两类辅助监督：

    1. 第一阶段 `Stay-Positive` 概率监督
    2. 第二阶段 `LVLM` 多标签语义监督

    这样训练脚本可以在同一个 metadata 入口中完成：
    - `SP` 约束
    - `LVLM` 语义头训练
    - `hard_weight` 难样本加权
    """

    def __init__(self, csv_path=""):
        self.csv_path = csv_path
        self.rows_by_exact = {}
        self.rows_by_suffix = {}
        self.row_count = 0

        if csv_path:
            self._load(csv_path)

    def _load(self, csv_path):
        """从 CSV 构建精确路径索引和后缀路径索引。"""

        with open(csv_path, "r", encoding="utf-8", newline="") as file_obj:
            reader = csv.DictReader(file_obj)
            for row in reader:
                image_path = row.get("image_path") or row.get("filename")
                if not image_path:
                    continue

                normalized = _normalize_path(image_path)
                suffix = _suffix_key(image_path)

                sp_score_raw = _to_float(
                    row.get("sp_score_raw", row.get("stay_positive_score", row.get("sp_score")))
                )
                sp_prob_calibrated = _to_float(
                    row.get(
                        "sp_prob_calibrated",
                        row.get(
                            "stay_positive_prob_calibrated",
                            row.get("stay_positive_score", row.get("sp_score")),
                        ),
                    )
                )
                hard_weight = _to_float(row.get("hard_weight"), default=1.0)
                lvlm_confidence = _to_float(row.get("lvlm_confidence"), default=0.0)

                lvlm_values = []
                valid_label_count = 0
                for field_name in LVLM_LABEL_FIELDS:
                    label_value = _to_float(row.get(field_name), default=float("nan"))
                    if math.isnan(label_value):
                        lvlm_values.append(0.0)
                    else:
                        lvlm_values.append(float(label_value))
                        valid_label_count += 1

                parsed_row = {
                    "image_path": image_path,
                    "split": row.get("split", ""),
                    "generator": row.get("generator", ""),
                    "label": row.get("label", row.get("ground_truth", "")),
                    "sp_score_raw": sp_score_raw,
                    "sp_prob_calibrated": sp_prob_calibrated,
                    "hard_weight": hard_weight if not math.isnan(hard_weight) else 1.0,
                    "subset_tag": row.get("subset_tag", ""),
                    "sp_conflict_flag": row.get("sp_conflict_flag", ""),
                    "lvlm_labels": lvlm_values,
                    "lvlm_valid": 1.0 if valid_label_count > 0 else 0.0,
                    "lvlm_confidence": 0.0 if math.isnan(lvlm_confidence) else float(lvlm_confidence),
                }

                self.rows_by_exact[normalized] = parsed_row
                self.rows_by_suffix[suffix] = parsed_row
                self.row_count += 1

    def lookup(self, image_path):
        """
        根据样本路径查找联合训练监督信息。

        优先走精确路径匹配；若失败，再尝试后缀键匹配，
        以兼容本地和服务器之间的数据根目录差异。
        """

        normalized = _normalize_path(image_path)
        if normalized in self.rows_by_exact:
            return self.rows_by_exact[normalized]

        suffix = _suffix_key(image_path)
        return self.rows_by_suffix.get(suffix)


class MetadataAwareImageFolder(ImageFolder):
    """
    在 `ImageFolder` 基础上追加联合训练监督字段。

    返回值结构为：
    - image tensor
    - class target
    - image path
    - sp_prob
    - sp_valid
    - hard_weight
    - lvlm_labels
    - lvlm_valid
    - lvlm_confidence

    这样可以在不破坏现有 FSD 主体流程的前提下，把第一阶段和第二阶段监督
    统一接进训练入口。
    """

    def __init__(self, root, metadata_index=None, transform=None):
        super().__init__(root, transform=transform)
        self.metadata_index = metadata_index
        self.metadata_match_count = 0
        self.lvlm_match_count = 0

        if self.metadata_index is not None:
            for path, _ in self.samples:
                record = self.metadata_index.lookup(path)
                if record is not None:
                    self.metadata_match_count += 1
                    if float(record.get("lvlm_valid", 0.0)) > 0.5:
                        self.lvlm_match_count += 1

            warnings.warn(
                f"MetadataAwareImageFolder loaded {len(self.samples)} samples from {root}, "
                f"metadata matched {self.metadata_match_count} samples, "
                f"LVLM labels matched {self.lvlm_match_count} samples."
            )

    def __getitem__(self, index):
        path, target = self.samples[index]

        try:
            sample = self.loader(path)
        except (UnidentifiedImageError, OSError) as exc:
            warnings.warn(f"Skip unreadable image: {path} ({exc})")
            return self.__getitem__((index + 1) % len(self.samples))

        if self.transform is not None:
            sample = self.transform(sample)
        if self.target_transform is not None:
            target = self.target_transform(target)

        record = self.metadata_index.lookup(path) if self.metadata_index is not None else None

        if record is None or math.isnan(record["sp_prob_calibrated"]):
            sp_prob = 0.0
            sp_valid = 0.0
            hard_weight = 1.0
        else:
            sp_prob = float(record["sp_prob_calibrated"])
            sp_valid = 1.0
            hard_weight = float(record.get("hard_weight", 1.0))

        if record is None:
            lvlm_labels = [0.0 for _ in LVLM_LABEL_FIELDS]
            lvlm_valid = 0.0
            lvlm_confidence = 0.0
        else:
            lvlm_labels = list(record.get("lvlm_labels", [0.0 for _ in LVLM_LABEL_FIELDS]))
            lvlm_valid = float(record.get("lvlm_valid", 0.0))
            lvlm_confidence = float(record.get("lvlm_confidence", 0.0))

        return (
            sample,
            target,
            path,
            torch.tensor(sp_prob, dtype=torch.float32),
            torch.tensor(sp_valid, dtype=torch.float32),
            torch.tensor(hard_weight, dtype=torch.float32),
            torch.tensor(lvlm_labels, dtype=torch.float32),
            torch.tensor(lvlm_valid, dtype=torch.float32),
            torch.tensor(lvlm_confidence, dtype=torch.float32),
        )


def setup_joint_infinity_train_dataloader(
    folder_path,
    metadata_index=None,
    batch_size=20,
    num_workers=16,
    pin_memory=True,
    drop_last=True,
):
    """
    构建带联合监督信息的无限训练 dataloader。

    整体设计与原始 `setup_infinity_train_dataloader` 保持一致，
    这样 `train_joint.py` 可以最大程度复用现有 FSD 的任务采样逻辑。
    """

    transform = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
        ]
    )

    dataset = MetadataAwareImageFolder(
        folder_path,
        metadata_index=metadata_index,
        transform=transform,
    )
    sampler = DistributedSampler(dataset) if dist.is_initialized() else None

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=(sampler is None),
        sampler=sampler,
        num_workers=num_workers,
        pin_memory=pin_memory,
        drop_last=drop_last,
    )

    epoch = 0
    while True:
        if sampler is not None:
            sampler.set_epoch(epoch)
        epoch += 1
        yield from loader
