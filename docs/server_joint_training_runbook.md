# 服务器执行版命令清单

## 1. 目标

本清单用于在服务器上完成三模型联合训练第一版最小闭环。

当前第一版目标不是直接做完整的 `FSD + Stay-Positive + LVLM` 全量联合，
而是先完成：

- 联合元数据生成
- `FSD + Stay-Positive` 联合训练
- 后续评估与结果对比准备

## 2. 当前默认服务器环境

以下命令默认基于当前项目服务器路径：

```bash
/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition
```

并默认使用项目本地虚拟环境：

```bash
./.venv/bin/python
./.venv/bin/torchrun
```

## 3. 先检查关键文件是否到位

在登录节点先执行：

```bash
cd /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition

ls fsd/train_joint.py
ls fsd/datasets/joint_metadata.py
ls tools/build_joint_training_metadata.py
ls analysis/adm_sample_export_enriched.csv
```

如果这些文件都存在，说明代码骨架已经到位。

## 4. 检查训练数据目录

先确认以下目录存在：

```bash
ls data/GenImage/real/train
ls data/GenImage/real/val
ls data/GenImage/ADM/train
ls data/GenImage/ADM/val
ls data/GenImage/SD/train
ls data/GenImage/SD/val
ls data/GenImage/Midjourney/train
ls data/GenImage/Midjourney/val
```

如果这些目录不全，联合训练先不要启动。

## 5. 生成联合元数据

### 5.1 直接命令版

如果你想先交互式跑一遍，可直接执行：

```bash
cd /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition

./.venv/bin/python tools/build_joint_training_metadata.py \
  --data_root data/GenImage \
  --output_csv analysis/joint_training_metadata.csv \
  --generators real,ADM,SD,Midjourney \
  --splits train,val \
  --sp_score_csv analysis/adm_sample_export_enriched.csv \
  --priority_fake_generators ADM
```

### 5.2 推荐 `slurm` 版

推荐直接提交：

```bash
sbatch run_joint_metadata_build.slurm
```

## 6. 检查元数据输出

元数据生成后，检查：

```bash
head -5 analysis/joint_training_metadata.csv
wc -l analysis/joint_training_metadata.csv
```

重点确认：

- 文件不是空表
- 有 `sp_prob_calibrated`
- 有 `hard_weight`

## 7. 启动第一版联合训练

当前推荐的第一版训练范围：

- `real`
- `ADM`
- `SD`
- `Midjourney`

训练脚本已经准备为：

- `fsd/train_joint.py`

推荐直接提交：

```bash
sbatch run_fsd_joint_sp_stage1.slurm
```

## 8. 查看训练日志

提交后可用：

```bash
squeue -u xj62kv
tail -f logs/fsd_joint_sp_stage1_*.out logs/fsd_joint_sp_stage1_*.err
```

重点关注日志中是否出现：

- `Loaded joint metadata rows`
- `Metadata CSV`
- `sp_loss`
- `valid_sp_samples`
- `Evaluation on ADM done`

## 9. 训练完成后先看什么

训练完成后，第一时间检查：

```bash
ls -lh fsd/output/joint_sp_stage1/ckpt
grep -E "Evaluation on|Save checkpoint|sp_loss|total_loss|FAILED|Traceback|Error" logs/fsd_joint_sp_stage1_*.out logs/fsd_joint_sp_stage1_*.err
```

## 10. 第一版结果该怎么比较

第一版至少和以下三组比较：

1. `FSD official`
2. `FSD finetune`
3. `FSD + SP`

重点先看：

- `ADM`
- `SD`
- `Midjourney`

## 11. 如果训练没有跑起来，优先排查什么

优先检查：

1. 元数据路径是否正确
2. 元数据是否真的匹配到训练图片
3. `data_root` 是否正确
4. checkpoint 路径是否存在
5. `train_joint.py` 是否打印了 `valid_sp_samples`

## 12. 当前最推荐的执行顺序

现在最稳的顺序是：

1. `sbatch run_joint_metadata_build.slurm`
2. 检查 `analysis/joint_training_metadata.csv`
3. `sbatch run_fsd_joint_sp_stage1.slurm`
4. 看日志
5. 确认 checkpoint 和第一版结果

只要这一步跑出来，项目就从“只有基线复刻”真正进入“联合训练验证”阶段了。
