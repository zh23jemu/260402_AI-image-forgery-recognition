# ADM 实际候选样本工作记录

## 1. 用途

这份文档用于先把已经确认拿到的真实样本级结果落成“工作版案例记录”，避免实际案例还没整理就散在聊天记录里。

当前这份记录基于 `analysis/adm_sample_export.csv` 的前几条真实输出，后续可继续增补。

## 2. 当前已确认的实际候选样本

### 候选样本 A

```text
sample_id: adm_auto_0001
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/0_adm_153.PNG
ground_truth: fake

stay_positive_prediction: real
stay_positive_score: 0.44916382112305414

official_fsd_prediction: fake
official_fsd_score: 0.763671875
fsd_finetune_v1_prediction: fake
fsd_finetune_v1_score: 0.7783203125
fsd_finetune_v2_prediction: fake
fsd_finetune_v2_score: 0.65673828125

working_case_type: model_conflict
working_priority: high

working_reason:
1. 三组 FSD 结论一致为 fake，但 Stay-Positive 给出 real。
2. 这是非常典型的“FSD 与 Stay-Positive 证据冲突”样本。
3. 适合优先进入 LVLM 分析，看高层语义是否更支持 fake 还是 real。

paper_use:
可用于说明不同方法在 ADM 上可能依赖不同判别证据。
```

### 候选样本 B

```text
sample_id: adm_auto_0002
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/0_adm_174.PNG
ground_truth: fake

stay_positive_prediction: real
stay_positive_score: 0.44455618831720967

official_fsd_prediction: fake
official_fsd_score: 0.50537109375
fsd_finetune_v1_prediction: fake
fsd_finetune_v1_score: 0.537109375
fsd_finetune_v2_prediction: real
fsd_finetune_v2_score: 0.399169921875

working_case_type: v2_regression
working_priority: high

working_reason:
1. 官方 FSD 与首轮微调都判断为 fake，但第二轮保守微调回落为 real。
2. Stay-Positive 也判断为 real，因此这是一个“第二轮退化”非常明确的样本。
3. 适合用来说明第二轮更保守设置并未自动改善困难样本。

paper_use:
可用于支撑“首轮微调有效、第二轮保守微调未进一步改善”的训练探索结论。
```

### 候选样本 C

```text
sample_id: adm_auto_0003
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/0_adm_34.PNG
ground_truth: fake

stay_positive_prediction: real
stay_positive_score: 0.4201140705222974

official_fsd_prediction: fake
official_fsd_score: 0.865234375
fsd_finetune_v1_prediction: fake
fsd_finetune_v1_score: 0.74853515625
fsd_finetune_v2_prediction: fake
fsd_finetune_v2_score: 0.91015625

working_case_type: model_conflict
working_priority: high

working_reason:
1. 三组 FSD 都稳定判断为 fake，但 Stay-Positive 仍给出 real。
2. 说明这类样本在 FSD 主线和 Stay-Positive 主线之间存在稳定冲突。
3. 适合与候选样本 A 配对，形成一组“稳定冲突样本”。

paper_use:
可用于说明 LVLM 需要补充解释“为什么某些样本会让不同检测器稳定冲突”。
```

### 候选样本 D

```text
sample_id: adm_auto_0004
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/0_adm_7.PNG
ground_truth: fake

stay_positive_prediction: real
stay_positive_score: 0.41553325677724523

official_fsd_prediction: fake
official_fsd_score: 0.87353515625
fsd_finetune_v1_prediction: fake
fsd_finetune_v1_score: 0.8046875
fsd_finetune_v2_prediction: fake
fsd_finetune_v2_score: 0.88671875

working_case_type: model_conflict
working_priority: high

working_reason:
1. 三组 FSD 一致判 fake，但 Stay-Positive 判 real。
2. 这说明该类冲突并不是单点偶然现象，而可能是 ADM 中一类稳定模式。
3. 适合与样本 A、C 一起构成“稳定冲突簇”。

paper_use:
可用于说明 ADM 中存在一类对 FSD 与 Stay-Positive 证据链造成稳定分歧的样本。
```

## 3. 当前阶段判断

基于已拿到的前 4 条真实样本，可以先确认两点：

- `ADM` 中确实已经出现可直接进入 `LVLM` 的真实冲突样本
- 当前优先级最高的实际案例，不是“边界分数特别接近 0.5”的样本，而是“FSD 与 Stay-Positive 明显冲突、或第二轮退化明显”的样本

## 4. 下一步最值得补的两类样本

为了把首批 `6` 个案例补齐，下一步最值得从完整 `adm_sample_export.csv` 中继续筛：

1. 再补 `1` 到 `2` 个分数接近阈值的 `borderline_case`
2. 再补 `1` 个比样本 B 更典型的 `v2_regression`

## 5. 当前建议

就目前已知信息看，候选样本 A、B、C、D 都值得进入首批正式案例候选范围。
