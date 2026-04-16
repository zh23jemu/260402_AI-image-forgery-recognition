# -*- coding: utf-8 -*-
"""对 ADM 样本级结果做冲突模式结构化统计。"""

import argparse
import math
import os
import re
from typing import Dict, List

import pandas as pd


def calibrated_prediction(score: float, threshold: float) -> str:
    return "fake" if float(score) >= threshold else "real"


def extract_prompt_type(image_path: str) -> str:
    filename = os.path.basename(image_path)
    match = re.search(r"adm_(\d+)\.", filename, flags=re.IGNORECASE)
    if match:
        return f"adm_{match.group(1)}"
    return "unknown"


def extract_file_index(image_path: str) -> int:
    filename = os.path.basename(image_path)
    match = re.match(r"(\d+)_", filename)
    if match:
        return int(match.group(1))
    return -1


def build_enriched_frame(input_csv: str, threshold: float) -> pd.DataFrame:
    frame = pd.read_csv(input_csv).copy()
    frame["stay_positive_postcal_prediction"] = frame["stay_positive_score"].map(
        lambda value: calibrated_prediction(value, threshold)
    )
    frame["official_match"] = frame["official_fsd_prediction"] == frame["stay_positive_postcal_prediction"]
    frame["v1_match"] = frame["fsd_finetune_v1_prediction"] == frame["stay_positive_postcal_prediction"]
    frame["v2_match"] = frame["fsd_finetune_v2_prediction"] == frame["stay_positive_postcal_prediction"]
    frame["match_count"] = frame[["official_match", "v1_match", "v2_match"]].sum(axis=1)
    frame["conflict_count"] = 3 - frame["match_count"]
    frame["all_fsd_real"] = (
        (frame["official_fsd_prediction"] == "real")
        & (frame["fsd_finetune_v1_prediction"] == "real")
        & (frame["fsd_finetune_v2_prediction"] == "real")
    )
    frame["all_fsd_fake"] = (
        (frame["official_fsd_prediction"] == "fake")
        & (frame["fsd_finetune_v1_prediction"] == "fake")
        & (frame["fsd_finetune_v2_prediction"] == "fake")
    )
    frame["conflict_pattern"] = frame.apply(
        lambda row: (
            f"SP={row['stay_positive_postcal_prediction']};"
            f"FSD={row['official_fsd_prediction']}/{row['fsd_finetune_v1_prediction']}/{row['fsd_finetune_v2_prediction']}"
        ),
        axis=1,
    )
    frame["prompt_type"] = frame["image_path"].map(extract_prompt_type)
    frame["file_index"] = frame["image_path"].map(extract_file_index)
    frame["score_bin_left"] = frame["stay_positive_score"].map(lambda x: math.floor(float(x) / 0.02) * 0.02)
    frame["score_bin"] = frame["score_bin_left"].map(lambda x: f"{x:.2f}-{x + 0.02:.2f}")
    return frame


def summarize_conflict_patterns(frame: pd.DataFrame) -> pd.DataFrame:
    summary = (
        frame.groupby("conflict_pattern", dropna=False)
        .agg(
            sample_count=("sample_id", "count"),
            mean_sp_score=("stay_positive_score", "mean"),
            min_sp_score=("stay_positive_score", "min"),
            max_sp_score=("stay_positive_score", "max"),
        )
        .reset_index()
        .sort_values(["sample_count", "mean_sp_score"], ascending=[False, False])
    )
    return summary


def summarize_prompt_types(frame: pd.DataFrame) -> pd.DataFrame:
    summary = (
        frame.groupby(["prompt_type", "conflict_pattern"], dropna=False)
        .agg(
            sample_count=("sample_id", "count"),
            mean_sp_score=("stay_positive_score", "mean"),
        )
        .reset_index()
        .sort_values(["sample_count", "mean_sp_score"], ascending=[False, False])
    )
    return summary


def summarize_score_bins(frame: pd.DataFrame) -> pd.DataFrame:
    summary = (
        frame.groupby(["score_bin", "conflict_pattern"], dropna=False)
        .agg(
            sample_count=("sample_id", "count"),
            min_sp_score=("stay_positive_score", "min"),
            max_sp_score=("stay_positive_score", "max"),
        )
        .reset_index()
        .sort_values(["score_bin", "sample_count"], ascending=[True, False])
    )
    return summary


