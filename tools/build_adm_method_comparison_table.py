# -*- coding: utf-8 -*-
"""生成 ADM 方法综合对比表。"""

import argparse
import csv
import os
import re
from typing import Dict, List


def parse_calibration_md(path: str) -> Dict[str, float]:
    text = open(path, "r", encoding="utf-8").read()

    def extract(pattern: str) -> float:
        match = re.search(pattern, text)
        if not match:
            raise ValueError(f"Pattern not found: {pattern}")
        return float(match.group(1))

    return {
        "default_acc": extract(r"## 默认阈值 0\.5[\s\S]*?- ACC: ([0-9.]+)"),
        "default_racc": extract(r"## 默认阈值 0\.5[\s\S]*?- RACC: ([0-9.]+)"),
        "default_facc": extract(r"## 默认阈值 0\.5[\s\S]*?- FACC: ([0-9.]+)"),
        "best_threshold": extract(r"## 最优准确率阈值[\s\S]*?- threshold: ([0-9.]+)"),
        "best_acc": extract(r"## 最优准确率阈值[\s\S]*?- ACC: ([0-9.]+)"),
        "best_racc": extract(r"## 最优准确率阈值[\s\S]*?- RACC: ([0-9.]+)"),
        "best_facc": extract(r"## 最优准确率阈值[\s\S]*?- FACC: ([0-9.]+)"),
    }


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def write_csv(path: str, rows: List[Dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["method", "setting", "accuracy", "ap", "racc", "facc", "threshold", "note"],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: str, rows: List[Dict[str, str]], calibration: Dict[str, float]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    lines = [
        "# ADM 方法综合对比表",
        "",
        "| 方法 | 设置 | ACC | AP | RACC | FACC | 阈值 | 备注 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['method']} | {row['setting']} | {row['accuracy']} | {row['ap']} | {row['racc']} | {row['facc']} | {row['threshold']} | {row['note']} |"
        )
    lines.extend(
        [
            "",
            "## 简要结论",
            "",
            f"- `FSD` 官方基线当前仍是 `ADM` 上最稳的参考点，结果为 `75.41% / 79.34%`。",
            f"- `FSD` 首轮微调达到 `75.28% / 78.54%`，明显优于从零初始化训练，但仍略低于官方基线。",
            f"- `FSD` 第二轮保守微调回落到 `74.13% / 76.89%`，说明更保守设置未继续改善。",
            f"- `Stay-Positive` 在默认阈值 `0.5` 下仅有 `ACC={pct(calibration['default_acc'])}`，但这主要由阈值失配导致。",
            f"- 将 `Stay-Positive` 阈值调整到 `0.388818` 后，整体准确率可提升到 `ACC={pct(calibration['best_acc'])}`，说明其在 `ADM` 上存在显著校准问题，而不是完全失效。",
        ]
    )
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ADM method comparison table.")
    parser.add_argument("--calibration_md", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--output_md", required=True)
    args = parser.parse_args()

    calibration = parse_calibration_md(args.calibration_md)

    rows = [
        {
            "method": "FSD",
            "setting": "官方基线",
            "accuracy": "75.41%",
            "ap": "79.34%",
            "racc": "-",
            "facc": "-",
            "threshold": "-",
            "note": "当前 ADM 官方参考结果",
        },
        {
            "method": "FSD",
            "setting": "首轮微调",
            "accuracy": "75.28%",
            "ap": "78.54%",
            "racc": "-",
            "facc": "-",
            "threshold": "-",
            "note": "当前最佳训练探索结果",
        },
        {
            "method": "FSD",
            "setting": "第二轮保守微调",
            "accuracy": "74.13%",
            "ap": "76.89%",
            "racc": "-",
            "facc": "-",
            "threshold": "-",
            "note": "未进一步改善，反而回落",
        },
        {
            "method": "Stay-Positive",
            "setting": "默认阈值 0.5",
            "accuracy": pct(calibration["default_acc"]),
            "ap": "87.58%",
            "racc": pct(calibration["default_racc"]),
            "facc": pct(calibration["default_facc"]),
            "threshold": "0.500000",
            "note": "默认阈值下明显失配",
        },
        {
            "method": "Stay-Positive",
            "setting": "校准后阈值",
            "accuracy": pct(calibration["best_acc"]),
            "ap": "87.58%",
            "racc": pct(calibration["best_racc"]),
            "facc": pct(calibration["best_facc"]),
            "threshold": f"{calibration['best_threshold']:.6f}",
            "note": "显示显著校准收益",
        },
    ]

    write_csv(args.output_csv, rows)
    write_md(args.output_md, rows, calibration)
    print(f"Wrote ADM comparison CSV to {args.output_csv}")
    print(f"Wrote ADM comparison markdown to {args.output_md}")


if __name__ == "__main__":
    main()
