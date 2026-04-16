# ADM 冲突批次执行包

这份文档用于对下一批 `strong_conflict` 案例做人工观察或 LVLM 分析。

## adm_conflict_priority_01

- `sample_id`: `adm_auto_2143`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/421_adm_153.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.592478`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```

## adm_conflict_priority_02

- `sample_id`: `adm_auto_2720`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/508_adm_174.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.590573`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```

## adm_conflict_priority_03

- `sample_id`: `adm_auto_2875`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/531_adm_153.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.568101`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```

## adm_conflict_priority_04

- `sample_id`: `adm_auto_0355`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/153_adm_153.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.562310`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```

## adm_conflict_priority_05

- `sample_id`: `adm_auto_2984`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/548_adm_174.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.555450`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```

## adm_conflict_priority_06

- `sample_id`: `adm_auto_1421`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/312_adm_85.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.555412`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```

## adm_conflict_priority_07

- `sample_id`: `adm_auto_1390`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/308_adm_7.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.549081`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```

## adm_conflict_priority_08

- `sample_id`: `adm_auto_1383`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/307_adm_34.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.539390`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```

## adm_conflict_priority_09

- `sample_id`: `adm_auto_0280`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/141_adm_7.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.533666`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```

## adm_conflict_priority_10

- `sample_id`: `adm_auto_2252`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/438_adm_174.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.526472`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```

## adm_conflict_priority_11

- `sample_id`: `adm_auto_1438`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/315_adm_7.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.525240`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```

## adm_conflict_priority_12

- `sample_id`: `adm_auto_2693`
- `image_path`: `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/503_adm_85.PNG`
- `stay_positive_postcal_prediction`: `fake`
- `official / v1 / v2`: `real / real / real`
- `stay_positive_score`: `0.523895`

```text
这张图像属于 ADM strong-conflict 样本。Stay-Positive 在校准后稳定判断为 fake，但 FSD official、首轮微调和第二轮保守微调都判断为 real。

请你从语义与视觉细节两个层面分析：
1. 图像整体为什么容易被当成真实图像。
2. 图像中哪些局部细节支持它更像 AI 生成图像。
3. 为什么这类样本可能被 Stay-Positive 抓住，但被 FSD 三个版本同时漏掉。
4. 如果必须给出判断，你更倾向真实还是 AI 生成，并说明原因。

最后请补 3 句话：
1. 这张图最关键的可疑点是什么。
2. 这个案例更像局部结构问题还是整体语义误导问题。
3. 这个案例对“FSD 系统性盲区 / 方法互补性”有什么支持作用。
```
