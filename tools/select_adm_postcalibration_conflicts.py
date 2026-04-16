# -*- coding: utf-8 -*-
"""筛选 Stay-Positive 校准后仍与 FSD 冲突的 ADM 样本。"""

import argparse
import csv
import os
from typing import Dict, List


def calibrated_prediction(score: float, threshold: float) -> str:
    return "fake" if score >= threshold else "real"


def load_rows(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_conflicts(rows: List[Dict[str, str]], threshold: float) -> List[Dict[str, str]]:
    selected: List[Dict[str, str]] = []
    for row in rows:
        score = float(row["stay_positive_score"])
        post_pred = calibrated_prediction(score, threshold)
        official = row["official_fsd_prediction"]
        v1 = row["fsd_finetune_v1_prediction"]
        v2 = row["fsd_finetune_v2_prediction"]

        conflict_count = sum([official != post_pred, v1 != post_pred, v2 != post_pred])
        if conflict_count == 0:
            continue

        if conflict_count >= 2:
            conflict_type = "strong_conflict"
        else:
            conflict_type = "single_conflict"

        selected.append(
            {
                "sample_id": row["sample_id"],
                "image_path": row["image_path"],
                "ground_truth": row["ground_truth"],
                "stay_positive_score": row["stay_positive_score"],
                "stay_positive_postcal_prediction": post_pred,
                "official_fsd_prediction": official,
                "fsd_finetune_v1_prediction": v1,
                "fsd_finetune_v2_prediction": v2,
                "conflict_count": str(conflict_count),
                "conflict_type": conflict_type,
                "priority_score": f"{conflict_count * 10 + abs(score - threshold):.6f}",
            }
        )
    selected.sort(key=lambda row: float(row["priority_score"]), reverse=True)
    return selected


def write_csv(path: str, rows: List[Dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fieldnames = [
        "sample_id",
        "image_path",
        "ground_truth",
        "stay_positive_score",
        "stay_positive_postcal_prediction",
        "official_fsd_prediction",
        "fsd_finetune_v1_prediction",
        "fsd_finetune_v2_prediction",
        "conflict_count",
        "conflict_type",
        "priority_score",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: str, rows: List[Dict[str, str]], threshold: float, top_k: int) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    lines = [
        "# ADM 校准后仍冲突样本",
        "",
        f"Stay-Positive 校准阈值：`{threshold:.6f}`",
        "",
        "| sample_id | postcal_pred | official | v1 | v2 | conflict_count | type |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows[:top_k]:
        lines.append(
            f"| {row['sample_id']} | {row['stay_positive_postcal_prediction']} | {row['official_fsd_prediction']} | {row['fsd_finetune_v1_prediction']} | {row['fsd_finetune_v2_prediction']} | {row['conflict_count']} | {row['conflict_type']} |"
        )
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Select ADM post-calibration conflicts.")
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--threshold", type=float, required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--output_md", required=True)
    parser.add_argument("--top_k", type=int, default=20)
    args = parser.parse_args()

    rows = load_rows(args.input_csv)
    selected = build_conflicts(rows, args.threshold)
    write_csv(args.output_csv, selected)
    write_md(args.output_md, selected, args.threshold, args.top_k)
    print(f"Wrote {len(selected)} post-calibration conflict rows to {args.output_csv}")
    print(f"Wrote markdown summary to {args.output_md}")


if __name__ == "__main__":
    main()
