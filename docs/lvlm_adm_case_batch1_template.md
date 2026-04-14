# ADM 首批案例记录页

## 1. 用途

这份文档用于记录首批正式进入 `LVLM` 分析的 `ADM` 案例。

建议首批只保留 `6` 个高代表性样本，先形成一组可写入论文的小闭环。

## 2. 当前分配建议

- `2` 个 `fsd_misclassified`
- `2` 个 `model_conflict`
- `2` 个 `borderline_case`

## 3. 填写说明

当前这份文档已经把每个案例的作用、推荐提示词类型、论文落点和预期观察点预填好了。

后续真正需要补的主要是：

- `image_path`
- 各模型结论与分数
- `LVLM` 输出摘要
- 基于真实案例的最终总结句

## 4. 案例 1

```text
sample_id: adm_case_001
image_path: 待从服务器补
ground_truth: fake
case_type: fsd_misclassified

official_fsd_prediction: 待填写
official_fsd_score: 待填写
fsd_finetune_v1_prediction: 待填写
fsd_finetune_v1_score: 待填写
fsd_finetune_v2_prediction: 待填写
fsd_finetune_v2_score: 待填写
stay_positive_prediction: 待填写
stay_positive_score: 待填写

visual_note: 重点挑选视觉上较自然、但 FSD 仍会出错的假图。

prompt_type: base
lvlm_prompt: 使用“基础分析模板”，重点观察局部结构异常与整体语义一致性。

lvlm_raw_output_summary:
1. 重点看人物/物体/背景关系是否协调。
2. 重点看局部纹理、边缘和反射是否存在违和。
3. 记录 LVLM 是否能指出传统分数无法直接解释的可疑点。

final_judgement: 待基于真实案例填写

paper_ready_summary: 该案例用于说明 ADM 上存在典型困难样本，仅依赖 FSD 分数不足以完整解释误判原因。

human_takeaway:
1. 这是首个“典型误判样本”。
2. 目标是证明 LVLM 能补足高层语义解释。
3. 适合落在论文第五章讨论部分。
```

## 5. 案例 2

```text
sample_id: adm_case_002
image_path: 待从服务器补
ground_truth: fake
case_type: fsd_misclassified

official_fsd_prediction: 待填写
official_fsd_score: 待填写
fsd_finetune_v1_prediction: 待填写
fsd_finetune_v1_score: 待填写
fsd_finetune_v2_prediction: 待填写
fsd_finetune_v2_score: 待填写
stay_positive_prediction: 待填写
stay_positive_score: 待填写

visual_note: 重点挑选首轮微调后仍然不稳、但具有一定代表性的困难假图。

prompt_type: base
lvlm_prompt: 使用“基础分析模板”，重点回答为什么首轮微调仍未完全解决该样本。

lvlm_raw_output_summary:
1. 判断该样本更像局部结构问题还是全局语义问题。
2. 记录最自然和最可疑的区域。
3. 记录是否存在值得人工复核的重点区域。

final_judgement: 待基于真实案例填写

paper_ready_summary: 该案例用于说明首轮微调虽然有效，但并未彻底解决 ADM 中最难的样本。

human_takeaway:
1. 这是“首轮微调仍未完全解决”的代表案例。
2. 重点支撑论文中关于训练收益边界的讨论。
3. 适合落在论文第五章讨论或第六章后续工作部分。
```

## 6. 案例 3

```text
sample_id: adm_case_003
image_path: 待从服务器补
ground_truth: fake
case_type: model_conflict

official_fsd_prediction: 待填写
official_fsd_score: 待填写
fsd_finetune_v1_prediction: 待填写
fsd_finetune_v1_score: 待填写
fsd_finetune_v2_prediction: 待填写
fsd_finetune_v2_score: 待填写
stay_positive_prediction: 待填写
stay_positive_score: 待填写

visual_note: 优先挑选 FSD 与 Stay-Positive 结论明显冲突的样本。

prompt_type: conflict
lvlm_prompt: 使用“模型冲突样本分析模板”，重点解释为什么不同检测器会给出不同判断。

lvlm_raw_output_summary:
1. 列出支持“真实”的视觉证据。
2. 列出支持“AI 生成”的视觉证据。
3. 说明冲突更像来自低层纹理还是高层语义。

final_judgement: 待基于真实案例填写

paper_ready_summary: 该案例用于说明 FSD 与 Stay-Positive 的关注证据并不完全相同，因此需要 LVLM 补充解释链条。

human_takeaway:
1. 这是“模型冲突样本”代表。
2. 重点支撑三条技术路线互补关系。
3. 适合放入论文讨论部分。
```

