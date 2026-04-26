# 联合训练元数据规范

## 1. 文档目标

本规范用于定义三模型联合训练所需的统一样本级元数据格式。

它的作用是把以下三类信息合并到同一个训练入口中：

- 主任务真假标签
- `Stay-Positive` 离线分数
- `LVLM` 离线语义标签

后续代码侧建议统一读取一个主表，例如：

- `analysis/joint_training_metadata.csv`

## 2. 总体原则

设计这份表时遵循以下原则：

1. 先保证 `FSD + SP` 最小闭环可跑
2. `LVLM` 字段允许先部分缺失
3. 所有字段都尽量样本级对齐
4. 便于后续扩展到更多类别和更多辅助监督

## 3. 第一版推荐字段

第一版推荐使用以下字段：

| 字段名 | 类型 | 含义 |
| --- | --- | --- |
| `image_path` | string | 图像绝对路径 |
| `split` | string | `train / val / test` |
| `generator` | string | `real / ADM / SD / Midjourney / ...` |
| `label` | int | `0=real, 1=fake` |
| `subset_tag` | string | 可选，如 `adm_core`, `adm_conflict`, `standard` |
| `sp_score_raw` | float | `Stay-Positive` 原始分数 |
| `sp_prob_calibrated` | float | 校准后的 fake 概率 |
| `sp_pred_default` | int | 默认阈值预测 |
| `sp_pred_calibrated` | int | 校准后预测 |
| `sp_conflict_flag` | int | 是否与当前 FSD 基线冲突 |
| `fsd_base_pred` | int | 当前 FSD 基线预测 |
| `fsd_base_score` | float | 当前 FSD 基线分数 |
| `lvlm_has_text_artifact` | int | 是否存在伪文本/伪界面异常 |
| `lvlm_has_layout_conflict` | int | 是否存在布局/关系异常 |
| `lvlm_has_structure_error` | int | 是否存在局部结构连接异常 |
| `lvlm_has_bio_detail_error` | int | 是否存在生物体局部真实性不足 |
| `lvlm_has_patch_or_smooth` | int | 是否存在修补/过度平滑异常 |
| `lvlm_confidence` | float | LVLM 标签可信度 |
| `hard_weight` | float | 难样本训练权重 |

## 4. 最小闭环必需字段

如果先只做 `FSD + SP`，那么最小必需字段可缩减为：

| 字段名 | 是否必需 |
| --- | --- |
| `image_path` | 必需 |
| `split` | 必需 |
| `generator` | 必需 |
| `label` | 必需 |
| `sp_score_raw` | 必需 |
| `sp_prob_calibrated` | 必需 |
| `sp_conflict_flag` | 建议 |
| `hard_weight` | 建议 |

也就是说，`LVLM` 字段可以先留空，等第二阶段再补。

## 5. 推荐标签定义

### `label`

- `0` 表示真实图像
- `1` 表示伪造图像

### `sp_conflict_flag`

推荐定义为：

- `0`：当前样本不属于关键冲突样本
- `1`：当前样本属于 `Stay-Positive` 与 `FSD` 冲突样本

如果后续想做更细划分，也可以扩展为：

- `0`：无冲突
- `1`：`SP=fake, FSD=real`
- `2`：`SP=real, FSD=fake`

### `hard_weight`

推荐初值：

- 普通样本：`1.0`
- 冲突样本：`1.5`
- 高价值 `ADM` 难样本：`2.0`
- 同时具有 LVLM 异常标签的困难样本：`2.5`

## 6. LVLM 语义标签建议

第一版建议只保留少量高价值标签，不要做过细 taxonomy。

推荐保留 5 类：

1. `lvlm_has_text_artifact`
2. `lvlm_has_layout_conflict`
3. `lvlm_has_structure_error`
4. `lvlm_has_bio_detail_error`
5. `lvlm_has_patch_or_smooth`

原因：

- 与当前 `ADM` 案例观察结果高度一致
- 足以支撑辅助头训练
- 便于论文写作和人工复核

## 7. 推荐 CSV 示例

```csv
image_path,split,generator,label,subset_tag,sp_score_raw,sp_prob_calibrated,sp_pred_default,sp_pred_calibrated,sp_conflict_flag,fsd_base_pred,fsd_base_score,lvlm_has_text_artifact,lvlm_has_layout_conflict,lvlm_has_structure_error,lvlm_has_bio_detail_error,lvlm_has_patch_or_smooth,lvlm_confidence,hard_weight
C:/.../ADM/val/ai/0_adm_153.PNG,train,ADM,1,adm_core,0.4491,0.6123,0,1,1,0,0.3812,1,0,1,0,0,0.82,2.0
```

## 8. 文件组织建议

推荐把联合训练相关表放在：

- `analysis/joint_training_metadata.csv`

如果后续体量变大，可再拆成：

- `analysis/joint_train.csv`
- `analysis/joint_val.csv`
- `analysis/joint_test.csv`

## 9. 第一版生成顺序

建议按这个顺序生成元数据：

1. 先导出基础 `image_path / split / generator / label`
2. 再合并 `Stay-Positive` 分数
3. 再合并当前 `FSD` 基线结果
4. 再补 `LVLM` 标签
5. 最后生成 `hard_weight`

## 10. 当前建议

现在代码端最值得先做的，就是基于这份规范新建：

- `analysis/joint_training_metadata.csv`

只要这张表先出来，后续：

- `train_joint.py`
- 联合损失
- 消融实验

都会顺很多。
