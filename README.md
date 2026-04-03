# AI伪造图像识别研究初稿工作区

本目录用于同时整理两部分内容：

1. 论文初稿：以 `FSD + Stay-Positive` 为主线，形成可继续扩展的中文初稿。
2. 代码初稿：保留两篇论文的官方实现，先完成目录规划、数据/权重放置规则和最小运行说明。

当前阶段的默认策略如下：

- 使用公开论文、官方代码、预训练模型和公开数据入口作为基础。
- 第一阶段不重新训练，先做基线建立与流程准备。
- `LVLM` 暂时不作为当前主线，仅保留为后续扩展方向。
- `GenImage` 当前仅按最小数据子集准备，可先从 `Stable Diffusion V1.4` 开始。

目录说明：

- [docs/paper_draft.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/paper_draft.md)：论文初稿正文。
- [docs/code_baseline_plan.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/code_baseline_plan.md)：代码准备与运行方案。
- [docs/fusion_design.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/fusion_design.md)：FSD 与 Stay-Positive 的联合设计说明。
- [notes/download_links.md](/C:/Coding/260402_AI-image-forgery-recognition/notes/download_links.md)：代码、数据、预训练模型下载入口整理。
- [fsd/README.md](/C:/Coding/260402_AI-image-forgery-recognition/fsd/README.md)：FSD 官方代码落位说明。
- [stay_positive/README.md](/C:/Coding/260402_AI-image-forgery-recognition/stay_positive/README.md)：Stay-Positive 官方代码落位说明。

说明：

- 本次实现没有直接修改 `123.docx`，因为它是二进制 Word 文件，不适合做可追踪的文本版本编辑。
- 已将可编辑初稿落为 Markdown，后续你可以据此继续扩展或再转换到 Word。
- 官方仓库在线克隆在当前网络环境下失败，因此先完成了可交付的文稿与代码准备骨架。
