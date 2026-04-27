# -*- coding: utf-8 -*-
"""生成闭集协议下 FSD-only 与 FSD+SP 的结果对比表。"""

import argparse
import csv
import glob
import os
import re
from typing import Dict, List, Optional, Tuple


# 说明：
# 1. 本脚本优先从服务器日志中自动抽取 ADM / SD / Midjourney 三类结果；
# 2. 如果某一组日志暂时还没有跑完，则允许保留为 pending，占位输出半成品表格；
# 3. 这样可以保证训练一结束后，只需重跑一次脚本，就能迅速得到最终对比表。


TARGET_GENERATORS = ["ADM", "SD", "Midjourney"]


def pct(value: Optional[float]) -> str:
    """把 0-1 浮点数格式化为百分比字符串；空值输出占位。"""
    if value is None:
        return "pending"
    return f"{value * 100:.2f}%"


def resolve_log_paths(patterns: List[str]) -> List[str]:
    """展开 glob 模式，并按路径排序，便于稳定选择最新日志。"""
    paths: List[str] = []
    for pattern in patterns:
        paths.extend(glob.glob(pattern))
    return sorted(set(paths))


def choose_latest_file(paths: List[str]) -> Optional[str]:
    """从候选日志中选最后一个，用于处理同名批次多次提交的情况。"""
    if not paths:
        return None
    return sorted(paths)[-1]


def read_text(path: str) -> str:
    """统一读取文本文件。"""
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        return handle.read()


def parse_eval_metrics(text: str) -> Dict[str, Dict[str, float]]:
    """从日志中提取每个生成器的 Accuracy / AP。"""
    metrics: Dict[str, Dict[str, float]] = {}
    pattern = re.compile(
        r"Evaluation on (?P<name>[A-Za-z0-9_+-]+) done\.(?: evaluating num: \d+,)? accuracy: (?P<acc>[0-9.]+), average precision: (?P<ap>[0-9.]+)",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        name = match.group("name")
        metrics[name] = {
            "accuracy": float(match.group("acc")),
            "ap": float(match.group("ap")),
        }
    return metrics


def parse_checkpoint_steps(text: str) -> List[str]:
    """从日志中抽取 checkpoint 保存步数，便于写入备注。"""
    steps = re.findall(r"Save checkpoint at step: (\d+)", text)
    return steps


def detect_failed(text: str) -> bool:
    """粗略判断日志里是否出现训练失败信号。"""
    failure_keywords = ["Traceback", "FAILED", "ChildFailedError", "RuntimeError", "Error:"]
    return any(keyword in text for keyword in failure_keywords)


def parse_one_run(
    out_patterns: List[str],
    err_patterns: List[str],
) -> Dict[str, object]:
    """解析一组训练运行的日志结果。"""
    out_path = choose_latest_file(resolve_log_paths(out_patterns))
    err_path = choose_latest_file(resolve_log_paths(err_patterns))

    out_text = read_text(out_path) if out_path and os.path.exists(out_path) else ""
    err_text = read_text(err_path) if err_path and os.path.exists(err_path) else ""
    merged_text = "\n".join([out_text, err_text])

    metrics = parse_eval_metrics(merged_text)
    ckpt_steps = parse_checkpoint_steps(merged_text)
    failed = detect_failed(merged_text)

    return {
        "out_path": out_path,
        "err_path": err_path,
        "metrics": metrics,
        "checkpoint_steps": ckpt_steps,
        "failed": failed,
    }


def build_rows(
    base_run: Dict[str, object],
    joint_run: Dict[str, object],
) -> List[Dict[str, str]]:
    """构造宽表行，便于同时输出 CSV 和 Markdown。"""
    rows: List[Dict[str, str]] = []

    base_metrics: Dict[str, Dict[str, float]] = base_run["metrics"]  # type: ignore[assignment]
    joint_metrics: Dict[str, Dict[str, float]] = joint_run["metrics"]  # type: ignore[assignment]

    for generator in TARGET_GENERATORS:
        base_item = base_metrics.get(generator, {})
        joint_item = joint_metrics.get(generator, {})
        base_acc = base_item.get("accuracy")
        base_ap = base_item.get("ap")
        joint_acc = joint_item.get("accuracy")
        joint_ap = joint_item.get("ap")

        acc_delta = None
        ap_delta = None
        if base_acc is not None and joint_acc is not None:
            acc_delta = joint_acc - base_acc
        if base_ap is not None and joint_ap is not None:
            ap_delta = joint_ap - base_ap

        # 中文备注帮助用户在结果一出来后快速判断是否值得写成正向增益。
        if base_acc is None:
            note = "FSD-only 结果待补齐"
        elif joint_acc is None:
            note = "FSD+SP 结果缺失，请检查日志"
        elif acc_delta is not None and acc_delta > 0.01:
            note = "联合训练相对 FSD-only 有明显正向增益"
        elif acc_delta is not None and acc_delta >= -0.01:
            note = "两者接近，需谨慎表述 SP 约束增益"
        else:
            note = "当前类别未体现联合训练优势"

        rows.append(
            {
                "generator": generator,
                "fsd_only_acc": pct(base_acc),
                "fsd_only_ap": pct(base_ap),
                "fsd_sp_acc": pct(joint_acc),
                "fsd_sp_ap": pct(joint_ap),
                "delta_acc": pct(acc_delta) if acc_delta is not None else "pending",
                "delta_ap": pct(ap_delta) if ap_delta is not None else "pending",
                "note": note,
            }
        )
    return rows


def write_csv(path: str, rows: List[Dict[str, str]]) -> None:
    """写出 CSV 对比表。"""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "generator",
                "fsd_only_acc",
                "fsd_only_ap",
                "fsd_sp_acc",
                "fsd_sp_ap",
                "delta_acc",
                "delta_ap",
                "note",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def build_summary_lines(
    base_run: Dict[str, object],
    joint_run: Dict[str, object],
    rows: List[Dict[str, str]],
) -> List[str]:
    """生成 Markdown 总结内容。"""
    base_failed = bool(base_run["failed"])
    joint_failed = bool(joint_run["failed"])
    base_steps = ", ".join(base_run["checkpoint_steps"]) if base_run["checkpoint_steps"] else "未发现"
    joint_steps = ", ".join(joint_run["checkpoint_steps"]) if joint_run["checkpoint_steps"] else "未发现"

    lines = [
        "# 闭集联合训练对比表",
        "",
        "## 1. 当前说明",
        "",
        "- 本表用于对比同一闭集协议下的 `FSD-only` 与 `FSD + Stay-Positive`。",
        "- 当前协议训练集合包含 `real`、`ADM`、`SD`、`Midjourney`，因此不能直接与历史 `exclude-ADM` 开放协议结果混用。",
        f"- `FSD-only` 日志状态：{'检测到失败信号' if base_failed else '未检测到失败信号'}。",
        f"- `FSD + SP` 日志状态：{'检测到失败信号' if joint_failed else '未检测到失败信号'}。",
        f"- `FSD-only` checkpoint 步数：{base_steps}。",
        f"- `FSD + SP` checkpoint 步数：{joint_steps}。",
        "",
        "## 2. 结果总表",
        "",
        "| 生成器 | FSD-only ACC | FSD-only AP | FSD+SP ACC | FSD+SP AP | ACC 差值 | AP 差值 | 备注 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            f"| {row['generator']} | {row['fsd_only_acc']} | {row['fsd_only_ap']} | {row['fsd_sp_acc']} | {row['fsd_sp_ap']} | {row['delta_acc']} | {row['delta_ap']} | {row['note']} |"
        )

    lines.extend(
        [
            "",
            "## 3. 结论模板",
            "",
            "### 3.1 如果 FSD+SP 整体优于 FSD-only",
            "",
            "- 可以表述为：在相同闭集训练协议、相同初始化 checkpoint 与相同训练步数下，引入 `Stay-Positive` 辅助约束后，模型在目标生成器上取得了更高的准确率与平均精度，说明该辅助监督对第一阶段联合训练具有实际增益。",
            "",
            "### 3.2 如果两者差距较小",
            "",
            "- 可以表述为：当前结果首先说明闭集训练框架本身是有效的，而 `Stay-Positive` 约束的附加收益暂时有限；因此第一阶段更适合作为联合训练可行性验证，而不是直接宣称显著性能突破。",
            "",
            "### 3.3 如果不同类别表现不一致",
            "",
            "- 可以表述为：`Stay-Positive` 辅助约束呈现出类别选择性收益，在部分生成器上提供明显帮助，但在另一些类别上的增益仍不稳定，这说明后续仍需结合类别特征进一步设计联合损失。",
            "",
            "## 4. 日志来源",
            "",
            f"- FSD-only out: `{base_run['out_path'] or 'missing'}`",
            f"- FSD-only err: `{base_run['err_path'] or 'missing'}`",
            f"- FSD+SP out: `{joint_run['out_path'] or 'missing'}`",
            f"- FSD+SP err: `{joint_run['err_path'] or 'missing'}`",
        ]
    )
    return lines


def write_md(
    path: str,
    base_run: Dict[str, object],
    joint_run: Dict[str, object],
    rows: List[Dict[str, str]],
) -> None:
    """写出 Markdown 对比表和结论模板。"""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    lines = build_summary_lines(base_run, joint_run, rows)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))


