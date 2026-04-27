# 闭集联合训练对比表

## 1. 当前说明

- 本表用于对比同一闭集协议下的 `FSD-only` 与 `FSD + Stay-Positive`。
- 当前协议训练集合包含 `real`、`ADM`、`SD`、`Midjourney`，因此不能直接与历史 `exclude-ADM` 开放协议结果混用。
- `FSD-only` 日志状态：未检测到失败信号。
- `FSD + SP` 日志状态：未检测到失败信号。
- `FSD-only` checkpoint 步数：未发现。
- `FSD + SP` checkpoint 步数：未发现。

## 2. 结果总表

| 生成器 | FSD-only ACC | FSD-only AP | FSD+SP ACC | FSD+SP AP | ACC 差值 | AP 差值 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADM | pending | pending | pending | pending | pending | pending | FSD-only 结果待补齐 |
| SD | pending | pending | pending | pending | pending | pending | FSD-only 结果待补齐 |
| Midjourney | pending | pending | pending | pending | pending | pending | FSD-only 结果待补齐 |

## 3. 结论模板

### 3.1 如果 FSD+SP 整体优于 FSD-only

- 可以表述为：在相同闭集训练协议、相同初始化 checkpoint 与相同训练步数下，引入 `Stay-Positive` 辅助约束后，模型在目标生成器上取得了更高的准确率与平均精度，说明该辅助监督对第一阶段联合训练具有实际增益。

### 3.2 如果两者差距较小

- 可以表述为：当前结果首先说明闭集训练框架本身是有效的，而 `Stay-Positive` 约束的附加收益暂时有限；因此第一阶段更适合作为联合训练可行性验证，而不是直接宣称显著性能突破。

### 3.3 如果不同类别表现不一致

- 可以表述为：`Stay-Positive` 辅助约束呈现出类别选择性收益，在部分生成器上提供明显帮助，但在另一些类别上的增益仍不稳定，这说明后续仍需结合类别特征进一步设计联合损失。

## 4. 日志来源

- FSD-only out: `missing`
- FSD-only err: `missing`
- FSD+SP out: `missing`
- FSD+SP err: `missing`