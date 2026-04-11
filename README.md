# AI伪造图像识别研究工作区

本目录当前同时服务三部分工作：

1. 论文主稿：以 `FSD + Stay-Positive + LVLM` 为整体框架，形成可提交的中文初稿。
2. 基线实验：保留官方实现，维护当前已跑通的 `FSD` 与 `Stay-Positive` 结果链路。
3. 下一步训练：以 `FSD` 为主干，进入最小改进训练准备与执行阶段。

当前阶段的默认策略如下：

- 使用公开论文、官方代码、预训练模型和公开数据入口作为基础。
- 论文口径已统一为 `FSD + Stay-Positive + LVLM` 三线结构。
- `LVLM` 已纳入本次论文整体研究框架，当前以方法分析、案例设计和轻量验证方式推进。
- 当前代码主线已从“只做基线准备”进入“可直接开始最小训练”的阶段。
- 下一步训练默认优先选择 `FSD` 主干做最小改进训练，再决定是否扩展到更复杂方案。

当前优先参考文档：

- [docs/full_paper_draft.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/full_paper_draft.md)：当前论文主稿。
- [docs/project_schedule_to_20260425.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/project_schedule_to_20260425.md)：当前整体推进计划。
- [docs/experiment_results_summary.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/experiment_results_summary.md)：当前统一结果总表。
- [docs/fusion_design.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/fusion_design.md)：主干 + 增强 + LVLM 辅助分析的设计说明。
- [docs/next_stage_training_plan.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/next_stage_training_plan.md)：下一步最小训练方案。
- [docs/training_ready_checklist.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/training_ready_checklist.md)：训练前检查清单。
- [notes/download_links.md](/C:/Coding/260402_AI-image-forgery-recognition/notes/download_links.md)：代码、数据、预训练模型下载入口整理。
- [fsd/README.md](/C:/Coding/260402_AI-image-forgery-recognition/fsd/README.md)：FSD 官方代码落位说明。
- [stay_positive/README.md](/C:/Coding/260402_AI-image-forgery-recognition/stay_positive/README.md)：Stay-Positive 官方代码落位说明。

当前训练入口：

- [fsd/scripts/train.sh](/C:/Coding/260402_AI-image-forgery-recognition/fsd/scripts/train.sh)：可配置的 FSD 训练脚本。
- [run_fsd_train_adm.slurm](/C:/Coding/260402_AI-image-forgery-recognition/run_fsd_train_adm.slurm)：首个推荐训练提交脚本。

说明：

- 本次实现没有直接修改 `123.docx`，因为它是二进制 Word 文件，不适合做可追踪的文本版本编辑。
- 当前论文、计划、LVLM 文书和训练入口已经统一到 Markdown 文档中，便于后续持续维护。
- 下一步如果直接进入训练，默认先从 `FSD / ADM` 最小训练开始，再根据结果决定是否扩展。
