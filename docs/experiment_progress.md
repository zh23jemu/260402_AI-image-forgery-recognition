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

### 下一步

- 转换 `resnet50_exclude_sd_step[200000].pth` 为纯权重版 checkpoint。
- 使用 `SD` 作为测试类别继续跑第二条基线评估。
- 将 `Midjourney` 与后续 `SD` 的结果整理进论文“实验进展”与“基线复现结果”部分。
