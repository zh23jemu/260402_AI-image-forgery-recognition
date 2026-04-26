# 三模型联合训练技术方案

## 1. 目标定义

客户当前要求的“三模型联合训练”，不能再表述为：

- 只是分别复现 `FSD`
- 分别测试 `Stay-Positive`
- 再把 `LVLM` 用作案例观察

而应升级为：

- 以 `FSD` 作为主干检测网络
- 以 `Stay-Positive` 的判别思想作为训练约束来源
- 以 `LVLM` 产生的高层语义证据作为辅助监督或难样本引导
- 在统一训练流程下形成一个新的联合模型或联合训练框架

因此，本文后续方法的核心贡献不再是“三条路线对比”，而是“如何把三条路线组织成一个可训练、可解释、可验证的统一框架”。

## 2. 三个模型在联合框架中的角色

### 2.1 FSD：联合框架主干

`FSD` 是当前最适合承担主干角色的方法，原因有三点：

- 它已经具备现成的训练脚本和 few-shot / prototypical learning 框架
- 它的研究重点本身就指向未知生成器泛化，符合论文主线
- 当前仓库中 `fsd/train.py` 已经可运行，改造成本最低

在联合训练中，`FSD` 负责：

- 提取统一视觉特征
- 完成主分类任务
- 维持对未知生成器场景的泛化能力

### 2.2 Stay-Positive：鲁棒判别约束分支

`Stay-Positive` 在联合框架中不建议直接作为第二个完整大主干与 `FSD` 并行反传，因为这样训练成本高、调试复杂、论文也不容易解释。

更合理的做法是把它转化为：

- 判别偏好约束来源
- teacher 分数来源
- 或 feature regularization 来源

在联合训练中，`Stay-Positive` 的职责是：

- 提供“不要过度依赖真实图像特征”的鲁棒判别偏置
- 在样本级上为 `FSD` 提供额外的 fake-oriented 监督信号
- 帮助主干模型减少把“更像真实图像”误判成“真实”的风险

### 2.3 LVLM：语义监督与难样本解释接口

`LVLM` 现阶段也不适合作为第三个端到端大模型一起反向传播训练，原因是：

- 资源成本高
- 提示词敏感
- 输出不稳定
- 当前仓库并没有现成的 LVLM 训练链路

因此第一版联合训练中，`LVLM` 的更稳定位是：

- 离线语义标签生成器
- 难样本筛选器
- 局部异常描述器
- 训练后分析与案例解释接口

其在联合框架中的作用包括：

- 为冲突样本生成结构化语义标签
- 为高风险误判样本提供“局部异常类型”提示
- 为训练集中的难样本分配更高权重
- 在论文中解释联合模型为什么在某些复杂样本上优于单模型

## 3. 建议采用的联合训练范式

## 3.1 不推荐方案：三大模型完全并行联合反传

即：

- `FSD` 主干
- `Stay-Positive` 主干
- `LVLM` 主干
- 三者端到端同时训练

不推荐原因：

- 工程复杂度远超当前项目节奏
- 训练资源压力过大
- 调参空间过大，短期很难收敛
- 论文虽然“看起来很大”，但实际很容易做不完

## 3.2 推荐方案：主干 + 判别约束 + 语义辅助的分层联合

第一版建议采用如下结构：

1. `FSD` 作为唯一在线训练主干
2. `Stay-Positive` 作为离线 teacher 或分数监督来源
3. `LVLM` 作为离线语义辅助标签来源
4. 三者通过损失函数和样本权重在同一训练流程中联合

这条路线的优点是：

- 能明确称为“三模型联合训练”
- 与现有代码和数据资产衔接最好
- 更容易在短期内拿到第一版实验结果
- 论文中的方法叙述更清晰

## 4. 第一版联合模型结构

## 4.1 输入

训练输入包含四类信息：

- 原始图像 `x`
- 图像真假标签 `y`
- `Stay-Positive` 离线分数 `s_sp`
- `LVLM` 离线语义标签 `z_lvlm`

其中：

- `s_sp` 可以是 fake score、校准后的概率、或 teacher logits
- `z_lvlm` 可以是离散标签或 one-hot / multi-hot 标签，例如：
  - `text_artifact`
  - `layout_inconsistency`
  - `local_structure_error`
  - `biological_detail_abnormal`
  - `over_smoothing_or_patch`

## 4.2 主干网络

使用 `FSD` 当前的 `resnet50` encoder 作为视觉 backbone，并保留其原始 prototypical learning 框架。

主干输出三部分：

1. `f(x)`：视觉特征
2. `p_cls(x)`：真假分类输出
3. `p_aux(x)`：语义辅助输出

其中：

- `p_cls(x)` 用于真假分类
- `p_aux(x)` 用于预测 LVLM 生成的辅助语义标签

## 4.3 联合损失

第一版联合损失建议写成：

```text
L_total = L_fsd + λ1 * L_sp + λ2 * L_lvlm + λ3 * L_hard
```

各项含义如下。

### `L_fsd`

主任务损失，沿用 `FSD` 当前的 prototypical loss / classification loss。

职责：

