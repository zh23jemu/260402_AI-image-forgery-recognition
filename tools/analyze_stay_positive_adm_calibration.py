# -*- coding: utf-8 -*-
"""分析 Stay-Positive 在 ADM 上的阈值与校准现象。"""

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


def merge_rows(
    real_labels: Dict[str, str],
    fake_labels: Dict[str, str],
    real_scores: Dict[str, float],
    fake_scores: Dict[str, float],
) -> List[Dict[str, float]]:
    rows: List[Dict[str, float]] = []
    for filename, label in real_labels.items():
        if filename in real_scores:
            rows.append({"filename": filename, "label": 0, "score": real_scores[filename]})
    for filename, label in fake_labels.items():
        if filename in fake_scores:
            rows.append({"filename": filename, "label": 1, "score": fake_scores[filename]})
    return rows


def calc_metrics(rows: List[Dict[str, float]], threshold: float) -> Dict[str, float]:
    tp = fp = tn = fn = 0
    real_total = fake_total = 0
    for row in rows:
        label = row["label"]
        pred = 1 if row["score"] >= threshold else 0
        if label == 1:
            fake_total += 1
            if pred == 1:
                tp += 1
            else:
                fn += 1
        else:
            real_total += 1
            if pred == 0:
                tn += 1
            else:
                fp += 1
    total = len(rows)
    return {
        "threshold": threshold,
        "acc": (tp + tn) / total if total else 0.0,
        "racc": tn / real_total if real_total else 0.0,
        "facc": tp / fake_total if fake_total else 0.0,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


def find_best_threshold(rows: List[Dict[str, float]]) -> Dict[str, float]:
    candidates = sorted({round(row["score"], 6) for row in rows})
    if 0.5 not in candidates:
        candidates.append(0.5)
    candidates = sorted(set(candidates))
    best = None
    for threshold in candidates:
        metrics = calc_metrics(rows, threshold)
        if best is None or metrics["acc"] > best["acc"]:
            best = metrics
    return best if best is not None else calc_metrics(rows, 0.5)


def summarize_score_bands(rows: List[Dict[str, float]]) -> Dict[str, float]:
    fake_scores = [row["score"] for row in rows if row["label"] == 1]
    real_scores = [row["score"] for row in rows if row["label"] == 0]
    return {
        "fake_mean": sum(fake_scores) / len(fake_scores) if fake_scores else 0.0,
        "real_mean": sum(real_scores) / len(real_scores) if real_scores else 0.0,
        "fake_min": min(fake_scores) if fake_scores else 0.0,
        "fake_max": max(fake_scores) if fake_scores else 0.0,
        "real_min": min(real_scores) if real_scores else 0.0,
        "real_max": max(real_scores) if real_scores else 0.0,
    }


def write_summary(path: str, summary: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(summary)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Stay-Positive ADM calibration.")
    parser.add_argument("--real_csv", required=True)
    parser.add_argument("--fake_csv", required=True)
    parser.add_argument("--real_scores_csv", required=True)
    parser.add_argument("--fake_scores_csv", required=True)
    parser.add_argument("--model_name", default="rajan-ours-plus")
    parser.add_argument("--output_md", required=True)
    args = parser.parse_args()

    real_labels = load_labels(args.real_csv)
    fake_labels = load_labels(args.fake_csv)
    real_scores = load_scores(args.real_scores_csv, args.model_name)
    fake_scores = load_scores(args.fake_scores_csv, args.model_name)
    rows = merge_rows(real_labels, fake_labels, real_scores, fake_scores)

    default_metrics = calc_metrics(rows, 0.5)
    best_metrics = find_best_threshold(rows)
    bands = summarize_score_bands(rows)

    summary = f"""# Stay-Positive / ADM 阈值分析

模型：`{args.model_name}`

## 默认阈值 0.5

- ACC: {default_metrics['acc']:.6f}
- RACC: {default_metrics['racc']:.6f}
- FACC: {default_metrics['facc']:.6f}
- TP / TN / FP / FN: {default_metrics['tp']} / {default_metrics['tn']} / {default_metrics['fp']} / {default_metrics['fn']}

## 最优准确率阈值

- threshold: {best_metrics['threshold']:.6f}
- ACC: {best_metrics['acc']:.6f}
- RACC: {best_metrics['racc']:.6f}
- FACC: {best_metrics['facc']:.6f}
- TP / TN / FP / FN: {best_metrics['tp']} / {best_metrics['tn']} / {best_metrics['fp']} / {best_metrics['fn']}

## 分数分布摘要

- fake_mean: {bands['fake_mean']:.6f}
- fake_min: {bands['fake_min']:.6f}
- fake_max: {bands['fake_max']:.6f}
- real_mean: {bands['real_mean']:.6f}
- real_min: {bands['real_min']:.6f}
- real_max: {bands['real_max']:.6f}

## 简要结论

如果最优阈值相对 0.5 存在明显偏移，并且 `FACC` 在默认阈值下显著偏低，就说明当前问题更像是分数分布漂移与阈值校准，而不是模型完全失去区分能力。
"""
    write_summary(args.output_md, summary)
    print(f"Wrote calibration summary to {args.output_md}")


if __name__ == "__main__":
    main()
