#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
构建三模型联合训练所需的统一元数据表。

第一版目标不是一次性把所有监督都补齐，而是先生成一张可以被
`FSD + Stay-Positive` 联合训练直接使用的 CSV。

支持三类能力：

1. 扫描 `GenImage` 目录，生成基础样本表
2. 合并可选的 `Stay-Positive` 分数 CSV
3. 生成基础 `hard_weight`

当前默认重点服务于：

- `real`
- `ADM`
- `SD`
- `Midjourney`
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path


def normalize_path(path: str) -> str:
    """统一路径格式，方便不同 CSV 之间对齐。"""

    normalized = str(path).replace("\\", "/").strip()
    while "//" in normalized:
        normalized = normalized.replace("//", "/")
    normalized = normalized.rstrip("/")
    if os.name == "nt":
        normalized = normalized.lower()
    return normalized


def suffix_key(path: str) -> str:
    """
    提取 `data/GenImage/...` 之后的后缀键。

    这样可以把服务器路径和本地路径对齐到同一个相对标识上。
    """

    normalized = normalize_path(path)
    parts = normalized.split("/")
    lowered = [part.lower() for part in parts]
    for index in range(len(parts) - 1):
        if lowered[index] == "data" and lowered[index + 1] == "genimage":
            return "/".join(parts[index:])
    return "/".join(parts[-5:])


def parse_list_arg(value: str) -> list[str]:
    """解析逗号分隔参数。"""

    return [item.strip() for item in value.split(",") if item.strip()]


def scan_split_rows(data_root: Path, generator: str, split: str) -> list[dict]:
    """
    扫描单个生成器 / 单个 split 的样本。

    目录约定：
    - `real/<split>/nature/*`
    - `fake_generator/<split>/ai/*`
    """

    rows = []
    label = 0 if generator == "real" else 1
    leaf_name = "nature" if generator == "real" else "ai"
    leaf_dir = data_root / generator / split / leaf_name

    if not leaf_dir.exists():
        return rows

    for image_path in sorted(leaf_dir.rglob("*")):
        if not image_path.is_file():
            continue

        rows.append(
            {
                "image_path": str(image_path.resolve()),
                "path_key": normalize_path(str(image_path.resolve())),
                "suffix_key": suffix_key(str(image_path.resolve())),
                "split": split,
                "generator": generator,
                "label": label,
                "subset_tag": "standard" if generator != "ADM" else "adm_core",
                "sp_score_raw": "",
                "sp_prob_calibrated": "",
                "sp_pred_default": "",
                "sp_pred_calibrated": "",
                "sp_conflict_flag": 0,
                "fsd_base_pred": "",
                "fsd_base_score": "",
                "lvlm_has_text_artifact": "",
                "lvlm_has_layout_conflict": "",
                "lvlm_has_structure_error": "",
                "lvlm_has_bio_detail_error": "",
                "lvlm_has_patch_or_smooth": "",
                "lvlm_confidence": "",
                "hard_weight": 1.0 if generator == "real" else 1.5,
            }
        )

    return rows


def load_score_records(csv_paths: list[str], score_column: str, prob_column: str) -> dict:
    """
    读取外部分数 CSV，并按路径建立索引。

    支持两种常见路径列：
    - `image_path`
    - `filename`
    """

    mapping = {}
    for csv_path in csv_paths:
        with open(csv_path, "r", encoding="utf-8", newline="") as file_obj:
            reader = csv.DictReader(file_obj)
            for row in reader:
                image_path = row.get("image_path") or row.get("filename")
                if not image_path:
                    continue

                record = {
                    "sp_score_raw": row.get(score_column, row.get("stay_positive_score", "")),
                    "sp_prob_calibrated": row.get(
                        prob_column,
                        row.get(score_column, row.get("stay_positive_score", "")),
                    ),
                    "sp_pred_default": row.get("stay_positive_prediction", row.get("pred_label", "")),
                    "sp_pred_calibrated": row.get("stay_positive_postcal_prediction", ""),
                    "sp_conflict_flag": row.get("sp_conflict_flag", row.get("conflict_count", 0)),
                    "fsd_base_pred": row.get("official_fsd_prediction", row.get("pred_label", "")),
                    "fsd_base_score": row.get("official_fsd_score", row.get("prob_fake", "")),
                }

                mapping[normalize_path(image_path)] = record
                mapping[suffix_key(image_path)] = record

    return mapping


