# -*- coding: utf-8 -*-
"""为 ADM strong-conflict 样本生成下一批案例包。"""

import argparse
import csv
import os
from typing import Dict, List


def load_rows(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def select_rows(rows: List[Dict[str, str]], top_k: int) -> List[Dict[str, str]]:
    def sort_key(row: Dict[str, str]) -> float:
        if row.get("priority_score"):
            return float(row["priority_score"])
        if row.get("stay_positive_score"):
            return float(row["stay_positive_score"])
        return 0.0

    rows = sorted(rows, key=sort_key, reverse=True)
    return rows[:top_k]


def enrich(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    enriched = []
    for idx, row in enumerate(rows, start=1):
        item = dict(row)
        item["case_id"] = f"adm_conflict_priority_{idx:02d}"
        item["case_reason"] = "Stay-Positive 校准后稳定判 fake，但 FSD official / v1 / v2 全部判 real，适合做方法互补性案例。"
        item["prompt_type"] = "conflict"
        if not item.get("priority_score"):
            item["priority_score"] = item.get("stay_positive_score", "0")
        enriched.append(item)
    return enriched


def ensure_parent(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)


def write_csv(path: str, rows: List[Dict[str, str]]) -> None:
    ensure_parent(path)
    fieldnames = [
        "case_id",
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
        "prompt_type",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([{k: row.get(k, "") for k in fieldnames} for row in rows])


def build_sync_md(rows: List[Dict[str, str]]) -> str:
    lines = [
        "# ADM 冲突批次图片同步清单",
        "",
        "这份清单用于同步下一批 `strong_conflict` 案例图片。",
        "",
        "| case_id | sample_id | image_path | 当前作用 |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['case_id']} | {row['sample_id']} | {row['image_path']} | {row['case_reason']} |"
        )
    return "\n".join(lines)


def build_execution_md(rows: List[Dict[str, str]]) -> str:
    lines = [
        "# ADM 冲突批次执行包",
        "",
        "这份文档用于对下一批 `strong_conflict` 案例做人工观察或 LVLM 分析。",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['case_id']}",
                "",
                f"- `sample_id`: `{row['sample_id']}`",
                f"- `image_path`: `{row['image_path']}`",
                f"- `stay_positive_postcal_prediction`: `{row['stay_positive_postcal_prediction']}`",
                f"- `official / v1 / v2`: `{row['official_fsd_prediction']} / {row['fsd_finetune_v1_prediction']} / {row['fsd_finetune_v2_prediction']}`",
                f"- `stay_positive_score`: `{float(row['stay_positive_score']):.6f}`",
                "",
                "```text",
                "这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。",
                "",
                "请你从语义与视觉细节两个层面分析：",
                "1. 图像整体为什么容易被当成真实图像。",
                "2. 图像中哪些局部细节支持它更像 AI 生成图像。",
                "3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。",
                "4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。",
                "",
                "最后请补 3 句话：",
                "1. 这张图最关键的可疑点是什么。",
                "2. 这个案例更像局部结构问题还是整体语义误导问题。",
                "3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。",
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def build_result_md(rows: List[Dict[str, str]]) -> str:
    lines = [
        "# ADM 冲突批次结果填写页",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['case_id']}",
                "",
                "```text",
                f"case_id: {row['case_id']}",
                f"sample_id: {row['sample_id']}",
                f"image_path: {row['image_path']}",
                "",
                "visual_observation:",
                "",
                "judgement:",
                "",
                "key_evidence_1:",
                "",
                "key_evidence_2:",
                "",
                "paper_ready_summary:",
                "",
                "human_takeaway:",
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def write_text(path: str, content: str) -> None:
    ensure_parent(path)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ADM conflict priority pack.")
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--top_k", type=int, default=5)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--sync_md", required=True)
    parser.add_argument("--execution_md", required=True)
    parser.add_argument("--result_md", required=True)
    args = parser.parse_args()

    rows = enrich(select_rows(load_rows(args.input_csv), args.top_k))
    write_csv(args.output_csv, rows)
    write_text(args.sync_md, build_sync_md(rows))
    write_text(args.execution_md, build_execution_md(rows))
    write_text(args.result_md, build_result_md(rows))
    print(f"Wrote {len(rows)} rows to {args.output_csv}")
    print(f"Wrote sync list to {args.sync_md}")
    print(f"Wrote execution pack to {args.execution_md}")
    print(f"Wrote result sheet to {args.result_md}")


if __name__ == "__main__":
    main()
