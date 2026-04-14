# -*- coding: utf-8 -*-
"""Export sample-level FSD scores for case analysis."""

import argparse
import csv
import os
import warnings

import dill
import timm
import torch
from PIL import Image, UnidentifiedImageError
from einops import rearrange
from torch.amp import autocast
from torchvision import transforms
from torchvision.datasets import ImageFolder

from model.prototypical_utils import compute_prototypical_loss
from util.utils import load_model


def str2bool(value):
    if isinstance(value, bool):
        return value
    value = value.lower()
    if value in ("yes", "true", "t", "y", "1"):
        return True
    if value in ("no", "false", "f", "n", "0"):
        return False
    raise argparse.ArgumentTypeError(f"Unsupported bool value: {value}")


def resolve_data_root(data_root):
    if os.path.isabs(data_root) and os.path.exists(data_root):
        return data_root

    candidates = [
        os.path.abspath(data_root),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", data_root)),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "GenImage")),
    ]

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return os.path.abspath(data_root)


class ValidatedPathImageFolder(ImageFolder):
    def __init__(self, root, transform=None):
        super().__init__(root, transform=transform)
        valid_samples = []
        for path, target in self.samples:
            try:
                with Image.open(path) as image:
                    image.verify()
                valid_samples.append((path, target))
            except (UnidentifiedImageError, OSError) as exc:
                warnings.warn(f"Skip unreadable image during export scan: {path} ({exc})")

        self.samples = valid_samples
        self.imgs = valid_samples
        self.targets = [target for _, target in valid_samples]

    def __getitem__(self, index):
        path, target = self.samples[index]
        sample = self.loader(path)
        if self.transform is not None:
            sample = self.transform(sample)
        if self.target_transform is not None:
            target = self.target_transform(target)
        return sample, target, path


def build_dataset(folder_path):
    transform = transforms.Compose([
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ])
    return ValidatedPathImageFolder(folder_path, transform=transform)


def robust_load_model(ckpt_path, model):
    try:
        load_model(ckpt_path, model=model)
        return "weights_only"
    except Exception as exc:
        warnings.warn(
            f"Standard weights-only loading failed for {ckpt_path} ({exc}). "
            "Falling back to dill-based full checkpoint loading."
        )

    checkpoint = torch.load(
        ckpt_path,
        map_location="cpu",
        pickle_module=dill,
        weights_only=False,
    )

    if "model" in checkpoint:
        model.load_state_dict(checkpoint["model"])
        return "dill_checkpoint:model"

    if "state_dict" in checkpoint:
        model.load_state_dict(checkpoint["state_dict"])
        return "dill_checkpoint:state_dict"

    raise KeyError(
        f"Unable to find model weights in checkpoint {ckpt_path}. "
        "Expected key 'model' or 'state_dict'."
    )


def collect_support(dataset, num_support):
    support_tensors = []
    support_paths = []
    for index in range(min(num_support, len(dataset))):
        tensor, _, path = dataset[index]
        support_tensors.append(tensor)
        support_paths.append(path)
    return support_tensors, support_paths


