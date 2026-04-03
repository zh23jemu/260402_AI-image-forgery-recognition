# FSD + Stay-Positive 代码初稿与最小运行方案

## 1. 当前定位

本目录中的代码部分不以“完整融合工程”为目标，而是以“可运行基线准备版”为目标。当前阶段的重点是把两篇论文的官方实现、数据目录、预训练模型路径和运行入口整理清楚，为后续最小验证和进一步融合打基础。

当前默认约束如下：

- 保留两份官方仓库，不先重构为统一项目。
- 不先修改训练脚本，不先开展联合训练。
- 优先使用预训练模型和公开数据子集。
- 使用项目本地目录管理数据和权重。

## 2. 建议目录结构

```text
C:\Coding\260402_AI-image-forgery-recognition
├── docs
├── fsd
├── stay_positive
├── data
│   └── GenImage
├── checkpoints
│   ├── fsd
│   └── stay_positive
└── notes
```

当前工作区已经准备好了上述目录对应的说明文件，但官方代码仓库尚未成功在线克隆到本地。后续你可以将官方 ZIP 解压到对应目录，或在网络稳定时重新克隆。

## 3. 官方资源入口

### 3.1 FSD

- 官方仓库：<https://github.com/teheperinko541/Few-Shot-AIGI-Detector>
- 论文：<https://arxiv.org/abs/2501.08763>
- 数据说明：使用 GenImage
- checkpoint：仓库 README 给出百度网盘入口，提取码 `icml`

已核对本地 FSD 仓库后，当前可确认的关键信息包括：

- 环境建议为 Python 3.12
- 安装方式为 `pip install -r requirements.txt`
- 推理入口为 `scripts/eval.sh`
- 训练入口为 `scripts/train.sh`
- `requirements.txt` 当前包含：
  - `torch>=2.3.0`
  - `torchvision`
  - `torchmetrics`
  - `timm`
  - `einops`
  - `dill`
  - `tqdm`
  - `scikit-learn`
  - `matplotlib`
- 评估前需要在脚本中手动指定 checkpoint 目录
- README 期望的数据组织为 `data/GenImage/{ADM,BigGAN,glide,Midjourney,SD,VQDM,real}`
- 其中 `real` 来自 `stable_diffusion_v_1_4` 和 `stable_diffusion_v_1_5` 的 `nature` 图像
- 当前 `scripts/train.sh` 实际默认是单卡配置：
  - `GPU_NUM=1`
  - 使用 `torchrun`
  - 默认 `EXCLUDE_CLASS="ADM"`
  - 默认训练步数 `50000`
- 当前 `scripts/eval.sh` 实际默认测试类为 `ADM`
- 当前 `scripts/eval.sh` 中的 checkpoint 路径仍是占位值 `your_ckpt_path/resnet50_200000.pth`
- 当前脚本中的数据根目录使用相对路径 `data/GenImage`

### 3.2 Stay-Positive

- 官方仓库：<https://github.com/AniSundar18/AlignedForensics>
- 项目页：<https://anisundar18.github.io/Stay-Positive/>
- 论文：<https://openreview.net/forum?id=VNLmfMJi3w>
- 预训练模型：仓库 README 中给出 `Corvi +` 与 `Rajan/Ours +` 等模型入口
- 评估数据：仓库 README 给出 Hugging Face 数据入口

Stay-Positive 的官方仓库同时包含 ICLR 2025 和 ICML 2025 两个相关工作，因此当前阶段重点只关注与 Stay-Positive 论文直接相关的预训练检测器和评估逻辑。

## 4. 数据准备策略

当前阶段采用最小数据子集策略。由于 GenImage 体量较大，允许先只准备 `Stable Diffusion V1.4`，后续再补其他生成器目录。

### 4.1 推荐的第一阶段数据准备

- 已准备或计划优先准备：
  - `Stable Diffusion V1.4`
- 后续可扩展：
  - `Stable Diffusion V1.5`
  - `Midjourney`
  - `VQDM`
  - `ADM`
  - `BigGAN`
  - `GLIDE`

### 4.2 当前写作口径

如果第一阶段只准备 `Stable Diffusion V1.4`，文稿中应统一表述为：

- 当前阶段使用公开数据子集开展流程验证
- 当前实验目标是建立基线与验证可行性
- 不将最小数据子集结果表述为完整的未知模型泛化结论

## 5. 权重放置规则

建议将权重统一放在以下目录：

```text
checkpoints/
├── fsd/
└── stay_positive/
```

建议的组织方式如下：

- `checkpoints/fsd/`
  - 存放 FSD 官方 checkpoint
  - 同时保留下载来源和提取码记录
- `checkpoints/stay_positive/`
  - 存放 Stay-Positive 相关预训练模型
  - 根据模型名建立子目录，避免混淆不同检测器

## 6. 最小运行顺序

当前推荐的推进顺序如下：

1. 将 FSD 官方代码放入 [fsd](/C:/Coding/260402_AI-image-forgery-recognition/fsd)。
2. 将 Stay-Positive 官方代码放入 [stay_positive](/C:/Coding/260402_AI-image-forgery-recognition/stay_positive)。
3. 将 `Stable Diffusion V1.4` 数据整理到 [data/GenImage](/C:/Coding/260402_AI-image-forgery-recognition/data/GenImage)。
4. 将 FSD checkpoint 放入 [checkpoints/fsd](/C:/Coding/260402_AI-image-forgery-recognition/checkpoints/fsd)。
5. 将 Stay-Positive 预训练模型放入 [checkpoints/stay_positive](/C:/Coding/260402_AI-image-forgery-recognition/checkpoints/stay_positive)。
6. 先检查 FSD `scripts/eval.sh` 与 `scripts/train.sh` 的路径要求。
7. 再检查 Stay-Positive 仓库中的测试入口与模型加载方式。
8. 记录两边输入、输出和特征位置，为后续联合设计做准备。

### 6.1 已确认的 FSD 最小运行前提

基于本地仓库内容，FSD 在当前阶段最需要确认的并不是训练参数，而是三个路径问题：

1. `data/GenImage` 是否存在于执行目录相对路径下。
2. `scripts/eval.sh` 中的 `CKPT_PATH` 是否已改成真实本地路径。
3. `TEST_CLASS` 是否对应当前实际已准备的数据目录。

若仅准备了 `Stable Diffusion V1.4`，则当前默认脚本中的 `ADM` 无法直接使用，后续需要根据代码实际支持的类别命名决定如何调整最小测试路径。

## 7. 当前阶段不做的事

为避免目标过大，当前阶段明确不做以下内容：

- 不进行完整联合训练
- 不重写两份官方仓库的训练框架
- 不在没有补足数据前声称完成跨生成器泛化实验
- 不把 LVLM 并入当前主线

## 8. 后续融合接口说明

后续的融合工作建议分成两个层次：

### 8.1 论文层

- 用 FSD 负责“少样本泛化检测”的主叙事
- 用 Stay-Positive 负责“抑制真实特征干扰”的增强叙事
- 将联合方案表述为“主干 + 判别增强”

### 8.2 代码层

第一阶段先记录以下接口信息：

- FSD 的输入图像格式和标签组织方式
- FSD 的主干特征输出位置
- FSD 的最终判别输出含义
- Stay-Positive 的模型输入和输出含义
- Stay-Positive 的核心损失或判别约束思想

只有在这些接口被真正看清之后，才进入第二阶段的微调或桥接实现。
