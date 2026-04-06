# FSD 与 Stay-Positive 方法与结果对比

## 1. 方法定位对比

| 方法 | 当前使用模型 | 当前测试方式 | 主要特点 | 当前阶段定位 |
| --- | --- | --- | --- | --- |
| FSD | 官方预训练 `ResNet-50` checkpoint | 直接基于 `GenImage` 目录按类评估 | 强调少样本泛化与未知生成器检测 | 作为泛化检测主基线 |
| Stay-Positive | `Corvi +` / `Rajan-Ours +` 预训练模型 | 先生成 CSV，再做 real/fake 打分评估 | 强调减少对真实图像特征的错误依赖 | 作为鲁棒判别主基线 |

## 2. 当前实验结果对比

| 方法 | 数据类别 | 模型/权重 | Accuracy | AP | 备注 |
| --- | --- | --- | --- | --- | --- |
| FSD | Midjourney | `resnet50_exclude_midjourney_step[200000]_converted.pth` | `79.56%` | `82.04%` | 已完成正式评估 |
| FSD | SD | `resnet50_exclude_sd_step[200000]_converted.pth` | `88.34%` | `91.30%` | 已完成正式评估 |
| Stay-Positive | Midjourney | `Corvi +` | `99.60%` | `99.98%` | 已完成正式评估 |
| Stay-Positive | Midjourney | `Rajan/Ours +` | `98.40%` | `99.94%` | 已完成正式评估 |
| Stay-Positive | SD | `Corvi +` | `99.78%` | `100%` | 已完成正式评估 |
| Stay-Positive | SD | `Rajan/Ours +` | `99.88%` | `100%` | 已完成正式评估 |

## 3. 当前结果的直接观察

- `FSD` 在 `SD` 数据上的结果优于 `Midjourney`，说明不同生成器类别上的检测难度存在差异。
- `Stay-Positive` 在当前 `Midjourney` 和 `SD` 的测试设定下都显著优于 `FSD`。
- 在 `Midjourney` 场景中，`Corvi +` 略优于 `Rajan/Ours +`。
- 在 `SD` 场景中，`Rajan/Ours +` 略优于 `Corvi +`。

## 4. 当前阶段应如何解释这些差异

- `FSD` 与 `Stay-Positive` 的方法目标并不完全相同。前者强调未知生成器和少样本适应，后者强调鲁棒判别与伪相关抑制，因此不能仅凭单组指标简单下结论说某一方法“全面更优”。
- 当前测试设定主要是固定的 `real vs fake` 二分类场景，更接近 Stay-Positive 的直接应用形式，因此其结果更高是可以理解的。
- `FSD` 的优势更可能体现在跨生成器泛化、少样本适应以及未知类别场景中，后续需要更多测试才能充分体现。
- 因此，当前更合理的表述是：Stay-Positive 在当前单类对照测试中的表现更强，而 FSD 为后续面向未知模型的扩展研究提供了更合适的主干基础。

## 5. 论文中建议使用的结论

当前实验表明，两类方法在相同数据基础上的表现存在明显差异。Stay-Positive 预训练模型在 `Midjourney` 和 `SD` 测试中均取得了接近满分的 accuracy 和 AP，说明其在当前 real/fake 对照场景下具有很强的检测能力；相比之下，FSD 在 `Midjourney` 和 `SD` 上分别取得约 `79.56%` 与 `88.34%` 的准确率，虽整体低于 Stay-Positive，但已经体现出一定的生成器区分能力和可用的基线价值。综合来看，Stay-Positive 更适合作为当前阶段的高性能判别基线，FSD 则更适合作为后续研究未知模型泛化和方法融合的主干路线。
