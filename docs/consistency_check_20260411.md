# 结果一致性检查记录（2026-04-11）

## 检查目的

对当前项目中最重要的两份结果文档进行一致性核对：

- [docs/full_paper_draft.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/full_paper_draft.md)
- [docs/experiment_results_summary.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/experiment_results_summary.md)

重点确认：

- `FSD` 六类生成器结果是否一致
- `Stay-Positive` 正式结果是否一致
- `Stay-Positive ADM` 扩展观察结果是否一致

## 检查结果

### 1. FSD 六类生成器结果

两份文档中的以下结果一致：

| 生成器 | Accuracy | AP |
| --- | --- | --- |
| Midjourney | 79.56% | 82.04% |
| Stable Diffusion | 88.34% | 91.30% |
| ADM | 75.41% | 79.34% |
| BigGAN | 79.27% | 82.40% |
| GLIDE | 96.67% | 96.82% |
| VQDM | 75.47% | 77.15% |

### 2. Stay-Positive 正式结果

两份文档中的以下结果一致：

| 测试类别 | 模型 | Accuracy | AP |
| --- | --- | --- | --- |
| Midjourney | Corvi+ | 99.60% | 99.98% |
| Midjourney | Rajan/Ours+ | 98.40% | 99.94% |
| Stable Diffusion | Corvi+ | 99.78% | 100% |
| Stable Diffusion | Rajan/Ours+ | 99.88% | 100% |

### 3. Stay-Positive ADM 扩展观察

当前两份文档中的扩展观察口径一致，均保留以下结果：

| 测试类别 | 模型 | RACC | FACC | ACC | AP |
| --- | --- | --- | --- | --- | --- |
| ADM | Rajan/Ours+ | 99.77% | 4.73% | 52.25% | 87.58% |

## 当前结论

- 主稿与结果总表中的核心实验数字一致。
- 当前未发现会影响论文正文和汇报材料的数值冲突。
- 后续如果继续修改论文或补充图表，建议优先以：
  - [docs/full_paper_draft.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/full_paper_draft.md)
  - [docs/experiment_results_summary.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/experiment_results_summary.md)
  
  作为统一结果来源。
