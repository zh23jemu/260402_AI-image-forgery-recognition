# FSD 本地仓库运行笔记

## 1. 已确认的仓库结构

当前 [fsd](/C:/Coding/260402_AI-image-forgery-recognition/fsd) 目录中已确认存在以下关键文件：

- `README.md`
- `requirements.txt`
- `train.py`
- `test.py`
- `scripts/eval.sh`
- `scripts/train.sh`
- `datasets/`
- `model/`
- `util/`

这说明官方代码已基本完整到位，可以进入脚本级检查和路径对齐阶段。

## 2. 依赖信息

`requirements.txt` 中当前列出的依赖为：

- `torch>=2.3.0`
- `torchvision`
- `torchmetrics`
- `timm`
- `einops`
- `dill`
- `tqdm`
- `scikit-learn`
- `matplotlib`

从依赖规模看，FSD 的环境门槛并不算高。当前真正的重点是 PyTorch 版本、CUDA 环境和数据目录是否能对齐。

## 3. 训练脚本信息

`scripts/train.sh` 当前默认参数显示：

- `GPU_NUM=1`
- `WORLD_SIZE=1`
- `NUM_WORKERS=8`
- `SEED=42`
- `EXCLUDE_CLASS="ADM"`
- `batch_size=16`
- `lr=1e-4`
- `total_training_steps=50000`
- 使用 `torchrun`

这意味着 README 虽然提到可配置多卡，但当前仓库里默认脚本已经是单卡版本，并不是必须多卡才能启动。

## 4. 评估脚本信息

`scripts/eval.sh` 当前默认参数显示：

- `TEST_CLASS="ADM"`
- `CKPT_PATH="your_ckpt_path/resnet50_200000.pth"`
- 数据根目录为 `data/GenImage`
- 执行入口为 `python test.py`

因此，FSD 当前最小运行前必须手动处理的内容是：

1. 将 `CKPT_PATH` 改成真实路径。
2. 保证运行目录下能正确找到 `data/GenImage`。
3. 保证 `TEST_CLASS` 对应实际存在的数据类别。

## 5. 当前最可能的阻塞点

### 5.1 数据目录名不一致

当前 `train.py` 与 `test.py` 中实际写死使用的类别名是：

- `ADM`
- `BigGAN`
- `glide`
- `Midjourney`
- `SD`
- `VQDM`
- `real`

而 GenImage 原始目录常见命名可能是：

- `Stable Diffusion V1.4`
- `Stable Diffusion V1.5`
- `GLIDE`

当前已经可以明确确认：代码就是直接按这些类名拼接目录路径。因此如果本地数据目录不采用这些命名，脚本无法直接原样运行。

这意味着后续只有两条处理路线：

1. **按 FSD 期望的命名重组数据目录**
   例如将与 `SD` 对应的数据整理到 `data/GenImage/SD/`，并额外整理 `real/` 目录。
2. **修改 FSD 代码中的类别名与路径读取逻辑**
   这种方式风险更高，当前阶段不建议立即做。

### 5.2 当前最小数据子集不足以覆盖默认测试类

如果你目前只准备 `Stable Diffusion V1.4`，那么默认 `TEST_CLASS="ADM"` 无法直接满足。也就是说，即使环境装好、checkpoint 到位，也不能直接照抄默认 `eval.sh` 跑起来。

进一步说，即使把 `TEST_CLASS` 改成 `SD`，也仍然需要本地目录真实存在：

- `data/GenImage/SD/val`
- `data/GenImage/real/val`

因此，“只下载了 Stable Diffusion V1.4”并不等于“FSD 已具备最小可运行目录”。后续还需要按 FSD 预期重新组织这一部分数据。

### 5.3 checkpoint 路径必须手填

官方脚本没有自动发现 checkpoint 的机制，必须在 `eval.sh` 中手动填写实际文件路径。

## 6. 当前最稳的下一步

在继续实现前，优先级建议如下：

1. 先把 FSD checkpoint 放进 [checkpoints/fsd](/C:/Coding/260402_AI-image-forgery-recognition/checkpoints/fsd)
2. 再把你实际准备的 GenImage 子目录放进 [data/GenImage](/C:/Coding/260402_AI-image-forgery-recognition/data/GenImage)
3. 优先按 FSD 期望的目录名补出：
   - `data/GenImage/SD/`
   - `data/GenImage/real/`
4. 到时再检查 `train.py`、`test.py` 是否还需要额外路径修正
5. 最后才决定是否需要修改脚本中的默认类别或相对路径
