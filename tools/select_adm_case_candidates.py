# -*- coding: utf-8 -*-
"""Select ADM case candidates from the merged sample export."""

import argparse
import os

import pandas as pd


def classify_row(row):
    predictions = [
        row["official_fsd_prediction"],
        row["fsd_finetune_v1_prediction"],
        row["fsd_finetune_v2_prediction"],
        row["stay_positive_prediction"],
    ]
    unique_predictions = len(set(predictions))

    if row["fsd_finetune_v1_prediction"] == "fake" and row["fsd_finetune_v2_prediction"] == "real":
        return "v2_regression"
    if unique_predictions >= 3:
        return "multi_conflict"
    if unique_predictions == 2 and row["stay_positive_prediction"] != row["official_fsd_prediction"]:
        return "model_conflict"
    if min(
        abs(float(row["official_fsd_score"]) - 0.5),
        abs(float(row["fsd_finetune_v1_score"]) - 0.5),
        abs(float(row["fsd_finetune_v2_score"]) - 0.5),
    ) < 0.05:
        return "borderline_case"
    return "stable_case"


def priority_score(row):
    disagreement = len(
        set(
            [
                row["official_fsd_prediction"],
                row["fsd_finetune_v1_prediction"],
                row["fsd_finetune_v2_prediction"],
                row["stay_positive_prediction"],
            ]
        )
    )
    closeness = min(
        abs(float(row["official_fsd_score"]) - 0.5),
        abs(float(row["fsd_finetune_v1_score"]) - 0.5),
        abs(float(row["fsd_finetune_v2_score"]) - 0.5),
    )
    return disagreement * 10 - closeness


def main():
    parser = argparse.ArgumentParser(description="Select ADM case candidates.")
    parser.add_argument("--input_csv", type=str, required=True)
    parser.add_argument("--output_csv", type=str, required=True)
    parser.add_argument("--top_k", type=int, default=20)
    args = parser.parse_args()

    frame = pd.read_csv(args.input_csv).copy()
    frame["case_hint"] = frame.apply(classify_row, axis=1)
    frame["priority_score"] = frame.apply(priority_score, axis=1)

    filtered = frame[
        frame["case_hint"].isin(["v2_regression", "multi_conflict", "model_conflict", "borderline_case"])
    ].copy()
    filtered = filtered.sort_values(by=["priority_score"], ascending=False).head(args.top_k)

    os.makedirs(os.path.dirname(os.path.abspath(args.output_csv)), exist_ok=True)
    filtered.to_csv(args.output_csv, index=False)
    print(f"Selected {len(filtered)} candidate rows into {args.output_csv}")


if __name__ == "__main__":
    main()
