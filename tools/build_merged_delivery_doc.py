from __future__ import annotations

from pathlib import Path


ROOT = Path(r"C:\Coding\260402_AI-image-forgery-recognition")
DOCS_DIR = ROOT / "docs"
OUT_PATH = DOCS_DIR / "项目交付总说明_合并版.md"


PREFERRED_FILES = [
    ROOT / "README.md",
    ROOT / "notes" / "download_links.md",
    DOCS_DIR / "源码与数据集说明.md",
]


def collect_source_docs() -> list[Path]:
    files: list[Path] = []
    for path in PREFERRED_FILES:
        if path.exists() and path.is_file():
            files.append(path)

    for path in sorted(DOCS_DIR.glob("*.md")):
        if path.name == OUT_PATH.name:
            continue
        if path in files:
            continue
        files.append(path)
    return files


def build_front_matter() -> str:
    return """# 项目交付总说明（合并版）

## 1. 文档用途

本文件是本项目的统一交付文档，用于替代分散的多个说明文件。

本文档包含以下内容：

- 项目总体说明
- 数据集来源与下载地址
- 使用 Python 直接进行训练、评估与联合训练的示例命令
- 原有 Markdown 文档的合并内容

## 2. 程序源码包说明

本次源码包为“纯代码交付版”，默认不包含以下内容：

- `slurm` 脚本
- 原始数据集
- 本地虚拟环境 `.venv`
- 日志、分析中间文件、渲染缓存
- 大模型权重与 checkpoint

## 3. 使用 Python 直接训练的推荐方式

### 3.1 FSD 单模型训练

单卡训练时，推荐直接使用项目本地 Python 调用 `torch.distributed.run`：

```powershell
.\\.venv\\Scripts\\python.exe -m torch.distributed.run --nproc_per_node=1 fsd\\train.py `
  --data_root data\\GenImage `
  --output_dir fsd\\output\\train_adm_python `
  --exclude_class ADM `
  --num_workers 8 `
  --seed 42 `
  --batch_size 16 `
  --lr 1e-4 `
  --total_training_steps 50000 `
  --save_interval 10000 `
  --eval_interval 10000 `
  --log_interval 1000 `
  --accumulation_steps 1 `
  --use_fp16 True `
  --pretrained_backbone False
```

如果需要在官方 checkpoint 基础上微调，可以补充：

```powershell
  --init_ckpt_path checkpoints\\fsd\\resnet50_exclude_adm_step[200000]_converted.pth
```

### 3.2 FSD 单模型评估

```powershell
.\\.venv\\Scripts\\python.exe fsd\\test.py `
  --data_root data\\GenImage `
  --test_class ADM `
  --ckpt_path checkpoints\\fsd\\resnet50_exclude_adm_step[200000]_converted.pth `
  --num_workers 0 `
  --seed 42 `
  --use_fp16 False `
  --output_dir fsd\\output\\eval_adm_python
```

### 3.3 第一阶段联合训练（FSD + Stay-Positive）

```powershell
.\\.venv\\Scripts\\python.exe -m torch.distributed.run --nproc_per_node=1 fsd\\train_joint.py `
  --data_root data\\GenImage `
  --output_dir fsd\\output\\joint_sp_stage1_python `
  --train_generators real,ADM,SD,Midjourney `
  --eval_generators ADM,SD,Midjourney `
  --metadata_csv analysis\\joint_training_metadata.csv `
  --exclude_class ADM `
  --num_workers 8 `
  --seed 42 `
  --batch_size 16 `
  --lr 1e-5 `
  --total_training_steps 10000 `
  --save_interval 5000 `
  --eval_interval 5000 `
  --log_interval 100 `
  --init_ckpt_path checkpoints\\fsd\\resnet50_exclude_adm_step[200000]_converted.pth `
  --use_fp16 True `
  --sp_loss_weight 0.3 `
  --sp_loss_type mse `
  --force_real_in_task True
```

### 3.4 第二阶段最小量化联合训练（FSD + LVLM）

在执行第二阶段前，先构建联合训练 metadata：

```powershell
.\\.venv\\Scripts\\python.exe tools\\build_joint_training_metadata.py `
  --data_root data\\GenImage `
  --output_csv analysis\\joint_training_metadata_stage2.csv `
  --adm_sample_export_csv analysis\\adm_sample_export.csv `
  --lvlm_structured_csv analysis\\lvlm_structured_supplement_cases.csv `
  --max_files_per_generator_split 5000 `
  --enable_adm_prompt_weak_lvlm
```

然后检查 metadata：

```powershell
.\\.venv\\Scripts\\python.exe tools\\check_joint_metadata.py `
  --metadata_csv analysis\\joint_training_metadata_stage2.csv
```

第二阶段训练命令：

```powershell
.\\.venv\\Scripts\\python.exe -m torch.distributed.run --nproc_per_node=1 fsd\\train_joint.py `
  --data_root data\\GenImage `
  --output_dir fsd\\output\\joint_stage2_min_python `
  --train_generators real,ADM,SD,Midjourney `
  --eval_generators ADM,SD,Midjourney `
  --metadata_csv analysis\\joint_training_metadata_stage2.csv `
  --exclude_class ADM `
  --num_workers 8 `
  --seed 42 `
  --batch_size 16 `
  --lr 1e-5 `
  --total_training_steps 10000 `
  --save_interval 5000 `
  --eval_interval 5000 `
  --log_interval 100 `
  --init_ckpt_path checkpoints\\fsd\\resnet50_exclude_adm_step[200000]_converted.pth `
  --use_fp16 True `
  --enable_lvlm_head True `
  --lvlm_loss_weight 0.2 `
  --lvlm_loss_on_fake_only True `
  --sp_loss_weight 0.0
```

训练完成后，可用下面的命令汇总第二阶段结果：

```powershell
.\\.venv\\Scripts\\python.exe tools\\build_joint_stage2_result_summary.py `
  --log_glob "logs\\fsd_joint_stage2_min_*.err" `
  --output_csv analysis\\joint_stage2_min_result.csv `
  --output_md docs\\joint_stage2_min_result.md
```

### 3.5 Stay-Positive 训练

在 `stay_positive\\training_code` 目录下可直接使用 Python 启动：

```powershell
cd stay_positive\\training_code
..\\..\\.venv\\Scripts\\python.exe train.py `
  --name latent_diffusion_text2img_train2 `
  --arch res50nodown `
  --cropSize 96 `
  --norm_type resnet `
  --resize_size 256 `
  --resize_ratio 0.75 `
  --blur_sig 0.0,3.0 `
  --cmp_method cv2,pil `
  --cmp_qual 30,100 `
  --resize_prob 0.2 `
  --jitter_prob 0.8 `
  --colordist_prob 0.2 `
  --cutout_prob 0.2 `
  --noise_prob 0.2 `
  --blur_prob 0.5 `
  --cmp_prob 0.5 `
  --rot90_prob 1.0 `
  --dataroot <Stay-Positive训练数据目录> `
  --batch_size 32 `
  --earlystop_epoch 10 `
  --use_inversions `
  --seed 17 `
  --batched_syncing
```

### 3.6 Stay-Positive 测试与打分

先把图片目录转成 CSV：

```powershell
cd stay_positive\\test_code
..\\..\\.venv\\Scripts\\python.exe create_csv.py `
  --base_folder "<图像目录>" `
  --output_csv "<输出CSV路径>"
```

再执行打分：

```powershell
..\\..\\.venv\\Scripts\\python.exe main.py `
  --in_csv "<输入CSV>" `
  --out_csv "<输出CSV>" `
  --device "cuda:0" `
  --weights_dir ".\\weights" `
  --models "corvi-plus,rajan-ours-plus"
```

## 4. 数据集与模型来源

### 4.1 GenImage

- 官方仓库：<https://github.com/GenImage-Dataset/GenImage>
- 论文地址：<https://arxiv.org/abs/2306.08571>
- Google Drive：<https://drive.google.com/drive/folders/1jGt10bwTbhEZuGXLyvrCuxOI0cBqQ1FS?usp=sharing>
- 百度网盘：见官方仓库 README，常用提取码 `ztf1`

### 4.2 FSD

- 官方仓库：<https://github.com/teheperinko541/Few-Shot-AIGI-Detector>
- 论文地址：<https://arxiv.org/abs/2501.08763>
- 官方 checkpoint：<https://pan.baidu.com/s/1zNxDKtFJ_5KXcMceNtrRqA?pwd=icml>
- 提取码：`icml`

### 4.3 Stay-Positive

- 官方仓库：<https://github.com/AniSundar18/AlignedForensics>
- 论文地址：<https://arxiv.org/abs/2502.07778>
- OpenReview：<https://openreview.net/forum?id=VNLmfMJi3w>
- 项目页：<https://anisundar18.github.io/Stay-Positive/>
- Robust LDM Benchmark：<https://huggingface.co/datasets/AniSundar18/Robust_LDM_Benchmark>
- LDMFakeDetect：<https://huggingface.co/datasets/AniSundar18/LDMFakeDetect>
- Corvi+：<https://drive.google.com/file/d/16Rp0G0Onbdmpm3xT2ZxTV6P13youB-kp/view?usp=sharing>
- Rajan/Ours+：<https://drive.google.com/file/d/14k9qakoIh36Z6U-fVHHjhvs667aywzfz/view?usp=sharing>

## 5. 合并文档目录

以下内容为项目中原有 Markdown 文档的合并结果。

---
"""


def build_merged_content() -> str:
    parts: list[str] = [build_front_matter()]
    source_docs = collect_source_docs()
    for idx, path in enumerate(source_docs, start=1):
        rel = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").strip()
        except Exception as exc:
            text = f"读取失败：{exc}"
        parts.append(f"\n## 合并文档 {idx}: `{rel}`\n")
        if text:
            parts.append(text)
        else:
            parts.append("（空文件）")
        parts.append("\n\n---\n")
    return "\n".join(parts)


def main() -> None:
    content = build_merged_content()
    OUT_PATH.write_text(content, encoding="utf-8")
    print(f"merged_doc_saved={OUT_PATH}")


if __name__ == "__main__":
    main()
