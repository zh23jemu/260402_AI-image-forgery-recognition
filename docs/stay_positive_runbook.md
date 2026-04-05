# Stay-Positive 最小运行手册

## 1. 当前确认的信息

本地已确认两个预训练模型文件都包含：

- `model`
- `optimizer`
- `total_steps`

并且最终分类层为：

- `fc.weight` 形状 `(1, 2048)`
- `fc.bias` 形状 `(1,)`

这说明当前两份权重都可视为单输出的 ResNet-50 检测器，与 `test_code` 中现有的 `res50nodown` 配置形式兼容。

## 2. 已准备好的本地模板

已在以下目录准备好最小配置模板：

- [corvi-plus/config.yaml](/C:/Coding/260402_AI-image-forgery-recognition/stay_positive/test_code/weights/corvi-plus/config.yaml)
- [rajan-ours-plus/config.yaml](/C:/Coding/260402_AI-image-forgery-recognition/stay_positive/test_code/weights/rajan-ours-plus/config.yaml)

当前默认配置为：

```yaml
arch: res50nodown
model_name: <模型名>
norm_type: resnet
patch_size: null
weights_file: weights.pth
```

这是基于仓库自带 `ours-sync/config.yaml` 以及两个 Stay-Positive checkpoint 的结构做出的最小兼容假设。

## 3. 服务器端推荐放置方式

在服务器上建议将原始权重复制或软链接到：

```text
stay_positive/test_code/weights/corvi-plus/weights.pth
stay_positive/test_code/weights/rajan-ours-plus/weights.pth
```

来源分别是：

```text
checkpoints/stay_positive/corvi-staypos.pth
checkpoints/stay_positive/rajan-staypos.pth
```

## 4. 最小测试数据建议

首次测试建议直接复用当前已经整理好的 FSD 数据：

- real: `data/GenImage/real/val/nature`
- fake: `data/GenImage/Midjourney/val/ai`

这样可以让 FSD 与 Stay-Positive 共享同一批基础数据，便于后续横向比较。

## 5. 最小运行流程

### 5.1 生成 CSV

在 `stay_positive/test_code/` 目录中执行：

```bash
../.venv/bin/python create_csv.py ../../data/GenImage/real/val/nature ../../stay_positive_runs/real_val.csv --dir real
../.venv/bin/python create_csv.py ../../data/GenImage/Midjourney/val/ai ../../stay_positive_runs/midjourney_val.csv --dir fake
```

说明：

- `create_csv.py` 默认每个目录最多写入前 `3000` 张图。
- 输出 CSV 中包含 `filename` 和 `typ` 两列。

### 5.2 对 real 图片打分

```bash
../.venv/bin/python main.py --in_csv ../../stay_positive_runs/real_val.csv --out_csv ../../stay_positive_runs/real_scores.csv --device cuda:0 --weights_dir ./weights --models corvi-plus,rajan-ours-plus
```

### 5.3 对 fake 图片打分

```bash
../.venv/bin/python main.py --in_csv ../../stay_positive_runs/midjourney_val.csv --out_csv ../../stay_positive_runs/fake_scores.csv --device cuda:0 --weights_dir ./weights --models corvi-plus,rajan-ours-plus
```

### 5.4 计算指标

```bash
../.venv/bin/python eval.py --real ../../stay_positive_runs/real_scores.csv --fake ../../stay_positive_runs/fake_scores.csv --ix 2
```

`--ix 2` 表示最后两列模型分数都会参与评估。

### 5.5 批任务运行

如果交互式 `srun --pty bash` 会话时间不够，建议直接提交批任务：

```bash
sbatch run_stay_positive_midjourney.slurm
```

该脚本会依次执行：

1. real 图片打分
2. Midjourney fake 图片打分
3. `eval.py` 统计指标

日志位置：

- `logs/stay_positive_mj_<jobid>.out`
- `logs/stay_positive_mj_<jobid>.err`

## 6. 运行前检查点

在服务器真正运行之前，优先确认：

1. `weights/corvi-plus/weights.pth` 是否存在
2. `weights/rajan-ours-plus/weights.pth` 是否存在
3. `stay_positive/test_code` 所在环境能否导入 `torch`、`yaml`、`pandas`、`PIL`
4. `stay_positive_runs/` 目录是否存在或能自动创建

## 7. 当前建议

先把 `Corvi +` 与 `Rajan/Ours +` 两个模型都接入同一批 `real/val` 与 `Midjourney/val` 数据，拿到第一条 Stay-Positive 基线结果，再决定是否扩展到 `SD`。
