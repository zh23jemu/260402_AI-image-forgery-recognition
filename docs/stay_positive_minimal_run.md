# Stay-Positive 最小运行入口说明

## 1. 当前定位

Stay-Positive 这条当前不建议直接进入训练，而是先走官方提供的测试流程，优先复用预训练模型：

- `corvi-staypos.pth`
- `rajan-staypos.pth`

当前最小目标是先跑通一次“数据路径 -> CSV -> 模型打分 -> 指标计算”的完整流程。

## 2. 测试入口

根据 [stay_positive/test_code/README.md](/C:/Coding/260402_AI-image-forgery-recognition/stay_positive/test_code/README.md) 和 [stay_positive/test_code/main.py](/C:/Coding/260402_AI-image-forgery-recognition/stay_positive/test_code/main.py)，最小运行流程如下：

1. 准备图片目录
2. 用 `create_csv.py` 生成待测图片 CSV
3. 用 `main.py` 对 CSV 中的图片逐张打分
4. 用 `eval.py` 计算 accuracy / AP

## 3. 当前代码关键点

### 3.1 配置文件来源

`main.py` 会从：

- `weights_dir/<model_name>/config.yaml`

读取模型配置，并根据 `config.yaml` 中的 `weights_file` 找到权重。

也就是说，Stay-Positive 的最小运行并不是直接传一个 `.pth` 文件路径，而是：

- 先整理 `weights` 目录结构
- 再通过模型名选择对应配置

### 3.2 输入格式

`main.py` 读取的是 CSV 文件，CSV 至少需要一列：

- `filename`

这些路径相对于输入 CSV 所在目录进行拼接。

### 3.3 结果输出

`main.py` 输出一个结果 CSV，其中模型列的值是对应图片的 fake score。  
后续通过 `eval.py` 使用 real/fake 两个 CSV 计算 accuracy 和 average precision。

## 4. 当前最小运行所需资源

### 4.1 已具备

- `stay_positive/` 官方代码
- `checkpoints/stay_positive/corvi-staypos.pth`
- `checkpoints/stay_positive/rajan-staypos.pth`

### 4.2 仍需整理

- 一个用于测试的图片目录或软链接目录
- 与预训练模型匹配的 `weights_dir/<model_name>/config.yaml`
- Stay-Positive 运行所需的 Python 环境与依赖

## 5. 建议的最小测试数据

为了降低复杂度，建议直接从当前已整理好的 FSD 数据中抽一小部分做 Stay-Positive 的首次验证，例如：

- `data/GenImage/real/val/nature`
- `data/GenImage/Midjourney/val/ai`

原因：

- 当前这两类路径已经确认可用
- 能直接构成 real/fake 对照
- 有利于把 FSD 与 Stay-Positive 的实验基础统一起来

## 6. 推荐的下一步

当前最值得先查清的是两件事：

1. `stay_positive/test_code/weights/` 目录下默认配置结构怎样组织
2. 如何把现有的 `corvi-staypos.pth` 和 `rajan-staypos.pth` 接入到该配置结构里

一旦这两点确认，就可以继续做：

- 生成 real/fake 的测试 CSV
- 运行 `main.py`
- 用 `eval.py` 得到第一条 Stay-Positive 基线结果