def build_key_findings(frame: pd.DataFrame, pattern_summary: pd.DataFrame, prompt_summary: pd.DataFrame) -> List[str]:
    findings: List[str] = []
    total_count = len(frame)
    strong_conflict = int((frame["conflict_count"] == 3).sum())
    findings.append(f"总样本数为 `{total_count}`，其中 `Stay-Positive` 校准后与三组 FSD 全冲突的样本数为 `{strong_conflict}`。")

    if not pattern_summary.empty:
        top_row = pattern_summary.iloc[0]
        findings.append(
            "最主要的冲突模式为 "
            f"`{top_row['conflict_pattern']}`，共 `{int(top_row['sample_count'])}` 个样本，"
            f"对应 Stay-Positive 平均分数约为 `{float(top_row['mean_sp_score']):.4f}`。"
        )

    if not prompt_summary.empty:
        prompt_top = prompt_summary.iloc[0]
        findings.append(
            f"按文件名模板统计，`{prompt_top['prompt_type']}` 是当前最密集的冲突模板之一，"
            f"其主导冲突模式为 `{prompt_top['conflict_pattern']}`，样本数为 `{int(prompt_top['sample_count'])}`。"
        )

    all_real_count = int(
        (
            (frame["stay_positive_postcal_prediction"] == "fake")
            & frame["all_fsd_real"]
        ).sum()
    )
    findings.append(
        f"`Stay-Positive` 校准后判 `fake` 且三组 FSD 全判 `real` 的样本共有 `{all_real_count}` 个，"
        "这是当前最值得优先解释的互补性子集。"
    )
    return findings


def write_markdown(
    output_md: str,
    threshold: float,
    frame: pd.DataFrame,
    pattern_summary: pd.DataFrame,
    prompt_summary: pd.DataFrame,
    score_summary: pd.DataFrame,
) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(output_md)), exist_ok=True)
    findings = build_key_findings(frame, pattern_summary, prompt_summary)
    lines = [
        "# ADM 冲突模式结构化统计",
        "",
        f"校准阈值：`{threshold:.6f}`",
        "",
        "## 1. 关键发现",
        "",
    ]
    for item in findings:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## 2. 冲突模式 Top 10",
            "",
            "| conflict_pattern | sample_count | mean_sp_score | min_sp_score | max_sp_score |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for _, row in pattern_summary.head(10).iterrows():
        lines.append(
            f"| {row['conflict_pattern']} | {int(row['sample_count'])} | {float(row['mean_sp_score']):.4f} | {float(row['min_sp_score']):.4f} | {float(row['max_sp_score']):.4f} |"
        )

    lines.extend(
        [
            "",
            "## 3. prompt_type Top 10",
            "",
            "| prompt_type | conflict_pattern | sample_count | mean_sp_score |",
            "| --- | --- | --- | --- |",
        ]
    )
    for _, row in prompt_summary.head(10).iterrows():
        lines.append(
            f"| {row['prompt_type']} | {row['conflict_pattern']} | {int(row['sample_count'])} | {float(row['mean_sp_score']):.4f} |"
        )

    lines.extend(
        [
            "",
            "## 4. 分数区间 Top 15",
            "",
            "| score_bin | conflict_pattern | sample_count | min_sp_score | max_sp_score |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for _, row in score_summary.head(15).iterrows():
        lines.append(
            f"| {row['score_bin']} | {row['conflict_pattern']} | {int(row['sample_count'])} | {float(row['min_sp_score']):.4f} | {float(row['max_sp_score']):.4f} |"
        )

    with open(output_md, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize ADM conflict patterns.")
    parser.add_argument("--input_csv", required=True, help="Unified ADM sample export CSV.")
    parser.add_argument("--threshold", type=float, default=0.388818)
    parser.add_argument("--output_dir", required=True, help="Directory for CSV summaries.")
    parser.add_argument("--output_md", required=True, help="Markdown summary path.")
    args = parser.parse_args()

    frame = build_enriched_frame(args.input_csv, args.threshold)
    pattern_summary = summarize_conflict_patterns(frame)
    prompt_summary = summarize_prompt_types(frame)
    score_summary = summarize_score_bins(frame)

    os.makedirs(args.output_dir, exist_ok=True)
    pattern_csv = os.path.join(args.output_dir, "adm_conflict_pattern_summary.csv")
    prompt_csv = os.path.join(args.output_dir, "adm_conflict_prompt_summary.csv")
    score_csv = os.path.join(args.output_dir, "adm_conflict_scorebin_summary.csv")
    enriched_csv = os.path.join(args.output_dir, "adm_sample_export_enriched.csv")

    frame.to_csv(enriched_csv, index=False)
    pattern_summary.to_csv(pattern_csv, index=False)
    prompt_summary.to_csv(prompt_csv, index=False)
    score_summary.to_csv(score_csv, index=False)
    write_markdown(args.output_md, args.threshold, frame, pattern_summary, prompt_summary, score_summary)

    print(f"Wrote enriched sample export to {enriched_csv}")
    print(f"Wrote conflict pattern summary to {pattern_csv}")
    print(f"Wrote prompt summary to {prompt_csv}")
    print(f"Wrote score-bin summary to {score_csv}")
    print(f"Wrote markdown summary to {args.output_md}")


if __name__ == "__main__":
    main()
