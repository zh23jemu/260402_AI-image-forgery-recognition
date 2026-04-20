# -*- coding: utf-8 -*-
"""绘制 ADM 方法对比图。"""

import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd


def percent_to_float(value: str) -> float:
    return float(str(value).replace("%", "").strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot ADM method comparison.")
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--output_png", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv).copy()
    setting_map = {
        "官方基线": "Official",
        "首轮微调": "Finetune-v1",
        "第二轮保守微调": "Finetune-v2",
        "默认阈值": "Default-0.5",
        "默认阈值 0.5": "Default-0.5",
        "校准后阈值": "Calibrated",
    }
    method_map = {
        "FSD": "FSD",
        "Stay-Positive": "Stay-Positive",
    }
    df["label"] = df.apply(
        lambda row: f"{method_map.get(str(row['method']), str(row['method']))}\n{setting_map.get(str(row['setting']), str(row['setting']))}",
        axis=1,
    )
    df["accuracy_float"] = df["accuracy"].map(percent_to_float)
    df["ap_float"] = df["ap"].map(percent_to_float)

    x = range(len(df))
    width = 0.38

    plt.figure(figsize=(11, 6))
    plt.bar([i - width / 2 for i in x], df["accuracy_float"], width=width, label="Accuracy", color="#3d6ea8")
    plt.bar([i + width / 2 for i in x], df["ap_float"], width=width, label="AP", color="#d28b36")
    plt.title("ADM method comparison")
    plt.ylabel("Percentage")
    plt.xticks(list(x), df["label"].tolist(), rotation=18, ha="right")
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()

    os.makedirs(os.path.dirname(os.path.abspath(args.output_png)), exist_ok=True)
    plt.savefig(args.output_png, dpi=220)
    plt.close()
    print(f"Wrote plot to {args.output_png}")


if __name__ == "__main__":
    main()