def split_patterns(raw: str) -> List[str]:
    """支持逗号分隔多个 glob 模式。"""
    return [item.strip() for item in raw.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build closed-set joint training comparison table.")
    parser.add_argument(
        "--base_out_glob",
        default="logs/fsd_joint_base_stage1_*.out",
        help="FSD-only 训练 out 日志 glob，可用逗号分隔多个模式。",
    )
    parser.add_argument(
        "--base_err_glob",
        default="logs/fsd_joint_base_stage1_*.err",
        help="FSD-only 训练 err 日志 glob，可用逗号分隔多个模式。",
    )
    parser.add_argument(
        "--joint_out_glob",
        default="logs/fsd_joint_sp_stage1_*.out",
        help="FSD+SP 训练 out 日志 glob，可用逗号分隔多个模式。",
    )
    parser.add_argument(
        "--joint_err_glob",
        default="logs/fsd_joint_sp_stage1_*.err",
        help="FSD+SP 训练 err 日志 glob，可用逗号分隔多个模式。",
    )
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--output_md", required=True)
    args = parser.parse_args()

    base_run = parse_one_run(
        out_patterns=split_patterns(args.base_out_glob),
        err_patterns=split_patterns(args.base_err_glob),
    )
    joint_run = parse_one_run(
        out_patterns=split_patterns(args.joint_out_glob),
        err_patterns=split_patterns(args.joint_err_glob),
    )

    rows = build_rows(base_run=base_run, joint_run=joint_run)
    write_csv(args.output_csv, rows)
    write_md(args.output_md, base_run, joint_run, rows)

    print(f"Wrote closed-set comparison CSV to {args.output_csv}")
    print(f"Wrote closed-set comparison markdown to {args.output_md}")


if __name__ == "__main__":
    main()
