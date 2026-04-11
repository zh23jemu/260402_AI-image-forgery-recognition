# 项目资产检查清单

## 1. 当前项目目标

当前项目的直接目标是：

- 保持论文主稿与实验结果一致
- 确保现有代码、数据、权重和脚本具备可复现性
- 为后续老师查看、阶段汇报和最终提交保留清晰的项目资产结构

## 2. 论文文档资产

当前建议重点保留的文档如下：

- [docs/full_paper_draft.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/full_paper_draft.md)
  当前最核心的论文主稿，应作为后续论文修改的唯一主线文件。

- [docs/experiment_results_summary.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/experiment_results_summary.md)
  当前实验结果总表，用于汇报、留档和后续论文补图表时取数。

- [docs/project_schedule_to_20260425.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/project_schedule_to_20260425.md)
  当前项目推进计划，用于后续控制任务范围和提醒节奏。

- [docs/lvlm_integration_notes.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/lvlm_integration_notes.md)
  `LVLM` 纳入本次论文的专项说明，用于统一后续汇报口径、边界表述和执行顺序。

- [docs/lvlm_case_analysis_plan.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/lvlm_case_analysis_plan.md)
  `LVLM` 轻量案例分析执行方案，用于后续实际选样、整理和论文落地。

- [docs/lvlm_prompt_templates.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/lvlm_prompt_templates.md)
  `LVLM` 提示词模板文档，用于后续统一分析口径和输出格式。

- [docs/lvlm_candidate_sample_template.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/lvlm_candidate_sample_template.md)
  `LVLM` 候选样本清单模板，用于后续实际筛样。

- [docs/lvlm_case_record_template.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/lvlm_case_record_template.md)
  `LVLM` 正式案例记录模板，用于整理分析结果和论文用语。

当前其他早期草稿、提交稿和说明性文档可以继续保留，但后续修改时应以主稿和结果总表为准，避免多处口径漂移。

## 3. 数据资产

当前实验主数据目录建议统一以服务器端的：

```text
data/GenImage/
```

为唯一有效实验入口。

当前已确认存在的主要生成器目录：

- `Midjourney`
- `Stable Diffusion`
- `ADM`
- `BigGAN`
- `GLIDE`
- `VQDM`
- `real`

其中：

- `real/train/nature`
- `real/val/nature`

已作为真实图像统一来源使用。

早期原始目录已归档至：

```text
data/_old_raw_backup/
```

后续实验不应再直接依赖这些旧目录。

## 4. 权重资产

### 4.1 FSD

当前 `FSD` 建议保留两类权重：

- 原始官方 checkpoint
- `_converted.pth` 版本

其中，实际评估统一使用：

```text
checkpoints/fsd/*_converted.pth
```

当前已确认可用的 converted 权重包括：

- `resnet50_exclude_midjourney_step[200000]_converted.pth`
- `resnet50_exclude_sd_step[200000]_converted.pth`
- `resnet50_exclude_adm_step[200000]_converted.pth`
- `resnet50_exclude_biggan_step[200000]_converted.pth`
- `resnet50_exclude_glide_step[200000]_converted.pth`
- `resnet50_exclude_vqdm_step[200000]_converted.pth`

### 4.2 Stay-Positive

当前 `Stay-Positive` 建议保留的核心权重为：

- `checkpoints/stay_positive/corvi-staypos.pth`
- `checkpoints/stay_positive/rajan-staypos.pth`

并通过：

```text
stay_positive/test_code/weights/
```

中的配置和软链接或复制方式接入。

## 5. 脚本资产

### 5.1 FSD

当前已建议保留的 `FSD` 运行脚本包括：

- `run_fsd_eval.slurm`
- `run_fsd_eval_sd.slurm`
- `run_fsd_eval_adm.slurm`
- `run_fsd_eval_biggan.slurm`
- `run_fsd_eval_glide.slurm`
- `run_fsd_eval_vqdm.slurm`

以及 `fsd/scripts/` 下对应的：

- `eval.sh`
- `eval_sd.sh`
- `eval_adm.sh`
- `eval_biggan.sh`
- `eval_glide.sh`
- `eval_vqdm.sh`

### 5.2 Stay-Positive

当前建议保留的 `Stay-Positive` 运行脚本包括：

- `run_stay_positive_midjourney.slurm`
- `run_stay_positive_sd.slurm`
- `run_stay_positive_adm.slurm`

以及：

- `stay_positive/test_code/create_csv.py`
- `stay_positive/test_code/main.py`
- `stay_positive/test_code/eval.py`

其中 `create_csv.py` 已修复为大小写无关的图片后缀识别方式，可兼容 `.PNG` 等大写后缀。

### 5.3 LVLM

当前 `LVLM` 相关资产以论文与方案文档为主，后续建议保留：

- `docs/lvlm_integration_notes.md`
- `docs/lvlm_case_analysis_plan.md`
- `docs/lvlm_prompt_templates.md`
- `docs/lvlm_candidate_sample_template.md`
- `docs/lvlm_case_record_template.md`
- 论文主稿中与 `LVLM` 对应的相关研究、方法定位和后续计划章节
- 若后续补做轻量案例分析，再额外保留提示词模板、输入样本清单和分析记录

## 6. 结果资产

当前建议保留的关键结果来源包括：

- `logs/` 下所有正式实验日志
- `stay_positive_runs/` 下生成的 CSV 和分数文件
- 论文主稿中的结果表
- [docs/experiment_results_summary.md](/C:/Coding/260402_AI-image-forgery-recognition/docs/experiment_results_summary.md)

对于 `LVLM`，当前阶段的“结果资产”主要不是数值表，而是：

- 方法定位说明
- 适用场景定义
- 轻量案例分析的预留位置

其中，最终对外汇报和论文引用时，应优先以：

- 主稿中的结果表
- 结果总表文档

作为统一结果来源，避免反复翻查原始日志。

## 7. 当前阶段建议

从当前项目进度看，后续最值得继续保留和维护的是：

- 论文主稿
- 结果总表
- 可直接运行的脚本
- 已整理好的 `GenImage` 主数据目录
- converted checkpoint
- `LVLM` 集成说明文档与后续案例分析入口
- `LVLM` 案例方案与提示词模板
- `LVLM` 候选样本模板与正式案例记录模板

而不需要继续投入额外精力去维护大量早期草稿、重复目录或过程性中间材料。

## 8. 当前可执行结论

- 论文主稿已经具备继续收尾和最终整理的基础。
- 实验结果已经足够支撑当前阶段论文初稿。
- `LVLM` 已经需要作为正式研究线被维护，因此相关说明文档与后续验证入口也应纳入保留范围。
- 当前更适合进入“留档、收束、统一口径、补足 LVLM 结构”阶段，而不是继续无边界扩展实验任务。