## 7. 案例 4

```text
sample_id: adm_case_004
image_path: 待从服务器补
ground_truth: fake
case_type: model_conflict

official_fsd_prediction: 待填写
official_fsd_score: 待填写
fsd_finetune_v1_prediction: 待填写
fsd_finetune_v1_score: 待填写
fsd_finetune_v2_prediction: 待填写
fsd_finetune_v2_score: 待填写
stay_positive_prediction: 待填写
stay_positive_score: 待填写

visual_note: 优先挑选模型冲突明显、同时人工观察也感到难判的样本。

prompt_type: conflict
lvlm_prompt: 使用“模型冲突样本分析模板”，重点回答哪个模型的关注点更可能偏离真正问题。

lvlm_raw_output_summary:
1. 判断冲突更像阈值、局部纹理还是整体语义问题。
2. 提炼 2 到 3 个最关键证据点。
3. 记录 LVLM 最终更倾向哪一边及理由。

final_judgement: 待基于真实案例填写

paper_ready_summary: 该案例用于说明在 ADM 困难样本上，不同检测模型可能围绕不同证据做出冲突判断。

human_takeaway:
1. 这是第二个“模型冲突样本”。
2. 目标是补足论文中关于方法关注点差异的解释。
3. 适合与案例 3 形成对照。
```

## 8. 案例 5

```text
sample_id: adm_case_005
image_path: 待从服务器补
ground_truth: fake
case_type: borderline_case

official_fsd_prediction: 待填写
official_fsd_score: 待填写
fsd_finetune_v1_prediction: 待填写
fsd_finetune_v1_score: 待填写
fsd_finetune_v2_prediction: 待填写
fsd_finetune_v2_score: 待填写
stay_positive_prediction: 待填写
stay_positive_score: 待填写

visual_note: 优先挑选分数接近阈值、真假视觉上都比较接近自然图像的样本。

prompt_type: borderline
lvlm_prompt: 使用“边界样本分析模板”，重点解释为什么这张图难以判断。

lvlm_raw_output_summary:
1. 记录图像中最自然的部分。
2. 记录图像中最可疑的部分。
3. 记录最值得人工复核的区域。

final_judgement: 待基于真实案例填写

paper_ready_summary: 该案例用于说明边界样本上仅依赖分类分数并不足以完整解释模型行为。

human_takeaway:
1. 这是首个“边界样本”。
2. 目标是补足论文中的边界样本讨论。
3. 适合连接 LVLM 的研究作用。
```

## 9. 案例 6

```text
sample_id: adm_case_006
image_path: 待从服务器补
ground_truth: fake
case_type: borderline_case

official_fsd_prediction: 待填写
official_fsd_score: 待填写
fsd_finetune_v1_prediction: 待填写
fsd_finetune_v1_score: 待填写
fsd_finetune_v2_prediction: 待填写
fsd_finetune_v2_score: 待填写
stay_positive_prediction: 待填写
stay_positive_score: 待填写

visual_note: 优先挑选第二轮保守微调仍未改善的代表性边界样本。

prompt_type: borderline
lvlm_prompt: 使用“边界样本分析模板”，重点回答为什么更保守的第二轮微调没有改善该样本。

lvlm_raw_output_summary:
1. 判断这是否属于 ADM 中最难的一类样本。
2. 判断问题更像局部结构异常还是高层语义不协调。
3. 记录该案例是否适合写成“调小参数并不能自动解决问题”的证据。

final_judgement: 待基于真实案例填写

paper_ready_summary: 该案例用于说明第二轮保守微调未进一步改善困难样本，训练收益对配置变化较为敏感。

human_takeaway:
1. 这是第二个“边界样本”。
2. 目标是连接训练负结果与 LVLM 解释分析。
3. 适合落在论文第六章后续工作部分。
```

## 10. 当前建议

第一次正式填写时，优先保证：

- 每个案例都能写出为什么被选中
- 每个案例都能比较三组 `FSD` 结论差异
- 每个案例都能压缩出 1 句可直接写进论文的话
