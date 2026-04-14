# ADM 候选样本收集说明

## 1. 目标

这份说明用于指导后续如何收集首批 `ADM` 候选样本，服务于 `LVLM` 小样本案例分析。

## 2. 首批目标数量

- 粗筛：`12` 到 `20` 个
- 精选：`6` 到 `8` 个

## 3. 优先收集的样本类型

1. 官方 `FSD`、首轮微调、第二轮保守微调结论不一致的样本
2. `FSD` 与 `Stay-Positive` 结论冲突的样本
3. 分数接近阈值的边界样本
4. 视觉上最像真实图像、人工也不容易直接判断的样本

## 4. 收集时至少记录的字段

- `image_path`
- `ground_truth`
- `official_fsd_prediction`
- `official_fsd_score`
- `fsd_finetune_v1_prediction`
- `fsd_finetune_v1_score`
- `fsd_finetune_v2_prediction`
- `fsd_finetune_v2_score`
- `stay_positive_prediction`
- `stay_positive_score`
- `visual_note`

## 5. 推荐执行顺序

1. 先按 `ADM` 分类收集路径
2. 再补三组 `FSD` 相关结论
3. 再补 `Stay-Positive` 结论
4. 最后根据视觉观察补 `visual_note`
5. 再决定哪些样本正式送入 `LVLM`

## 6. 目前最缺的原始信息

当前本地文档已经准备好，但要真正填实首批案例，仍需要从服务器补回下面这些样本级信息：

- 候选图片的真实 `image_path`
- 官方 `FSD` 对这些图片的预测结论或分数
- 首轮微调对这些图片的预测结论或分数
- 第二轮保守微调对这些图片的预测结论或分数
- `Stay-Positive` 对这些图片的预测结论或分数

如果暂时拿不到完整导出，最低也应先手工记录：

- `image_path`
- 三组 `FSD` 结论差异
- `Stay-Positive` 是否冲突
- 一句人工视觉备注
## 7. 当前建议

首批样本不追求多，只追求代表性。

最稳妥的做法是：

- 先收一批最能体现“首轮微调有效、第二轮未进一步改善”的样本
- 再用 `LVLM` 对这些样本做统一提示词分析
- 最终提炼成论文讨论部分可直接使用的 2 到 3 条观察结论
