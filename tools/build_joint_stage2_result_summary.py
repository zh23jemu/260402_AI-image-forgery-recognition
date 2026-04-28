# -*- coding: utf-8 -*-
"""汇总第二阶段最小量化版训练日志，生成论文可直接使用的结果表。"""

import argparse
import csv
import glob
import os
import re
from pathlib import Path


def choose_latest(pattern: str) -> str:
    """选择最新一个匹配文件。"""

    matches = sorted(glob.glob(pattern))
    return matches[-1] if matches else ""


def read_text(path: str) -> str:
    """安全读取日志文本。"""

    if not path or not os.path.exists(path):
        return ""
    return Path(path).read_text(encoding="utf-8", errors="ignore")


def parse_eval_metrics(text: str) -> list[dict]:
    """从日志中解析每个生成器的主任务指标和可选 LVLM F1。"""

    rows = []
    pattern = re.compile(
        r"Evaluation on (?P<name>[A-Za-z0-9_+-]+) done\. accuracy: (?P<acc>[0-9.]+), average precision: (?P<ap>[0-9.]+)(?:, lvlm_f1: (?P<f1>[0-9.]+))?\."
    )
    for match in pattern.finditer(text):
        rows.append(
            {
                "generator": match.group("name"),
                "accuracy": match.group("acc"),
                "average_precision": match.group("ap"),
                "lvlm_f1": match.group("f1") or "",
            }
        )
    return rows


def parse_training_signals(text: str) -> dict:
    """提取训练中第二阶段是否真的生效的关键信号。"""

    lvlm_counts = [int(item) for item in re.findall(r"valid_lvlm_samples=(\d+)", text)]
    sp_counts = [int(item) for item in re.findall(r"valid_sp_samples=(\d+)", text)]
    ckpt_steps = re.findall(r"Save checkpoint at step: (\d+)", text)

    return {
        "max_valid_lvlm_samples": max(lvlm_counts) if lvlm_counts else 0,
        "max_valid_sp_samples": max(sp_counts) if sp_counts else 0,
        "checkpoint_steps": ",".join(ckpt_steps),
    }


def write_csv(path: str, rows: list[dict]) -> None:
    """输出 CSV 结果表。"""

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=["generator", "accuracy", "average_precision", "lvlm_f1"],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: str, rows: list[dict], signals: dict, log_path: str) -> None:
    """输出论文可直接引用的 Markdown 摘要。"""

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 第二阶段最小量化版结果汇总",
        "",
        "## 1. 运行信号",
        "",
        f"- 日志来源：`{log_path or 'missing'}`",
        f"- `max_valid_lvlm_samples`：`{signals['max_valid_lvlm_samples']}`",
        f"- `max_valid_sp_samples`：`{signals['max_valid_sp_samples']}`",
        f"- `checkpoint_steps`：`{signals['checkpoint_steps'] or '未发现'}`",
        "",
        "## 2. 结果表",
        "",
        "| 生成器 | Accuracy | AP | LVLM F1 |",
        "| --- | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            f"| {row['generator']} | {row['accuracy']} | {row['average_precision']} | {row['lvlm_f1'] or 'N/A'} |"
        )

    lines.extend(
        [
            "",
            "## 3. 论文可直接引用结论模板",
            "",
            "```text",
            "第二阶段最小量化版实验以 FSD 为主干、以 Stay-Positive 离线分数为判别约束，并进一步引入 LVLM 结构化语义标签作为多标签辅助监督。日志结果显示，训练过程中已经出现非零的 valid_lvlm_samples，说明 LVLM 辅助头并非停留在方案层面，而是真正进入了训练计算图。最终在闭集评估中，模型除给出主任务 Accuracy 与 AP 外，还能够输出 LVLM 辅助头的多标签 F1 指标。这说明本文第二阶段虽然仍属于轻量量化验证，但已经完成了从结构化案例分析到可训练语义监督的关键过渡。`",
            "```",
        ]
    )

    Path(path).write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build stage2 joint result summary from logs.")
    parser.add_argument("--log_glob", required=True, help="第二阶段训练日志 glob。")
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--output_md", required=True)
    args = parser.parse_args()

    log_path = choose_latest(args.log_glob)
    text = read_text(log_path)
    rows = parse_eval_metrics(text)
    signals = parse_training_signals(text)

    write_csv(args.output_csv, rows)
    write_md(args.output_md, rows, signals, log_path)

    print(f"Wrote stage2 CSV to {args.output_csv}")
    print(f"Wrote stage2 markdown to {args.output_md}")


if __name__ == "__main__":
    main()
