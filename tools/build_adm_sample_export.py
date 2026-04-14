# -*- coding: utf-8 -*-
"""Build a unified ADM sample export from FSD and Stay-Positive outputs."""

import argparse
import math
import os

import pandas as pd


def sigmoid(value):
    return 1.0 / (1.0 + math.exp(-float(value)))


def load_fsd_csv(path, prefix):
    frame = pd.read_csv(path)
    frame = frame[frame["ground_truth"] == "fake"].copy()
    frame = frame.rename(
        columns={
            "filename": "image_path",
            "pred_label": f"{prefix}_prediction",
            "prob_fake": f"{prefix}_score",
        }
    )
    keep_columns = ["image_path", f"{prefix}_prediction", f"{prefix}_score"]
    return frame[keep_columns]


def load_stay_positive(val_csv, scores_csv, model_name):
    val_frame = pd.read_csv(val_csv).rename(columns={"filename": "image_path", "typ": "ground_truth"})
    score_frame = pd.read_csv(scores_csv).rename(columns={"filename": "image_path"})
    merged = val_frame.merge(score_frame[["image_path", model_name]], on="image_path", how="inner")
    merged["stay_positive_score"] = merged[model_name].map(sigmoid)
    merged["stay_positive_prediction"] = merged["stay_positive_score"].map(
        lambda value: "fake" if value >= 0.5 else "real"
    )
    return merged[["image_path", "ground_truth", "stay_positive_prediction", "stay_positive_score"]]


def main():
    parser = argparse.ArgumentParser(description="Build unified ADM sample export.")
    parser.add_argument("--official_csv", type=str, required=True)
    parser.add_argument("--finetune_v1_csv", type=str, required=True)
    parser.add_argument("--finetune_v2_csv", type=str, required=True)
    parser.add_argument("--stay_positive_val_csv", type=str, required=True)
    parser.add_argument("--stay_positive_scores_csv", type=str, required=True)
    parser.add_argument("--stay_positive_model", type=str, default="rajan-ours-plus")
    parser.add_argument("--output_csv", type=str, required=True)
    args = parser.parse_args()

    official = load_fsd_csv(args.official_csv, "official_fsd")
    finetune_v1 = load_fsd_csv(args.finetune_v1_csv, "fsd_finetune_v1")
    finetune_v2 = load_fsd_csv(args.finetune_v2_csv, "fsd_finetune_v2")
    stay_positive = load_stay_positive(
        args.stay_positive_val_csv,
        args.stay_positive_scores_csv,
        args.stay_positive_model,
    )

    merged = stay_positive.merge(official, on="image_path", how="inner")
    merged = merged.merge(finetune_v1, on="image_path", how="inner")
    merged = merged.merge(finetune_v2, on="image_path", how="inner")
    merged = merged.reset_index(drop=True)
    merged.insert(0, "sample_id", [f"adm_auto_{idx + 1:04d}" for idx in range(len(merged))])

    os.makedirs(os.path.dirname(os.path.abspath(args.output_csv)), exist_ok=True)
    merged.to_csv(args.output_csv, index=False)
    print(f"Exported merged ADM sample file to {args.output_csv} ({len(merged)} rows)")


if __name__ == "__main__":
    main()
