# 第二轮落地清单

## 1. 当前状态

当前工作区已经具备以下内容：

- 论文初稿正文：[docs/paper_draft.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/paper_draft.md)
- 代码准备方案：[docs/code_baseline_plan.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/code_baseline_plan.md)
- 联合设计说明：[docs/fusion_design.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/fusion_design.md)
- 下载入口整理：[notes/download_links.md](/C:/Coding/260402_AI-image-forgery-recognition/notes/download_links.md)

当前仍未到位的资源：

- FSD 官方代码
- Stay-Positive 官方代码
- FSD checkpoint
- Stay-Positive 预训练模型
- GenImage 最小数据子集

## 2. 资源落位要求

### 2.1 FSD 官方代码

将官方仓库内容放入：

- [fsd](/C:/Coding/260402_AI-image-forgery-recognition/fsd)

到位后应至少能看到：

- `README.md`
- `requirements.txt`
- `train.py`
- `test.py`
- `scripts/`

### 2.2 Stay-Positive 官方代码

将官方仓库内容放入：

- [stay_positive](/C:/Coding/260402_AI-image-forgery-recognition/stay_positive)

到位后建议优先确认：

- `README.md`
- 环境配置文件
- 测试或评估入口
- 预训练模型加载说明

### 2.3 GenImage 数据

最小可运行阶段允许先只放：

- [data/GenImage](/C:/Coding/260402_AI-image-forgery-recognition/data/GenImage) 下的 `Stable Diffusion V1.4`

如果后续补充更多目录，再按同级结构继续扩展。

### 2.4 权重

将权重分别放入：

- [checkpoints/fsd](/C:/Coding/260402_AI-image-forgery-recognition/checkpoints/fsd)
- [checkpoints/stay_positive](/C:/Coding/260402_AI-image-forgery-recognition/checkpoints/stay_positive)

## 3. 到位后的第二次检查重点

资源到位后，需要重点检查以下内容：

1. FSD 的脚本是否写死了数据路径。
2. FSD 的评估脚本是否要求手动修改 checkpoint 路径。
3. Stay-Positive 的测试代码入口在哪个目录。
4. Stay-Positive 的预训练模型与测试代码是否一一对应。
5. GenImage 的目录命名是否与代码中使用的命名一致。
6. 当前仅使用 `Stable Diffusion V1.4` 时，哪些脚本可以直接跑，哪些脚本仍依赖完整数据结构。
7. 是否已经按 FSD 代码要求补出 `SD/` 和 `real/` 目录，而不是仅保留 GenImage 原始命名。

## 4. 当前论文写作可直接引用的结论

在资源未完全到位前，论文中已经可以稳定使用以下口径：

- 本研究当前阶段基于公开论文、官方代码、预训练模型和公开数据入口开展工作。
- 当前阶段优先完成基线建立与流程验证，而不直接开展联合重训练。
- 当前数据准备采用最小子集策略，先以 `Stable Diffusion V1.4` 作为流程验证数据来源。
- FSD 作为未知模型少样本检测主框架，Stay-Positive 作为抗真实特征干扰的增强思想。

## 5. 下一轮可直接继续做的事情

只要你把代码、权重或数据中的任意一项放进来，我下一轮就可以继续做对应检查：

- 如果你先放 **FSD 代码**：
  我会检查 `requirements.txt`、`scripts/`、路径假设和最小运行命令。
- 如果你先放 **Stay-Positive 代码**：
  我会梳理预训练模型入口、测试脚本和与 FSD 的可连接点。
- 如果你先放 **checkpoint**：
  我会把权重路径规则写死到本地文档里。
- 如果你先放 **GenImage 数据**：
  我会核对目录名、数据层级和是否需要补 `real/`。
