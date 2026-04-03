# GenImage 数据目录说明

此目录用于放置 GenImage 数据集。

当前阶段采用最小数据子集策略：

- 允许先只准备 `Stable Diffusion V1.4`
- 后续再按需要补充 `Stable Diffusion V1.5`、`Midjourney`、`VQDM` 等目录

说明：

- GenImage 原始数据通常按生成器分别组织，每个目录下包含 `train/ai`、`train/nature`、`val/ai`、`val/nature`。
- FSD README 中额外提到的 `real/` 目录，本质上来自 `stable_diffusion_v_1_4` 和 `stable_diffusion_v_1_5` 的 `nature` 图像整理。
- 当前阶段无需提前重排所有原始目录，先保留原始结构更稳。

下载入口见：

- [notes/download_links.md](/C:/Coding/260402_AI-image-forgery-recognition/notes/download_links.md)