def export_scores(args):
    data_root = resolve_data_root(args.data_root)
    requested_device = args.device
    if requested_device.startswith("cuda") and not torch.cuda.is_available():
        warnings.warn("CUDA is unavailable. Falling back to CPU for sample export.")
        requested_device = "cpu"
    device = torch.device(requested_device)
    use_fp16 = bool(args.use_fp16 and device.type == "cuda")

    real_dataset = build_dataset(os.path.join(data_root, "real", "val"))
    fake_dataset = build_dataset(os.path.join(data_root, args.test_class, "val"))

    if len(real_dataset) < args.num_support or len(fake_dataset) < args.num_support:
        raise ValueError("Not enough samples to build support sets.")

    real_support, real_support_paths = collect_support(real_dataset, args.num_support)
    fake_support, fake_support_paths = collect_support(fake_dataset, args.num_support)

    model = timm.create_model("resnet50", pretrained=False, num_classes=1024)
    load_mode = robust_load_model(args.ckpt_path, model=model)
    model = model.to(device).eval()
    print(f"Loaded checkpoint {args.ckpt_path} via mode: {load_mode}")

    max_queries = min(len(real_dataset), len(fake_dataset))
    rows = []

    with torch.no_grad():
        for start in range(0, max_queries, args.query_batch_size):
            end = min(start + args.query_batch_size, max_queries)
            query_size = end - start

            real_query_tensors = []
            real_query_paths = []
            fake_query_tensors = []
            fake_query_paths = []

            for index in range(start, end):
                real_tensor, _, real_path = real_dataset[index]
                fake_tensor, _, fake_path = fake_dataset[index]
                real_query_tensors.append(real_tensor)
                real_query_paths.append(real_path)
                fake_query_tensors.append(fake_tensor)
                fake_query_paths.append(fake_path)

            real_stack = torch.stack(real_support + real_query_tensors, dim=0)
            fake_stack = torch.stack(fake_support + fake_query_tensors, dim=0)
            batch_data = torch.stack([real_stack, fake_stack], dim=0).to(device)
            batch_data = rearrange(batch_data, "n b c h w -> (n b) c h w")

            labels = torch.arange(0, 2, device=device).repeat(query_size)

            with autocast(enabled=use_fp16, device_type=device.type):
                outputs = model(batch_data)
            outputs = rearrange(outputs, "(n b) l -> 1 b n l", n=2)

            _, scores = compute_prototypical_loss(outputs, labels, args.num_support)
            probs = scores.softmax(dim=-1).cpu()
            scores = scores.cpu()

            for offset in range(query_size):
                real_row_index = 2 * offset
                fake_row_index = 2 * offset + 1

                real_prob = probs[real_row_index]
                fake_prob = probs[fake_row_index]
                real_score = scores[real_row_index]
                fake_score = scores[fake_row_index]

                rows.append({
                    "filename": real_query_paths[offset],
                    "ground_truth": "real",
                    "pred_label": "fake" if int(real_prob.argmax().item()) == 1 else "real",
                    "prob_real": float(real_prob[0].item()),
                    "prob_fake": float(real_prob[1].item()),
                    "score_real": float(real_score[0].item()),
                    "score_fake": float(real_score[1].item()),
                    "support_real_paths": "|".join(real_support_paths),
                    "support_fake_paths": "|".join(fake_support_paths),
                })
                rows.append({
                    "filename": fake_query_paths[offset],
                    "ground_truth": "fake",
                    "pred_label": "fake" if int(fake_prob.argmax().item()) == 1 else "real",
                    "prob_real": float(fake_prob[0].item()),
                    "prob_fake": float(fake_prob[1].item()),
                    "score_real": float(fake_score[0].item()),
                    "score_fake": float(fake_score[1].item()),
                    "support_real_paths": "|".join(real_support_paths),
                    "support_fake_paths": "|".join(fake_support_paths),
                })

    os.makedirs(os.path.dirname(os.path.abspath(args.output_csv)), exist_ok=True)
    with open(args.output_csv, "w", newline="", encoding="utf-8") as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=[
                "filename",
                "ground_truth",
                "pred_label",
                "prob_real",
                "prob_fake",
                "score_real",
                "score_fake",
                "support_real_paths",
                "support_fake_paths",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} sample-level rows to {args.output_csv}")


def main():
    parser = argparse.ArgumentParser(description="Export sample-level FSD scores.")
    parser.add_argument("--data_root", type=str, default="../data/GenImage")
    parser.add_argument("--test_class", type=str, default="ADM")
    parser.add_argument("--ckpt_path", type=str, required=True)
    parser.add_argument("--output_csv", type=str, required=True)
    parser.add_argument("--num_support", type=int, default=5)
    parser.add_argument("--query_batch_size", type=int, default=64)
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--use_fp16", type=str2bool, default=True)
    args = parser.parse_args()
    export_scores(args)


if __name__ == "__main__":
    main()
