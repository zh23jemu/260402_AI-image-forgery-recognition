# 第二阶段最小量化版服务器执行清单

## 1. 当前状态判断

上一轮 `run_joint_metadata_build.slurm` 的 `17856139` 作业结果为 `TIMEOUT`，并且没有生成：

```text
analysis/joint_training_metadata_stage2.csv
```

因此不能直接提交第二阶段训练。需要先用新的快速建表脚本重跑 metadata。

## 2. 已完成的代码侧调整

- `tools/build_joint_training_metadata.py`：改为快速扫描，并支持 `ADM/train` prompt-level 弱 `LVLM` 标签。
- `fsd/datasets/joint_metadata.py`：支持读取 `SP` 分数、`LVLM` 多标签、`lvlm_valid` 与 `lvlm_confidence`。
- `fsd/train_joint.py`：支持 `LVLM` 轻量辅助头、`lvlm_loss`、`valid_lvlm_samples` 和评估阶段 `lvlm_f1`。
- `run_joint_metadata_build.slurm`：已加入 `--max_files_per_generator_split 5000` 和 `--enable_adm_prompt_weak_lvlm`。
- `run_fsd_joint_stage2_min.slurm`：第二阶段最小量化训练脚本。

## 3. 服务器执行顺序

### 3.1 重新提交快速 metadata 构建

```bash
sbatch run_joint_metadata_build.slurm
```

### 3.2 查看 metadata 构建状态

```bash
sacct -j <JOBID> --format=JobID,State,ExitCode,Elapsed

grep -E "Scanned rows|Scanned [0-9]+ rows|Loaded score entries|Loaded LVLM entries|Output CSV|Traceback|Error|FAILED" \
  logs/joint_meta_<JOBID>.out logs/joint_meta_<JOBID>.err
```

### 3.3 检查第二阶段 metadata 是否可用

```bash
ls -lh analysis/joint_training_metadata_stage2.csv

./.venv/bin/python tools/check_joint_metadata.py \
  --metadata_csv analysis/joint_training_metadata_stage2.csv
```

如果输出中出现：

```text
READY=YES
train_rows_with_lvlm=<非零数字>
```

则可以提交第二阶段训练。

### 3.4 提交第二阶段最小量化训练

```bash
sbatch run_fsd_joint_stage2_min.slurm
```

### 3.5 训练中检查日志

```bash
squeue -u xj62kv

tail -f logs/fsd_joint_stage2_min_*.err
```

重点看：

```text
valid_lvlm_samples
steps_with_valid_lvlm
lvlm_loss
lvlm_f1
```

只要 `valid_lvlm_samples` 或 `steps_with_valid_lvlm` 出现非零值，就说明第二阶段 `LVLM` 辅助监督已经真实进入训练流程。

## 4. 训练结束后汇总结果

```bash
./.venv/bin/python tools/build_joint_stage2_result_summary.py \
  --log_glob "logs/fsd_joint_stage2_min_*.err" \
  --output_csv analysis/joint_stage2_min_result.csv \
  --output_md docs/joint_stage2_min_result.md
```

## 5. 论文口径

如果第二阶段训练正常完成，论文中可以写：

```text
本文进一步完成了第二阶段最小量化版训练，即在 FSD 主干与 Stay-Positive 离线分数约束基础上，引入 LVLM 结构化语义标签作为多标签辅助监督。训练日志中出现非零 valid_lvlm_samples，并在评估阶段输出 LVLM 辅助头 F1 指标，说明 LVLM 已经从后验案例分析工具进一步进入训练监督流程。该实验仍属于轻量量化验证，但已经足以支撑本文完整两阶段联合训练框架的可运行性。
```

