# 训练前检查清单

## 1. 目标

这份清单用于保证我们进入下一步训练前，不再因为路径、环境或口径问题反复返工。

## 2. 环境检查

- `.venv` 可用
- `.venv/bin/python` 或对应服务器路径可正常导入 `torch`
- `.venv/bin/torchrun` 可用
- GPU 可见
- 日志目录可写

## 3. 数据检查

- `data/GenImage` 为统一数据入口
- `ADM/train/ai`
- `ADM/val/ai`
- `real/train/nature`
- `real/val/nature`

以上目录都应可访问，且路径与训练脚本一致。

## 4. 代码检查

- `fsd/train.py` 存在
- `fsd/test.py` 存在
- `fsd/scripts/train.sh` 已改为使用本地 `.venv` 的 `torchrun`
- `fsd/scripts/eval_adm.sh` 可继续用于训练后评估

## 5. 输出检查

- 输出目录已规划
- 日志命名已规划
- 训练完成后 checkpoint 保存位置已明确

## 6. 论文口径检查

训练开始前，统一口径应为：

- 当前进入的是“最小改进训练”
- 首轮对象是 `FSD / ADM`
- `Stay-Positive` 继续作为增强思想和对照基线
- `LVLM` 继续作为解释性补充路线

## 7. 通过标准

如果以上内容都已确认，就可以直接进入下一步训练。
