# LVLM 案例记录模板

## 1. 用途

这份模板用于记录已经实际送入 `LVLM` 分析的案例。

它和候选样本清单的区别是：

- 候选清单是“待选”
- 案例记录是“已经正式分析”

## 2. 单案例记录模板

下面是一条案例建议使用的记录格式。

```text
sample_id:
image_path:
generator_type:
ground_truth:
case_type:

fsd_prediction:
fsd_score:
stay_positive_prediction:
stay_positive_score:

prompt_type:
lvlm_prompt:

lvlm_raw_output_summary:
1.
2.
3.

final_judgement:

paper_ready_summary:

human_takeaway:
1.
2.
3.
```

## 3. Markdown 表格模板

如果想用表格快速总览，可以用下面这个版本：

| sample_id | generator_type | case_type | fsd_prediction | fsd_score | stay_positive_prediction | stay_positive_score | prompt_type | final_judgement | paper_ready_summary | human_takeaway |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sample_001 | ADM | fsd_misclassified | real | 待填写 | fake | 待填写 | base | 待填写 | 待填写 | 待填写 |
| sample_002 | Midjourney | model_conflict | fake | 待填写 | real | 待填写 | conflict | 待填写 | 待填写 | 待填写 |

## 4. 推荐整理方式

每个案例建议最终压缩为三层内容：

- 原始提示词
- `LVLM` 输出摘要
- 论文可直接使用的总结句

不建议直接把长篇原始回答原封不动塞进论文。

## 5. 论文可直接引用的简写格式

后续写论文时，每个案例可以压缩成如下句式：

```text
在某一边界样本中，LVLM 指出图像在局部结构与全局语义一致性上同时存在可疑迹象，说明该样本并非仅在低层纹理上具有异常，而是可能存在更高层的语义不协调。这表明 LVLM 可为传统判别模型的误判分析提供补充证据。
```

## 6. 当前建议

第一次正式整理时，建议先只做：

- `2` 个 `fsd_misclassified`
- `2` 个 `model_conflict`
- `2` 个 `borderline_case`

共 `6` 个案例即可。