- 保持主任务能力
- 保持 few-shot 泛化主线

### `L_sp`

`Stay-Positive` 约束损失，建议采用以下两种之一：

1. 分数蒸馏损失
2. 排序一致性损失

较稳的第一版是分数蒸馏：

```text
L_sp = KL(p_cls(x) || p_sp(x))
```

或对 fake score 做 MSE / BCE 约束：

```text
L_sp = MSE(sigmoid(logit_fsd), calibrated_score_sp)
```

核心目的是：

- 让 `FSD` 对 fake 样本的响应更接近 `Stay-Positive` 的判别趋势
- 尤其在 `ADM` 这类冲突样本上减少“整体自然感误导”

### `L_lvlm`

`LVLM` 语义辅助损失，建议采用多标签 BCE：

```text
L_lvlm = BCE(p_aux(x), z_lvlm)
```

作用是：

- 让主干特征不仅学“真假”
- 还学“为什么可能是假”
- 提升难样本上的局部异常敏感度

### `L_hard`

难样本加权损失。

对以下样本提高权重：

- `FSD` 与 `Stay-Positive` 冲突样本
- `LVLM` 标记为高风险异常的样本
- 当前模型训练中持续误判的样本

简单实现可以是：

- 对样本赋权 `w_i`
- 在 `L_fsd` 上做 weighted loss

## 5. 联合训练数据构造

## 5.1 基础训练集

基础训练集仍来自 `GenImage`：

- `real`
- `ADM`
- `BigGAN`
- `GLIDE`
- `Midjourney`
- `SD`
- `VQDM`

## 5.2 Stay-Positive 辅助标签

对训练图像或至少对关键训练子集，提前离线跑出：

- `stay_positive_score`
- `stay_positive_prediction`
- 校准后概率

并保存成统一 CSV / parquet：

```text
image_path,label,sp_score,sp_prob,sp_pred
```

## 5.3 LVLM 辅助标签

对优先子集做离线标注：

- 优先标注 `ADM`
- 优先标注 FSD 与 SP 冲突样本
- 优先标注高不确定度样本

标签格式建议：

```text
image_path,label,
has_text_artifact,
has_layout_conflict,
has_local_structure_error,
has_bio_detail_error,
has_patch_or_smoothing,
lvlm_confidence
```

## 5.4 第一版不必全量 LVLM 标注

为降低成本，第一版建议：

- 全量使用 `Stay-Positive` 离线分数
- 仅对高价值子集使用 `LVLM` 标签

这样已经足以构成真正的三模型联合训练。

## 6. 第一版联合训练流程

### 阶段 A：构造 teacher 与辅助标签

1. 用 `Stay-Positive` 对训练集或关键子集导出分数
2. 用 `LVLM` 对冲突样本和难样本生成语义标签
3. 合并为统一训练 metadata

### 阶段 B：改造 FSD 训练脚本

在 `fsd/train.py` 基础上增加：

- 读取样本级 metadata
- 读取 `sp_score`
- 读取 `lvlm_label`
- 增加联合损失

### 阶段 C：先跑最小子集验证

建议先只跑：

- `ADM`
- `Midjourney`
- `SD`
- `real`

原因：

- 当前论文讨论最集中的是 `ADM`
- `Midjourney` / `SD` 可提供稳定对照
- 训练成本更可控

### 阶段 D：跑第一版正式结果

比较对象至少包括：

1. `FSD official`
2. `FSD finetune`
3. `FSD + SP joint`
4. `FSD + SP + LVLM joint`

## 7. 联合方案的论文创新点

如果该方案落地，论文中的创新点可以从“单纯复现比较”升级为以下三点：

### 创新点 1：三路线统一建模

首次在本项目框架下，将：

- 未知生成器泛化
- 判别依据稳定性
- 复杂样本语义解释

组织为统一训练与分析框架。

### 创新点 2：鲁棒判别约束引入 FSD 主干

把 `Stay-Positive` 的 fake-oriented 判别思想，从单独方法转化为 `FSD` 主干的训练约束。

### 创新点 3：LVLM 参与训练监督而非只做文书分析

使 `LVLM` 从“后验案例描述工具”升级为“训练阶段的语义辅助监督来源”。

## 8. 风险与控制

## 8.1 主要风险

- `LVLM` 标签噪声较大
- `Stay-Positive` 分数跨域不稳定
- 多损失联合后训练不收敛
- 当前 few-shot 框架接入样本级辅助标签需要改造

## 8.2 控制策略

- 先做 `FSD + SP`，再叠加 `LVLM`
- 先做 `ADM` 和少量类别，不直接全量
- 先做离线标签，不做在线 LVLM 推理
- 先做一版最小可运行结果，再逐步增强

## 9. 最终建议

最合理的执行顺序是：

1. 先把 `FSD + Stay-Positive` 联合损失跑通
2. 再把 `LVLM` 语义标签作为辅助头加入
3. 最后补充联合前后案例分析与论文主结果表

这样做的好处是：

- 技术上能落地
- 论文上能称为三模型联合训练
- 风险可控
- 与当前仓库和已有结果的衔接最好
