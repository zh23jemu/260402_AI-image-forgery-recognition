# ADM 样本级结果导出运行说明

## 1. 用途

这份说明用于指导如何在服务器上导出：

- 官方 `FSD` 的 `ADM` 样本级结果
- 首轮微调 `FSD` 的 `ADM` 样本级结果
- 第二轮保守微调 `FSD` 的 `ADM` 样本级结果
- 最终统一合并为一个 `adm_sample_export.csv`

## 2. 推荐方式：直接提交 slurm 任务

如果登录节点没有 GPU，最推荐直接提交：

```bash
sbatch run_adm_sample_export.slurm
```

跑完后检查：

```bash
tail -f logs/adm_sample_export_*.out logs/adm_sample_export_*.err
ls -lh analysis/adm_*.csv
head -5 analysis/adm_sample_export.csv
```

## 3. 手动方式：逐步导出官方 FSD 样本级结果

在服务器项目根目录执行：

```bash
mkdir -p analysis
cd fsd
../.venv/bin/python export_sample_scores.py \
  --data_root ../data/GenImage \
  --test_class ADM \
  --ckpt_path ../checkpoints/fsd/resnet50_exclude_adm_step[200000]_converted.pth \
  --output_csv ../analysis/adm_official_fsd.csv \
  --num_support 5 \
  --query_batch_size 64 \
  --use_fp16 True
```

## 4. 第二步：导出首轮微调样本级结果

请把 `CKPT_PATH` 改成首轮微调实际产出的 checkpoint 路径，例如：

```bash
cd fsd
../.venv/bin/python export_sample_scores.py \
  --data_root ../data/GenImage \
  --test_class ADM \
  --ckpt_path ./output/finetune_adm_stage1/ckpt/resnet50_step[10000].pth \
  --output_csv ../analysis/adm_finetune_v1.csv \
  --num_support 5 \
  --query_batch_size 64 \
  --use_fp16 True
```

## 5. 第三步：导出第二轮保守微调样本级结果

请把 `CKPT_PATH` 改成第二轮实际产出的 checkpoint 路径，例如：

```bash
cd fsd
../.venv/bin/python export_sample_scores.py \
  --data_root ../data/GenImage \
  --test_class ADM \
  --ckpt_path ./output/finetune_adm_stage2/ckpt/resnet50_step[5000].pth \
  --output_csv ../analysis/adm_finetune_v2.csv \
  --num_support 5 \
  --query_batch_size 64 \
  --use_fp16 True
```

## 6. 第四步：合并 Stay-Positive 与 FSD

回到项目根目录执行：

```bash
./.venv/bin/python tools/build_adm_sample_export.py \
  --official_csv analysis/adm_official_fsd.csv \
  --finetune_v1_csv analysis/adm_finetune_v1.csv \
  --finetune_v2_csv analysis/adm_finetune_v2.csv \
  --stay_positive_val_csv stay_positive_runs/adm_val.csv \
  --stay_positive_scores_csv stay_positive_runs/adm_scores.csv \
  --stay_positive_model rajan-ours-plus \
  --output_csv analysis/adm_sample_export.csv
```

## 7. 最终产物

最终最关键的文件是：

```text
analysis/adm_sample_export.csv
```

这个文件一旦同步回本地，就可以开始正式填写：

- `docs/lvlm_adm_case_screening_sheet.md`
- `docs/lvlm_adm_case_batch1_template.md`

## 8. 当前建议

如果服务器登录节点没有 GPU，就不要在登录节点直接跑 `cuda` 导出。

最稳妥的顺序是：

1. 直接 `sbatch run_adm_sample_export.slurm`
2. 等导出完成
3. 检查 `analysis/adm_sample_export.csv`
4. 再同步回本地开始填案例
