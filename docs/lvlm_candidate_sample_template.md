# LVLM 候选样本清单模板

## 1. 用途

这份模板用于后续从 `FSD`、`Stay-Positive` 现有结果中筛选 `LVLM` 分析候选样本。

建议先把候选样本都记到这里，再决定最终进入论文的案例。

## 2. 使用原则

- 先广泛收集，再精选
- 优先保留“有代表性”的样本，而不是单纯追求数量
- 最终正式进入论文的案例建议控制在 `6` 到 `12` 个

## 3. 字段说明

建议每条候选样本至少记录以下字段：

- `sample_id`
- `image_path`
- `generator_type`
- `ground_truth`
- `case_source`
- `official_fsd_prediction`
- `official_fsd_score`
- `fsd_prediction`
- `fsd_score`
- `fsd_finetune_v1_prediction`
- `fsd_finetune_v1_score`
- `fsd_finetune_v2_prediction`
- `fsd_finetune_v2_score`
- `stay_positive_prediction`
- `stay_positive_score`
- `candidate_reason`
- `priority`
- `selected_for_lvlm`
- `notes`

其中：

- `case_source` 建议取值：
  - `fsd_misclassified`
  - `model_conflict`
  - `borderline_case`
  - `other`
- `priority` 建议取值：
  - `high`
  - `medium`
  - `low`
- `selected_for_lvlm` 建议取值：
  - `yes`
  - `no`
  - `pending`

## 4. Markdown 表格模板

| sample_id | image_path | generator_type | ground_truth | case_source | official_fsd_prediction | official_fsd_score | fsd_finetune_v1_prediction | fsd_finetune_v1_score | fsd_finetune_v2_prediction | fsd_finetune_v2_score | stay_positive_prediction | stay_positive_score | candidate_reason | priority | selected_for_lvlm | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sample_001 | 待填写 | ADM | fake | fsd_misclassified | real | 待填写 | fake | 待填写 | real | 待填写 | fake | 待填写 | 官方与两轮微调结论不稳，适合解释 | high | pending | 待补截图或人工备注 |
| sample_002 | 待填写 | ADM | fake | model_conflict | fake | 待填写 | fake | 待填写 | fake | 待填写 | real | 待填写 | FSD 与 Stay-Positive 结论冲突，适合做解释 | high | pending | 待补 |
| sample_003 | 待填写 | ADM | fake | borderline_case | fake | 待填写 | fake | 待填写 | fake | 待填写 | fake | 待填写 | 分数接近阈值，适合边界分析 | medium | pending | 待补 |

## 5. CSV 表头模板

后续如果要转成 CSV，可直接使用下面这一行：

```text
sample_id,image_path,generator_type,ground_truth,case_source,official_fsd_prediction,official_fsd_score,fsd_finetune_v1_prediction,fsd_finetune_v1_score,fsd_finetune_v2_prediction,fsd_finetune_v2_score,stay_positive_prediction,stay_positive_score,candidate_reason,priority,selected_for_lvlm,notes
```

## 6. 推荐筛选顺序

建议按下面顺序填这个模板：

1. 先填 `ADM` 中官方基线、首轮微调、第二轮微调结论不一致或都不稳定的样本
2. 再填 `FSD` 与 `Stay-Positive` 结论冲突的样本
3. 最后补充边界样本

## 7. 当前建议

第一次筛样时，建议：

- 先收集 `15` 到 `20` 个候选样本
- 再从中精选 `6` 到 `12` 个进入 `LVLM` 正式分析

这样更容易保证最终案例质量。
