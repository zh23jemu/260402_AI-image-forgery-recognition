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

### 下一步

- 梳理 Stay-Positive 的最小运行入口，并尝试使用 `Corvi +` 与 `Rajan/Ours +` 进行测试。
- 将 `Midjourney` 与 `SD` 的结果整理进论文“实验进展”与“基线复现结果”部分。
- 对比 FSD 在不同生成器上的表现差异，为后续方法改进提供依据。
