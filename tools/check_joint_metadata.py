# -*- coding: utf-8 -*-
"""检查联合训练 metadata 是否满足开跑条件。"""

import argparse
import csv
from collections import Counter


LVLM_FIELDS = [
    "lvlm_has_text_artifact",
    "lvlm_has_layout_conflict",
    "lvlm_has_structure_error",
    "lvlm_has_bio_detail_error",
    "lvlm_has_patch_or_smooth",
]


def is_filled(value: str) -> bool:
    """判断一个 CSV 字段是否有有效值。"""

    return value not in ("", "0", "0.0", "nan", "None", None)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check joint metadata readiness.")
    parser.add_argument("--metadata_csv", required=True)
    args = parser.parse_args()

    with open(args.metadata_csv, "r", encoding="utf-8", newline="") as file_obj:
        rows = list(csv.DictReader(file_obj))

    split_counter = Counter(row.get("split", "") for row in rows)
    generator_counter = Counter(row.get("generator", "") for row in rows)
    subset_counter = Counter(row.get("subset_tag", "") for row in rows)
    rows_with_sp = sum(1 for row in rows if row.get("sp_prob_calibrated") not in ("", "nan"))
    rows_with_lvlm = sum(1 for row in rows if any(is_filled(row.get(field, "")) for field in LVLM_FIELDS))
    train_rows_with_lvlm = sum(
        1
        for row in rows
        if row.get("split") == "train" and any(is_filled(row.get(field, "")) for field in LVLM_FIELDS)
    )

    print(f"metadata_csv={args.metadata_csv}")
    print(f"total_rows={len(rows)}")
    print(f"rows_with_sp={rows_with_sp}")
    print(f"rows_with_lvlm={rows_with_lvlm}")
    print(f"train_rows_with_lvlm={train_rows_with_lvlm}")
    print(f"split_counter={dict(split_counter)}")
    print(f"generator_counter={dict(generator_counter)}")
    print(f"top_subset_tags={subset_counter.most_common(10)}")

    if len(rows) == 0:
        print("READY=NO reason=empty_metadata")
    elif train_rows_with_lvlm == 0:
        print("READY=NO reason=no_train_lvlm_labels")
    else:
        print("READY=YES")


if __name__ == "__main__":
    main()
