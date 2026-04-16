# -*- coding: utf-8 -*-
"""从 ADM 校准后冲突样本中导出下一批案例。"""

import argparse
import csv
import os
from typing import Dict, List


def load_rows(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def select_rows(rows: List[Dict[str, str]], conflict_type: str, top_k: int) -> List[Dict[str, str]]:
    filtered = [row for row in rows if row.get("conflict_type") == conflict_type]
    filtered.sort(key=lambda row: float(row["priority_score"]), reverse=True)
    return filtered[:top_k]


def write_csv(path: str, rows: List[Dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    if not rows:
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
            "case_reason",
        ]
    else:
        fieldnames = list(rows[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def enrich_rows(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    enriched = []
    for idx, row in enumerate(rows, start=1):
        enriched_row = dict(row)
        enriched_row["case_reason"] = "Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。"
        enriched_row["case_id"] = f"adm_conflict_batch_{idx:02d}"
        enriched.append(enriched_row)
    return enriched


def write_md(path: str, rows: List[Dict[str, str]], conflict_type: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    lines = [
        "# ADM 下一批冲突案例清单",
        "",
        f"筛选类型：`{conflict_type}`",
        "",
        "| case_id | sample_id | postcal_pred | official | v1 | v2 | score | reason |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['case_id']} | {row['sample_id']} | {row['stay_positive_postcal_prediction']} | {row['official_fsd_prediction']} | {row['fsd_finetune_v1_prediction']} | {row['fsd_finetune_v2_prediction']} | {float(row['stay_positive_score']):.6f} | {row['case_reason']} |"
        )
    lines.extend(
        [
            "",
            "## 简要说明",
            "",
            "- 这批样本的共同特点是：`Stay-Positive` 在校准后已经稳定判为 `fake`，但 `FSD` 官方基线、首轮微调和第二轮保守微调仍全部判为 `real`。",
            "- 因此，这批样本更适合作为“FSD 系统性盲区”与“方法互补性”分析入口。",
        ]
    )
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Select next ADM conflict batch.")
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--conflict_type", default="strong_conflict")
    parser.add_argument("--top_k", type=int, default=20)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--output_md", required=True)
    args = parser.parse_args()

    rows = load_rows(args.input_csv)
    selected = select_rows(rows, args.conflict_type, args.top_k)
    enriched = enrich_rows(selected)
    write_csv(args.output_csv, enriched)
    write_md(args.output_md, enriched, args.conflict_type)
    print(f"Wrote {len(enriched)} rows to {args.output_csv}")
    print(f"Wrote markdown summary to {args.output_md}")


if __name__ == "__main__":
    main()
