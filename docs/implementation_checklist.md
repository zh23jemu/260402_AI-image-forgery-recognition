# 第二轮落地清单

## 1. 当前状态

当前工作区已经具备以下内容：

- 论文主稿正文：[docs/full_paper_draft.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/full_paper_draft.md)
- 代码准备方案：[docs/code_baseline_plan.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/code_baseline_plan.md)
- 联合设计说明：[docs/fusion_design.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/fusion_design.md)
- 下一步训练方案：[docs/next_stage_training_plan.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/next_stage_training_plan.md)
- 训练前检查清单：[docs/training_ready_checklist.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/training_ready_checklist.md)
- 下载入口整理：[notes/download_links.md](/C:/Coding/260402_AI-image-forgery-recognition/notes/download_links.md)

当前仍需在训练前再次确认的资源：

- 训练输出目录是否具备写权限
- `data/GenImage` 是否在服务器端保持统一入口
- FSD 训练脚本是否使用 `.venv` 内的 `torchrun`
- 首轮训练的目标类别与日志命名是否已经固定

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

## 3. 进入训练前的第二次检查重点

资源到位后，需要重点检查以下内容：

1. FSD 的脚本是否写死了数据路径。
2. FSD 的评估脚本是否要求手动修改 checkpoint 路径。
3. Stay-Positive 的测试代码入口在哪个目录。
4. Stay-Positive 的预训练模型与测试代码是否一一对应。
5. GenImage 的目录命名是否与代码中使用的命名一致。
6. 当前训练是否已经从“最小子集验证”切换到“统一主数据目录”。
7. 是否已经按 FSD 代码要求补出 `SD/` 和 `real/` 目录，而不是仅保留 GenImage 原始命名。
8. 训练脚本、日志脚本和论文口径是否一致指向同一个首轮训练目标。

## 4. 当前论文写作可直接引用的结论

在资源未完全到位前，论文中已经可以稳定使用以下口径：

- 本研究当前阶段基于公开论文、官方代码、预训练模型和公开数据入口开展工作。
- 当前阶段已经完成基线建立与流程验证，具备进入最小改进训练的条件。
- 下一步训练将优先围绕 `FSD` 主干展开，并以 `ADM` 作为首个训练切入点。
- `Stay-Positive` 仍作为增强思想和对照基线，`LVLM` 作为解释性补充路线保留在论文结构中。

## 5. 下一轮可直接继续做的事情

- 如果直接进入训练准备，我下一轮就优先做这三件事：

1. 检查并确认首轮训练脚本参数。
2. 整理训练输出目录与日志命名规则。
3. 在训练完成后立刻把结果补进论文和结果总表。
