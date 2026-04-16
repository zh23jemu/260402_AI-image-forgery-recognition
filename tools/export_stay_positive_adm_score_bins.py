# -*- coding: utf-8 -*-
"""导出 Stay-Positive / ADM 分数分布统计表。"""

import argparse
import csv
import math
import os
from typing import Dict, List


def sigmoid(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-value))


def load_labels(path: str) -> Dict[str, str]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return {row["filename"]: row["typ"] for row in reader}


def load_scores(path: str, model_name: str) -> Dict[str, float]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return {row["filename"]: sigmoid(float(row[model_name])) for row in reader}


def build_rows(real_labels: Dict[str, str], fake_labels: Dict[str, str], real_scores: Dict[str, float], fake_scores: Dict[str, float]) -> List[Dict[str, float]]:
    rows: List[Dict[str, float]] = []
    for filename in real_labels:
        if filename in real_scores:
            rows.append({"filename": filename, "label": "real", "score": real_scores[filename]})
    for filename in fake_labels:
        if filename in fake_scores:
            rows.append({"filename": filename, "label": "fake", "score": fake_scores[filename]})
    return rows


def score_bin(score: float, bin_size: float) -> str:
    lower = math.floor(score / bin_size) * bin_size
    upper = min(1.0, lower + bin_size)
    return f"{lower:.2f}-{upper:.2f}"


def summarize_bins(rows: List[Dict[str, float]], bin_size: float) -> List[Dict[str, str]]:
    table: Dict[str, Dict[str, int]] = {}
    for row in rows:
        key = score_bin(float(row["score"]), bin_size)
        if key not in table:
            table[key] = {"real": 0, "fake": 0}
        table[key][row["label"]] += 1
    ordered = []
    for key in sorted(table.keys()):
        ordered.append(
            {
                "score_bin": key,
                "real_count": str(table[key]["real"]),
                "fake_count": str(table[key]["fake"]),
            }
        )
    return ordered


def write_csv(path: str, rows: List[Dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["score_bin", "real_count", "fake_count"])
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: str, rows: List[Dict[str, str]], bin_size: float, model_name: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    lines = [
        "# Stay-Positive / ADM 分数分布统计",
        "",
        f"模型：`{model_name}`",
        "",
        f"分桶宽度：`{bin_size:.2f}`",
        "",
        "| score_bin | real_count | fake_count |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['score_bin']} | {row['real_count']} | {row['fake_count']} |")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Stay-Positive ADM score bins.")
    parser.add_argument("--real_csv", required=True)
    parser.add_argument("--fake_csv", required=True)
    parser.add_argument("--real_scores_csv", required=True)
    parser.add_argument("--fake_scores_csv", required=True)
    parser.add_argument("--model_name", default="rajan-ours-plus")
    parser.add_argument("--bin_size", type=float, default=0.02)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--output_md", required=True)
    args = parser.parse_args()

    real_labels = load_labels(args.real_csv)
    fake_labels = load_labels(args.fake_csv)
    real_scores = load_scores(args.real_scores_csv, args.model_name)
    fake_scores = load_scores(args.fake_scores_csv, args.model_name)
    rows = build_rows(real_labels, fake_labels, real_scores, fake_scores)
    bins = summarize_bins(rows, args.bin_size)
    write_csv(args.output_csv, bins)
    write_md(args.output_md, bins, args.bin_size, args.model_name)
    print(f"Wrote score bins CSV to {args.output_csv}")
    print(f"Wrote score bins markdown to {args.output_md}")


if __name__ == "__main__":
    main()
