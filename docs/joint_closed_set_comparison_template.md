# 闭集联合训练对比表模板

## 1. 用途

本模板用于在 `run_fsd_joint_base_stage1.slurm` 跑完后，快速整理：

- `FSD-only closed-set`
- `FSD + Stay-Positive closed-set`

两组结果的公平对照结论。

## 2. 当前已知结果

当前已经拿到的 `FSD + SP Stage1` 结果为：

| 生成器 | FSD+SP ACC | FSD+SP AP |
| --- | --- | --- |
| ADM | 95.50% | 97.50% |
| SD | 95.34% | 97.90% |
| Midjourney | 87.00% | 90.47% |

说明：

- 以上结果来自闭集协议，训练集中已包含 `ADM`、`SD` 与 `Midjourney`。
- 因此它们不能直接与历史 `exclude-ADM` 开放协议结果做严格横向比较。

## 3. 待补字段

`FSD-only` 同协议结果出来后，需要立刻补下表：

| 生成器 | FSD-only ACC | FSD-only AP | FSD+SP ACC | FSD+SP AP | ACC 差值 | AP 差值 | 结论 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADM | pending | pending | 95.50% | 97.50% | pending | pending | pending |
| SD | pending | pending | 95.34% | 97.90% | pending | pending | pending |
| Midjourney | pending | pending | 87.00% | 90.47% | pending | pending | pending |

## 4. 快速结论模板

### 4.1 如果联合训练明显更优

可直接写为：

“在相同闭集协议、相同初始化 checkpoint 和相同训练步数条件下，引入 `Stay-Positive` 辅助约束后，模型在 `ADM`、`SD` 和 `Midjourney` 上取得了更高的准确率与平均精度，说明第一阶段联合训练不只是跑通，而且已经体现出实际性能增益。” 

### 4.2 如果差距较小

可直接写为：

“当前结果首先说明闭集训练框架本身有效，而 `Stay-Positive` 辅助约束的附加收益暂时有限。因此，第一阶段更适合作为联合训练可行性验证，而不是直接宣称已经带来显著性能突破。” 

### 4.3 如果不同类别表现不一致

可直接写为：

“当前联合训练收益呈现出类别选择性，即 `Stay-Positive` 辅助约束在部分生成器上提供明显帮助，但在另一些类别上的增益仍不稳定。这说明后续需要围绕类别差异进一步优化联合损失设计。” 

## 5. 推荐命令

训练一结束后，建议直接运行：

```powershell
.\.venv\Scripts\python.exe tools\build_joint_closed_set_comparison.py `
  --output_csv analysis\joint_closed_set_comparison.csv `
  --output_md docs\joint_closed_set_comparison.md
```

如果本地没有服务器日志，就在服务器项目根目录运行：

```bash
./.venv/bin/python tools/build_joint_closed_set_comparison.py \
  --output_csv analysis/joint_closed_set_comparison.csv \
  --output_md docs/joint_closed_set_comparison.md
```
