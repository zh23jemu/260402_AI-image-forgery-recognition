# FSD 实验进展记录

## 2026-04-05

### Midjourney 评估

- 模型：FSD
- 测试类别：`Midjourney`
- 使用权重：`checkpoints/fsd/resnet50_exclude_midjourney_step[200000]_converted.pth`
- 数据目录：`data/GenImage`
- 运行环境：Slurm 单卡 `Tesla V100-PCIE-32GB`
- 评估样本数：`9000`
- Accuracy：`0.7955555319786072`
- Average Precision：`0.8203965425491333`
- 说明：已完成 FSD 在 `Midjourney` 数据上的首次有效评估，说明当前代码、数据、权重和服务器环境已经联通。

### SD 评估

- 模型：FSD
- 测试类别：`SD`
- 使用权重：`checkpoints/fsd/resnet50_exclude_sd_step[200000]_converted.pth`
- 数据目录：`data/GenImage`
- 运行环境：Slurm 单卡 `Tesla V100-PCIE-32GB`
- 评估样本数：`9000`
- Accuracy：`0.8834444284439087`
- Average Precision：`0.913029670715332`
- 说明：已完成 FSD 在 `SD` 数据上的第二条基线评估，结果优于 `Midjourney`，表明不同生成器类别上的检测难度存在差异。

### 当前结论

- FSD 基线已在 `Midjourney` 和 `SD` 两类数据上完成初步评估。
- `SD` 上的检测表现明显优于 `Midjourney`。
- 当前结果已经可以作为论文与周报中的“实验进展”与“基线复现结果”使用。

### Stay-Positive / Midjourney 评估

- 模型：Stay-Positive
- 测试数据：`real/val/nature` vs `Midjourney/val/ai`
- 使用权重：
  - `checkpoints/stay_positive/corvi-staypos.pth`
  - `checkpoints/stay_positive/rajan-staypos.pth`
- 运行环境：Slurm 单卡 `Tesla V100-PCIE-32GB`
- 评估方式：`create_csv.py -> main.py -> eval.py`
- `corvi-plus`
  - RACC：`0.9956666666666667`
  - FACC：`0.9963333333333333`
  - ACC：`0.996`
  - AP：`0.9998131520389307`
- `rajan-ours-plus`
  - RACC：`0.9976666666666667`
  - FACC：`0.9703333333333334`
  - ACC：`0.984`
  - AP：`0.9994048293285538`
- 说明：Stay-Positive 预训练模型已完成 `Midjourney` 数据上的首次有效验证，整体指标显著高于当前 FSD 在同类数据上的结果，其中 `corvi-plus` 表现最好。

### Stay-Positive / SD 评估

- 模型：Stay-Positive
- 测试数据：`real/val/nature` vs `SD/val/ai`
- 使用权重：
  - `checkpoints/stay_positive/corvi-staypos.pth`
  - `checkpoints/stay_positive/rajan-staypos.pth`
- 运行环境：Slurm 单卡 `Tesla V100-PCIE-32GB`
- 评估方式：`create_csv.py -> main.py -> eval.py`
- `corvi-plus`
  - RACC：`0.9956666666666667`
  - FACC：`1.0`
  - ACC：`0.9978333333333333`
  - AP：`1.0`
- `rajan-ours-plus`
  - RACC：`0.9976666666666667`
  - FACC：`1.0`
  - ACC：`0.9988333333333334`
  - AP：`1.0`
- 说明：Stay-Positive 在 `SD` 数据上的两种预训练模型均取得接近满分的结果，其中 `rajan-ours-plus` 略优于 `corvi-plus`。

### 下一步

- 将 `FSD` 与 `Stay-Positive` 在 `Midjourney`、`SD` 两类数据上的结果整理成统一对比表。
- 分析为何 `Stay-Positive` 在当前数据设置下显著优于 FSD，并讨论数据设定与任务定义差异。
- 继续准备后续方法整合与改进方案。
