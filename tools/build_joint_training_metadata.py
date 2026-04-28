#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
构建三模型联合训练所需的统一元数据表。

当前版本的目标是把“第二阶段最小量化版”真正落成可训练输入：

1. 扫描 `GenImage` 目录，生成基础样本表
2. 合并可选的 `Stay-Positive` 分数与冲突信息
3. 合并可选的 `LVLM` 结构化语义标签
4. 生成适合联合训练的 `hard_weight`

这样生成出的 CSV 可以直接服务于：

- 第一阶段 `FSD + SP`
- 第二阶段最小量化版 `FSD + SP + LVLM labels`
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path


LVLM_FIELD_MAPPING = {
    "伪文本/伪界面": "lvlm_has_text_artifact",
    "局部结构连接异常": "lvlm_has_structure_error",
    "生物体局部真实性不足": "lvlm_has_bio_detail_error",
    "局部修补/过度平滑": "lvlm_has_patch_or_smooth",
}


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


def infer_adm_prompt_weak_labels(image_path: str) -> dict:
    """
    根据 ADM 文件名模板生成第二阶段最小量化版的弱 LVLM 标签。

    这不是人工逐图标注，而是基于现有 20 个结构化案例总结出的 prompt-level
    弱监督。它的作用是让第二阶段辅助头能够在 `train` split 中获得非零监督，
    从而完成“LVLM 结构化标签进入训练计算图”的最小量化验证。
    """

    name = Path(image_path).name.lower()
    record = {
        "lvlm_has_text_artifact": "0",
        "lvlm_has_layout_conflict": "0",
        "lvlm_has_structure_error": "1",
        "lvlm_has_bio_detail_error": "0",
        "lvlm_has_patch_or_smooth": "0",
        "lvlm_confidence": "0.45",
    }

    if "_adm_174" in name:
        record.update(
            {
                "lvlm_has_text_artifact": "1",
                "lvlm_has_layout_conflict": "1",
                "lvlm_has_structure_error": "1",
                "lvlm_confidence": "0.55",
            }
        )
    elif "_adm_153" in name:
        record.update(
            {
                "lvlm_has_layout_conflict": "1",
                "lvlm_has_structure_error": "1",
                "lvlm_has_patch_or_smooth": "1",
                "lvlm_confidence": "0.50",
            }
        )
    elif "_adm_7" in name or "_adm_85" in name or "_adm_91" in name:
        record.update(
            {
                "lvlm_has_structure_error": "1",
                "lvlm_has_bio_detail_error": "1",
                "lvlm_confidence": "0.50",
            }
        )
    elif "_adm_34" in name:
        record.update(
            {
                "lvlm_has_structure_error": "1",
                "lvlm_has_patch_or_smooth": "1",
                "lvlm_confidence": "0.48",
            }
        )

    return record


