# ADM 样本筛选清单

## 1. 文档用途

这份清单用于把 `ADM` 相关的 `LVLM` 案例筛选工作落成一个可直接填写的执行页。

它主要服务三个目的：

- 为 `LVLM` 小样本案例分析准备候选样本
- 为论文中的“误判样本分析”准备统一素材
- 把官方基线、首轮微调、第二轮保守微调三组结论放到同一张表里比较

## 2. 当前筛选原则

- 优先选 `ADM`
- 优先选结论不稳定的样本
- 优先选肉眼不容易直接判断的样本
- 优先选能体现“首轮微调有效但第二轮未进一步改善”的样本

## 3. 优先级定义

### 高优先级

- 官方基线、首轮微调、第二轮保守微调中至少两者结论不同
- `FSD` 与 `Stay-Positive` 结论冲突
- 图像具有明显语义异常或局部结构可疑点

### 中优先级

- 多个模型都判断为假，但分数接近边界
- 多个模型都判断为真，但人工观察仍觉得可疑
- 适合拿来解释“为什么模型会犹豫”

### 低优先级

- 模型结论一致且分数非常稳定
- 即使加入 `LVLM` 也很难提升论文讨论价值

## 4. 建议先收的 8 类样本

1. 官方基线判错、首轮微调判对、第二轮又判错的样本
2. 官方基线判对、首轮和第二轮都判错的样本
3. 三者都判错，但 `Stay-Positive` 分数排序较强的样本
4. 首轮微调与第二轮保守微调结论冲突的样本
5. `FSD` 与 `Stay-Positive` 明显冲突的样本
6. 预测分数接近阈值的边界样本
7. 局部结构违和明显但模型分数不极端的样本
8. 视觉上高质量、最像真实图像的困难样本

## 5. 建议首批数量

- 先粗筛 `12` 到 `20` 个候选
- 再精选 `6` 个正式送入 `LVLM`

## 6. 首批记录表

| sample_id | image_path | ground_truth | official_fsd_prediction | official_fsd_score | fsd_finetune_v1_prediction | fsd_finetune_v1_score | fsd_finetune_v2_prediction | fsd_finetune_v2_score | stay_positive_prediction | stay_positive_score | case_type | priority | candidate_reason | visual_note | selected |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| adm_case_001 | 待填写 | fake | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | fsd_misclassified | high | 典型误判样本，适合说明 FSD 在 ADM 上仍存在难例 | 优先选视觉上较自然的假图 | pending |
| adm_case_002 | 待填写 | fake | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | fsd_misclassified | high | 首轮微调后仍不稳定，适合说明训练收益边界 | 优先选微调后仍容易出错的假图 | pending |
| adm_case_003 | 待填写 | fake | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | model_conflict | high | FSD 与 Stay-Positive 结论冲突，适合解释关注证据差异 | 优先选人工也觉得难判的样本 | pending |
| adm_case_004 | 待填写 | fake | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | model_conflict | high | 冲突样本，用于补足“不同模型为何矛盾” | 优先选两类证据都存在的样本 | pending |
| adm_case_005 | 待填写 | fake | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | borderline_case | medium | 边界样本，适合说明仅依赖分数不够 | 优先选分数接近阈值的假图 | pending |
| adm_case_006 | 待填写 | fake | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | borderline_case | medium | 第二轮保守微调未改善的代表案例 | 优先选最能体现“参数调小也没解决”的样本 | pending |

## 7. 推荐填写顺序

1. 先补 `image_path`、`ground_truth`
2. 再补三组 `FSD` 相关结论
3. 再补 `Stay-Positive` 结论
4. 最后写 `visual_note` 和 `selected`

## 8. 当前建议

当前不需要一开始就做很多样本。

最稳妥的做法是：

- 先把 `ADM` 的 `6` 个强代表性案例筛出来
- 先完成一轮 `LVLM` 定性分析
- 再决定是否扩到 `VQDM` 或其他类别
