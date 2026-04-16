# -*- coding: utf-8 -*-
"""根据案例 CSV 导出图片同步命令清单。"""

import argparse
import csv
import os
from pathlib import Path
from typing import Dict, List


def load_rows(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_name(row: Dict[str, str]) -> str:
    source = Path(row["image_path"]).name
    case_id = row.get("case_id") or row.get("sample_id") or "sample"
    return f"{case_id}_{source}"


def build_markdown(rows: List[Dict[str, str]], local_dir: str, remote_project_dir: str) -> str:
    lines = [
        "# 图片同步命令清单",
        "",
        f"本地目标目录：`{local_dir}`",
        "",
        "## 1. 服务器侧复制命令",
        "",
        "```bash",
        f"mkdir -p {local_dir.replace('analysis', 'analysis')}",
    ]
    for row in rows:
        lines.append(f"cp {row['image_path']} {local_dir}/{safe_name(row)}")
    lines.append("```")
    lines.extend([
        "",
        "## 2. 服务器侧打包命令",
        "",
        "```bash",
        f"mkdir -p {local_dir}",
    ])
    for row in rows:
        lines.append(f"cp {row['image_path']} {local_dir}/{safe_name(row)}")
    tar_parent = str(Path(local_dir).parent).replace("\\", "/")
    tar_name = f"{Path(local_dir).name}.tar.gz"
    lines.append(f"tar -czf {tar_parent}/{tar_name} -C {tar_parent} {Path(local_dir).name}")
    lines.append("```")
    lines.extend([
        "",
        "## 3. Windows 本地建议落点",
        "",
        f"```text\n{local_dir}\n```",
        "",
        "## 4. 当前图片列表",
        "",
        "| case_id | sample_id | server_image_path | local_filename |",
        "| --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row.get('case_id','')} | {row.get('sample_id','')} | {row['image_path']} | {safe_name(row)} |"
        )
    if remote_project_dir:
        lines.extend(
            [
                "",
                "## 5. 备注",
                "",
                f"- 若在服务器项目根目录 `{remote_project_dir}` 下执行，建议把图片放入 `{local_dir}` 对应的相对目录后再打包。",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export image sync commands from a case CSV.")
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--local_dir", required=True)
    parser.add_argument("--output_md", required=True)
    parser.add_argument("--remote_project_dir", default="")
    args = parser.parse_args()

    rows = load_rows(args.input_csv)
    os.makedirs(args.local_dir, exist_ok=True)
    content = build_markdown(rows, args.local_dir.replace("\\", "/"), args.remote_project_dir)
    os.makedirs(os.path.dirname(os.path.abspath(args.output_md)), exist_ok=True)
    with open(args.output_md, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    print(f"Wrote sync commands to {args.output_md}")


if __name__ == "__main__":
    main()
