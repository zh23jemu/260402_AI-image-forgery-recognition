"""Convert official FSD checkpoints into plain state_dict checkpoints.

This script should only be used with trusted checkpoints downloaded from the
official FSD release. It loads the original checkpoint with dill support and
re-saves only the model state dict plus minimal metadata, which avoids repeated
PyTorch weights_only compatibility issues during evaluation.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import dill
import torch


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, help="Path to the original FSD checkpoint")
    parser.add_argument("--dst", required=True, help="Path to write the converted checkpoint")
    args = parser.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)
    dst.parent.mkdir(parents=True, exist_ok=True)

    checkpoint = torch.load(
        src,
        map_location="cpu",
        weights_only=False,
        pickle_module=dill,
    )

    if "model" not in checkpoint:
        raise KeyError(f'Key "model" not found in checkpoint: {src}')

    converted = {
        "model": checkpoint["model"],
    }

    for key in ("step", "epoch", "effective_step"):
        if key in checkpoint:
            converted[key] = checkpoint[key]

    torch.save(converted, dst)
    print(f"converted: {src} -> {dst}")


if __name__ == "__main__":
    main()