def merge_score_records(rows: list[dict], score_mapping: dict, priority_fake_generators: set[str]) -> None:
    """
    把外部分数信息合并进基础元数据。

    如果样本被标记为冲突样本或属于高优先级困难类别，则同步提高 `hard_weight`。
    """

    for row in rows:
        record = score_mapping.get(row["path_key"]) or score_mapping.get(row["suffix_key"])
        if record is None:
            continue

        row["sp_score_raw"] = record.get("sp_score_raw", "")
        row["sp_prob_calibrated"] = record.get("sp_prob_calibrated", "")
        row["sp_pred_default"] = record.get("sp_pred_default", "")
        row["sp_pred_calibrated"] = record.get("sp_pred_calibrated", "")
        row["fsd_base_pred"] = record.get("fsd_base_pred", "")
        row["fsd_base_score"] = record.get("fsd_base_score", "")

        try:
            conflict_flag = int(float(record.get("sp_conflict_flag", 0))) > 0
        except (TypeError, ValueError):
            conflict_flag = False

        row["sp_conflict_flag"] = 1 if conflict_flag else 0

        if conflict_flag:
            row["hard_weight"] = max(float(row["hard_weight"]), 2.0)
        elif row["generator"] in priority_fake_generators and row["label"] == 1:
            row["hard_weight"] = max(float(row["hard_weight"]), 1.8)


def write_rows(output_csv: Path, rows: list[dict]) -> None:
    """写出统一元数据 CSV。"""

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "image_path",
        "split",
        "generator",
        "label",
        "subset_tag",
        "sp_score_raw",
        "sp_prob_calibrated",
        "sp_pred_default",
        "sp_pred_calibrated",
        "sp_conflict_flag",
        "fsd_base_pred",
        "fsd_base_score",
        "lvlm_has_text_artifact",
        "lvlm_has_layout_conflict",
        "lvlm_has_structure_error",
        "lvlm_has_bio_detail_error",
        "lvlm_has_patch_or_smooth",
        "lvlm_confidence",
        "hard_weight",
    ]

    with open(output_csv, "w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            output_row = {field: row.get(field, "") for field in fieldnames}
            writer.writerow(output_row)


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(description="构建联合训练元数据 CSV。")
    parser.add_argument("--data_root", type=str, required=True, help="GenImage 根目录。")
    parser.add_argument(
        "--output_csv",
        type=str,
        default="analysis/joint_training_metadata.csv",
        help="输出元数据 CSV 路径。",
    )
    parser.add_argument(
        "--generators",
        type=str,
        default="real,ADM,SD,Midjourney",
        help="要扫描的生成器列表，逗号分隔。",
    )
    parser.add_argument(
        "--splits",
        type=str,
        default="train,val",
        help="要扫描的数据划分，逗号分隔。",
    )
    parser.add_argument(
        "--sp_score_csv",
        action="append",
        default=[],
        help="可重复传入多个包含 Stay-Positive 分数的 CSV 路径。",
    )
    parser.add_argument(
        "--sp_score_column",
        type=str,
        default="stay_positive_score",
        help="Stay-Positive 原始分数字段名。",
    )
    parser.add_argument(
        "--sp_prob_column",
        type=str,
        default="sp_prob_calibrated",
        help="Stay-Positive 概率字段名；若不存在则退化为 score 字段。",
    )
    parser.add_argument(
        "--priority_fake_generators",
        type=str,
        default="ADM",
        help="需要默认抬高 hard_weight 的困难类别列表。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_root = Path(args.data_root)
    output_csv = Path(args.output_csv)

    generators = parse_list_arg(args.generators)
    splits = parse_list_arg(args.splits)
    priority_fake_generators = set(parse_list_arg(args.priority_fake_generators))

    rows = []
    for generator in generators:
        for split in splits:
            rows.extend(scan_split_rows(data_root, generator, split))

    score_mapping = {}
    if args.sp_score_csv:
        score_mapping = load_score_records(
            csv_paths=args.sp_score_csv,
            score_column=args.sp_score_column,
            prob_column=args.sp_prob_column,
        )
        merge_score_records(rows, score_mapping, priority_fake_generators)

    write_rows(output_csv, rows)

    print(f"Scanned rows: {len(rows)}")
    print(f"Loaded score entries: {len(score_mapping)}")
    print(f"Output CSV: {output_csv}")


if __name__ == "__main__":
    main()
