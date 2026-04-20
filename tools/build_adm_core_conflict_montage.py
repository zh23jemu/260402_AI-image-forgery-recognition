# -*- coding: utf-8 -*-
"""生成 ADM 核心冲突 Top12 案例拼图。"""

import argparse
import math
import os
from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw


def find_image(base_dir: str, case_index: int) -> Path:
    pattern = f"adm_core_conflict_{case_index:02d}_"
    for path in sorted(Path(base_dir).glob(f"{pattern}*")):
        return path
    raise FileNotFoundError(f"Image not found for pattern {pattern} in {base_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ADM core conflict montage.")
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--image_dir", required=True)
    parser.add_argument("--output_png", required=True)
    parser.add_argument("--top_k", type=int, default=12)
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv).head(args.top_k).copy()

    tile_w = 250
    tile_h = 250
    label_h = 44
    cols = 4
    rows = math.ceil(len(df) / cols)
    canvas = Image.new("RGB", (cols * tile_w, rows * (tile_h + label_h)), "white")
    draw = ImageDraw.Draw(canvas)

    for idx, row in df.reset_index(drop=True).iterrows():
        image_path = find_image(args.image_dir, idx + 1)
        img = Image.open(image_path).convert("RGB")
        img = img.resize((tile_w, tile_h))
        x = (idx % cols) * tile_w
        y = (idx // cols) * (tile_h + label_h)
        canvas.paste(img, (x, y))
        label = f"{row['case_id']}\n{row['sample_id']}"
        draw.rectangle([x, y + tile_h, x + tile_w, y + tile_h + label_h], fill=(248, 248, 248))
        draw.text((x + 8, y + tile_h + 6), label, fill=(20, 20, 20))

    os.makedirs(os.path.dirname(os.path.abspath(args.output_png)), exist_ok=True)
    canvas.save(args.output_png)
    print(f"Wrote montage to {args.output_png}")


if __name__ == "__main__":
    main()
