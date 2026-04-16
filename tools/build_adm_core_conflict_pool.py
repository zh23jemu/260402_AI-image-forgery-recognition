# -*- coding: utf-8 -*-
"""从 ADM 核心冲突样本中构建均衡代表样本池。"""

import argparse
import os
from typing import List

import pandas as pd


TARGET_PATTERN = "SP=fake;FSD=real/real/real"


def load_core_rows(path: str, conflict_pattern: str) -> pd.DataFrame:
    frame = pd.read_csv(path).copy()
    frame = frame[frame["conflict_pattern"] == conflict_pattern].copy()
    frame["score_distance"] = (frame["stay_positive_score"] - 0.388818).abs()
    frame["source_name"] = frame["image_path"].map(lambda x: os.path.basename(x))
    return frame


def balanced_select(frame: pd.DataFrame, per_prompt: int, max_total: int) -> pd.DataFrame:
    picked: List[pd.DataFrame] = []
    for prompt_type, group in frame.groupby("prompt_type", sort=True):
        ordered = group.sort_values(
            ["stay_positive_score", "score_distance", "sample_id"],
            ascending=[False, False, True],
        )
        picked.append(ordered.head(per_prompt))
    selected = pd.concat(picked, ignore_index=True) if picked else frame.head(0).copy()
    selected = selected.sort_values(
        ["stay_positive_score", "prompt_type", "sample_id"],
        ascending=[False, True, True],
    )
    if len(selected) > max_total:
        selected = selected.head(max_total).copy()
    return selected.reset_index(drop=True)


def add_case_metadata(frame: pd.DataFrame, prefix: str) -> pd.DataFrame:
    frame = frame.copy()
    frame.insert(0, "case_id", [f"{prefix}_{idx + 1:02d}" for idx in range(len(frame))])
    frame["case_reason"] = (
        "属于核心互补模式 SP=fake;FSD=real/real/real，用于继续筛查 "
        "FSD 系统性盲区的代表样本。"
    )
    frame["selection_rule"] = "balanced_by_prompt_type"
    return frame


def write_markdown(path: str, frame: pd.DataFrame, conflict_pattern: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    lines = [
        "# ADM 核心冲突代表样本池",
        "",
        f"目标模式：`{conflict_pattern}`",
        "",
        "| case_id | sample_id | prompt_type | score_bin | stay_positive_score | source_name |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for _, row in frame.iterrows():
        lines.append(
            f"| {row['case_id']} | {row['sample_id']} | {row['prompt_type']} | {row['score_bin']} | {float(row['stay_positive_score']):.6f} | {row['source_name']} |"
        )
    lines.extend(
        [
            "",
            "## 说明",
            "",
            "- 这批样本全部来自 `SP=fake;FSD=real/real/real` 的核心互补模式。",
            "- 当前按 `prompt_type` 做均衡抽样，避免再次只看到单一模板。",
            "- 这批样本适合继续做真实视觉观察、LVLM 分析或进一步图片同步。",
        ]
    )
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ADM core conflict representative pool.")
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--output_md", required=True)
    parser.add_argument("--conflict_pattern", default=TARGET_PATTERN)
    parser.add_argument("--per_prompt", type=int, default=4)
    parser.add_argument("--max_total", type=int, default=24)
    parser.add_argument("--case_prefix", default="adm_core_conflict")
    args = parser.parse_args()

    frame = load_core_rows(args.input_csv, args.conflict_pattern)
    selected = balanced_select(frame, args.per_prompt, args.max_total)
    selected = add_case_metadata(selected, args.case_prefix)

    os.makedirs(os.path.dirname(os.path.abspath(args.output_csv)), exist_ok=True)
    selected.to_csv(args.output_csv, index=False)
    write_markdown(args.output_md, selected, args.conflict_pattern)
    print(f"Wrote {len(selected)} representative rows to {args.output_csv}")
    print(f"Wrote markdown summary to {args.output_md}")


if __name__ == "__main__":
    main()
