# AI伪造图像识别研究工作区

本目录当前同时服务三部分工作：

1. 论文主稿：以 `FSD + Stay-Positive + LVLM` 为整体框架，形成可提交的中文初稿。
2. 基线实验：保留官方实现，维护当前已跑通的 `FSD`、`Stay-Positive` 与 `ADM` 训练探索结果链路。
3. 案例分析：围绕 `ADM` 误判样本、冲突样本和边界样本，推进 `LVLM` 小样本定性分析。

当前阶段的默认策略如下：

- 使用公开论文、官方代码、预训练模型和公开数据入口作为基础。
- 论文口径已统一为 `FSD + Stay-Positive + LVLM` 三线结构。
- `LVLM` 已纳入本次论文整体研究框架，当前以方法分析、案例设计和轻量验证方式推进。
- `ADM` 训练探索已经完成到“首轮微调正结果 + 第二轮保守微调负结果”的收束状态。
- 当前默认不继续无边界追加训练，而是优先做结果分析与 `LVLM` 案例补充。

当前优先参考文档：

- [docs/full_paper_draft.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/full_paper_draft.md)：当前论文主稿。
- [docs/document_map.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/document_map.md)：全部关键文档导航。
- [docs/project_schedule_to_20260425.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/project_schedule_to_20260425.md)：当前整体推进计划。
- [docs/experiment_results_summary.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/experiment_results_summary.md)：当前统一结果总表。
- [docs/final_submission_draft.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/final_submission_draft.md)：对外提交/汇报版摘要。
- [docs/experiment_progress.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/experiment_progress.md)：当前实验进展总览。
- [docs/lvlm_adm_case_screening_sheet.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/lvlm_adm_case_screening_sheet.md)：`ADM` 候选样本筛选页。
- [docs/lvlm_adm_case_batch1_template.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/lvlm_adm_case_batch1_template.md)：首批正式案例记录页。
- [docs/lvlm_execution_checklist.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/lvlm_execution_checklist.md)：`LVLM` 落地清单。

当前训练相关入口：

- [fsd/scripts/train.sh](/C:/Coding/260402_AI-image-forgery-recognition/fsd/scripts/train.sh)：可配置的 FSD 训练脚本。
- [run_fsd_finetune_adm.slurm](/C:/Coding/260402_AI-image-forgery-recognition/run_fsd_finetune_adm.slurm)：首轮微调脚本，对应当前最佳训练探索结果。
- [run_fsd_finetune_adm_v2.slurm](/C:/Coding/260402_AI-image-forgery-recognition/run_fsd_finetune_adm_v2.slurm)：第二轮保守微调脚本，用于负结果验证。

说明：

- 当前论文、计划、`LVLM` 文书和训练探索说明已经统一到 Markdown 文档中，便于后续持续维护。
- 当前最自然的下一步不是立即重启训练，而是先完成 `ADM + LVLM` 小样本案例分析。
- 只有在案例分析和论文收束之后，仍然明确存在新增训练收益时，才考虑下一步训练。
