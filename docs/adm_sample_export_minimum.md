# ADM 样本级结果最小导出要求

## 1. 用途

这份文档用于说明：为了把首批 `ADM` 案例真正填实，服务器侧最少需要导出哪些信息。

## 2. 最低可用字段

每个候选样本至少需要下面这些字段：

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

## 3. 最推荐附带字段

如果服务器侧导出方便，建议再加：

- `case_type`
- `priority`
- `visual_note`
- `selected`

## 4. 最简单导出格式

最简单可用的表头如下：

```text
sample_id,image_path,ground_truth,official_fsd_prediction,official_fsd_score,fsd_finetune_v1_prediction,fsd_finetune_v1_score,fsd_finetune_v2_prediction,fsd_finetune_v2_score,stay_positive_prediction,stay_positive_score
```

## 5. 当前建议

如果一次性导出全部字段比较麻烦，那么最低要求是：

1. 先把 `image_path`
2. 再把三组 `FSD` 结论
3. 再把 `Stay-Positive` 结论

只要这几项到位，就已经可以开始正式填首批案例页。