def scan_split_rows(
    data_root: Path,
    generator: str,
    split: str,
    max_files: int = 0,
    enable_adm_prompt_weak_lvlm: bool = False,
) -> list[dict]:
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

    scanned = 0
    for current_root, _, filenames in os.walk(leaf_dir):
        for filename in filenames:
            image_path = Path(current_root) / filename
            if not image_path.is_file():
                continue

            image_path_str = str(image_path)

            row = {
                "image_path": image_path_str,
                "path_key": normalize_path(image_path_str),
                "suffix_key": suffix_key(image_path_str),
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

            if enable_adm_prompt_weak_lvlm and generator == "ADM" and split == "train":
                row.update(infer_adm_prompt_weak_labels(image_path_str))
                row["subset_tag"] = "adm_prompt_weak_lvlm"
                row["hard_weight"] = max(float(row["hard_weight"]), 2.2)

            rows.append(row)
            scanned += 1

            if max_files > 0 and scanned >= max_files:
                return rows

    return rows


def build_lookup_keys(image_path: str) -> list[str]:
    """
    为同一路径生成多种查找键。

    这样可以兼容：
    - 服务器绝对路径
    - 本地绝对路径
    - `data/GenImage/...` 后缀路径
    """

    return [normalize_path(image_path), suffix_key(image_path)]


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


def load_lvlm_records(csv_paths: list[str]) -> dict:
    """
    读取 `LVLM` 结构化案例 CSV。

    当前输入默认对应：
    - `analysis/lvlm_structured_supplement_cases.csv`

    由于这是人工/结构化案例集，不是全量数据，因此只会匹配一小部分关键困难样本。
    这正符合第二阶段“先做最小量化验证”的目标。
    """

    mapping = {}

    for csv_path in csv_paths:
        with open(csv_path, "r", encoding="utf-8", newline="") as file_obj:
            reader = csv.DictReader(file_obj)
            for row in reader:
                image_path = row.get("image_path")
                if not image_path:
                    continue

                record = {
                    "subset_tag": row.get("case_type", row.get("selection_role", "adm_lvlm_case")),
                    "lvlm_has_text_artifact": "0",
                    "lvlm_has_layout_conflict": "0",
                    "lvlm_has_structure_error": "0",
                    "lvlm_has_bio_detail_error": "0",
                    "lvlm_has_patch_or_smooth": "0",
                    "lvlm_confidence": "0.85" if row.get("evidence_level") == "强" else "0.70",
                }

                primary = row.get("primary_abnormality", "").strip()
                secondary = row.get("secondary_abnormality", "").strip()
                scene_group = row.get("scene_group", "").strip()

                for abnormality in [primary, secondary]:
                    if abnormality in LVLM_FIELD_MAPPING:
                        record[LVLM_FIELD_MAPPING[abnormality]] = "1"

                # 设备/室内/复杂关系场景通常还伴随布局或关系异常，这里显式补一位。
                if scene_group in {"设备/伪界面", "室内/建筑/结构场景", "复杂生活场景"}:
                    record["lvlm_has_layout_conflict"] = "1"

                for key in build_lookup_keys(image_path):
                    mapping[key] = record

    return mapping


def merge_lvlm_records(rows: list[dict], lvlm_mapping: dict) -> None:
    """
    把 `LVLM` 结构化标签合并进基础元数据。

    合并策略：
    1. 只对匹配到的关键困难样本写入多标签
    2. 同时提高 `hard_weight`
    3. 保留已有 `subset_tag`，但优先让案例样本进入更明确的困难子集
    """

    for row in rows:
        record = lvlm_mapping.get(row["path_key"]) or lvlm_mapping.get(row["suffix_key"])
        if record is None:
            continue

        for field_name in [
            "lvlm_has_text_artifact",
            "lvlm_has_layout_conflict",
            "lvlm_has_structure_error",
            "lvlm_has_bio_detail_error",
            "lvlm_has_patch_or_smooth",
            "lvlm_confidence",
        ]:
            row[field_name] = record.get(field_name, row.get(field_name, ""))

        row["subset_tag"] = f"lvlm_{record.get('subset_tag', 'case')}"
        row["hard_weight"] = max(float(row["hard_weight"]), 2.5)


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
    parser.add_argument(
        "--lvlm_cases_csv",
        action="append",
        default=[],
        help="可重复传入多个 LVLM 结构化案例 CSV 路径。",
    )
    parser.add_argument(
        "--max_files_per_generator_split",
        type=int,
        default=0,
        help="每个 generator/split 最多扫描多少文件；0 表示不限制。",
    )
    parser.add_argument(
        "--enable_adm_prompt_weak_lvlm",
        action="store_true",
        help="是否为 ADM/train 根据文件名模板生成弱 LVLM 标签。",
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
            split_rows = scan_split_rows(
                data_root,
                generator,
                split,
                max_files=args.max_files_per_generator_split,
                enable_adm_prompt_weak_lvlm=args.enable_adm_prompt_weak_lvlm,
            )
            rows.extend(split_rows)
            print(f"Scanned {len(split_rows)} rows for {generator}/{split}", flush=True)

    score_mapping = {}
    if args.sp_score_csv:
        score_mapping = load_score_records(
            csv_paths=args.sp_score_csv,
            score_column=args.sp_score_column,
            prob_column=args.sp_prob_column,
        )
        merge_score_records(rows, score_mapping, priority_fake_generators)

    lvlm_mapping = {}
    if args.lvlm_cases_csv:
        lvlm_mapping = load_lvlm_records(args.lvlm_cases_csv)
        merge_lvlm_records(rows, lvlm_mapping)

    write_rows(output_csv, rows)

    print(f"Scanned rows: {len(rows)}")
    print(f"Loaded score entries: {len(score_mapping)}")
    print(f"Loaded LVLM entries: {len(lvlm_mapping)}")
    print(f"Output CSV: {output_csv}")


if __name__ == "__main__":
    main()
