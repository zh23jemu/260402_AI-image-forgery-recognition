# 下一步建议

## 1. 当前判断

当前文书层面的主要收束工作已经基本完成，训练探索也已经收束到可写入论文的稳定状态。

因此，下一步不应再默认继续追加微调训练，而应先转入：

- `ADM` 误判样本整理
- `LVLM` 小样本案例分析
- 论文讨论与结论部分补强

## 2. 当前默认主线

- 默认优先工作对象：`ADM`
- 默认优先工作类型：结果分析与案例补充
- 默认优先方法组合：`FSD + Stay-Positive + LVLM`

这样安排的原因是：

- 首轮微调已经提供了当前最佳训练探索结果
- 第二轮保守微调未进一步改善 `ADM`
- 继续盲目调参的边际收益已经明显下降
- 当前更缺的是“为什么这些困难样本仍然困难”的解释材料

## 3. 现在最应该做的事

1. 先按 [lvlm_adm_case_screening_sheet.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/lvlm_adm_case_screening_sheet.md) 粗筛 `ADM` 候选样本
2. 再按 [adm_sample_export_minimum.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/adm_sample_export_minimum.md) 准备服务器侧样本级结果
3. 再按 [lvlm_adm_batch1_assignment.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/lvlm_adm_batch1_assignment.md) 固定首批 `6` 个案例
4. 然后按 [lvlm_adm_case_batch1_template.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/lvlm_adm_case_batch1_template.md) 开始正式记录
5. 最后把案例结论压缩进论文讨论部分

## 4. 什么时候才值得进入下一步训练

只有在满足下面至少一条时，才值得重启训练：

- `LVLM` 案例分析已经完成，论文讨论部分仍明显缺少新增实验支撑
- 已经从误判样本里识别出非常明确、可直接针对的失败模式
- 已经能提出比“继续调小学习率”更具体的训练改动

## 5. 当前建议

当前最稳妥的推进方式是：

- 先把分析线做完
- 再决定是否真的需要下一步训练

而不是一边文书未收束、一边继续滚动训练。
