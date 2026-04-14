# ADM 案例填写顺序说明

## 1. 用途

这份文档用于说明后续填 `ADM` 案例时，先填什么、后填什么，避免一上来就把所有字段都堆在一起。

## 2. 推荐顺序

### 第一步：先补最稳定的信息

先补这些字段：

- `sample_id`
- `image_path`
- `ground_truth`
- `case_type`

这些信息只要样本一确定，就应该先写进去。

### 第二步：再补模型结论

接着补：

- `official_fsd_prediction`
- `official_fsd_score`
- `fsd_finetune_v1_prediction`
- `fsd_finetune_v1_score`
- `fsd_finetune_v2_prediction`
- `fsd_finetune_v2_score`
- `stay_positive_prediction`
- `stay_positive_score`

这一步的目标是把“模型之间到底哪里不一致”先固定下来。

### 第三步：再补人工观察

然后补：

- `visual_note`
- `candidate_reason`
- `priority`

这一步的目标是回答“为什么这张图值得拿给 LVLM 看”。

### 第四步：最后补 LVLM 结果

只有在前面都齐了之后，再补：

- `prompt_type`
- `lvlm_prompt`
- `lvlm_raw_output_summary`
- `paper_ready_summary`
- `human_takeaway`

## 3. 每步完成标准

### 第一步完成标准

- 已经能唯一定位样本
- 已经明确这张图属于哪一类案例

### 第二步完成标准

- 已经可以看出哪些模型结论一致、哪些不一致
- 已经能判断这张图是否真的有讨论价值

### 第三步完成标准

- 已经能用一句话解释“为什么选它”
- 已经能判断它更适合写在论文讨论部分还是后续工作部分

### 第四步完成标准

- 已经能提炼出 1 到 2 句可直接进论文的话

## 4. 当前建议

后续真正开始填时，不要追求一次填完。

最稳妥的做法是：

1. 先把 `6` 个案例的前两步补齐
2. 再从里面挑出最值得做 `LVLM` 的 `3` 个优先推进
3. 最后再把完整 `LVLM` 输出补齐
