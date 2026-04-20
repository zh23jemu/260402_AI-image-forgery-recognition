# -*- coding: utf-8 -*-
"""绘制 Stay-Positive / ADM 分数分布图。"""

import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot Stay-Positive ADM score bins.")
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--output_png", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)
    labels = df["score_bin"].tolist()
    real_count = df["real_count"].tolist()
    fake_count = df["fake_count"].tolist()
    x = range(len(labels))

    plt.figure(figsize=(13, 6))
    width = 0.42
    plt.bar([i - width / 2 for i in x], real_count, width=width, label="Real", color="#6b8fd6")
    plt.bar([i + width / 2 for i in x], fake_count, width=width, label="Fake", color="#d77a61")
    plt.axvline(x=2.5, color="#222222", linestyle="--", linewidth=1.2, label="Around calibrated threshold")
    plt.title("Stay-Positive / ADM score distribution")
    plt.xlabel("Score bin")
    plt.ylabel("Sample count")
    plt.xticks(list(x), labels, rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    os.makedirs(os.path.dirname(os.path.abspath(args.output_png)), exist_ok=True)
    plt.savefig(args.output_png, dpi=220)
    plt.close()
    print(f"Wrote plot to {args.output_png}")


if __name__ == "__main__":
    main()
