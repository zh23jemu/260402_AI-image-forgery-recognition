# 强化版联合训练运行说明

## 1. 这轮训练的目的

这轮不是重复上一轮 `FSD + SP`，而是做一次“强针对性验证训练”，核心目的是回答两个问题：

1. `Stay-Positive` 约束是否真正进入了训练流程
2. 在更强约束下，结果是否开始偏离 `FSD-only` 并体现联合训练增益

## 2. 相比上一轮的主要变化

- `sp_loss_weight` 从 `0.3` 提高到 `2.0`
- `sp_loss_type` 从 `mse` 改为 `bce`
- `log_interval` 从 `500` 降到 `100`
- 新增更详细的联合训练调试日志：
  - `SP loss weight`
  - `SP loss type`
  - `valid_sp_samples`
  - `steps_with_valid_sp`
  - `avg_valid_sp_samples_per_step`
  - `Joint debug step=...`

## 3. 提交命令

```bash
sbatch run_fsd_joint_sp_stage1_strong.slurm
```

## 4. 重点查看命令

```bash
tail -f logs/fsd_joint_sp_stage1_strong_*.out logs/fsd_joint_sp_stage1_strong_*.err
```

```bash
grep -E "SP loss weight|Loaded joint metadata rows|Joint debug|valid_sp_samples|Save checkpoint|Evaluation on|Traceback|FAILED|Error" logs/fsd_joint_sp_stage1_strong_*.out logs/fsd_joint_sp_stage1_strong_*.err
```

## 5. 这轮训练后怎么判断是否有价值

### 情况 A：出现明显不同于 `FSD-only` 的结果

说明：

- `SP` 约束大概率真正起作用了
- 可以在论文里写成“强化版第一阶段联合训练开始体现约束效应”

### 情况 B：全局结果变化不大，但日志里 `valid_sp_samples` 和 `sp_loss` 明确非零

说明：

- `SP` 约束已经真实参与训练
- 当前问题不是“约束没进来”，而是“当前约束形式收益有限”
- 论文可写成“第一阶段完成约束链路验证，但增益有限”

### 情况 C：结果依旧与 `FSD-only` 几乎一致，且 `valid_sp_samples` 长期接近 0

说明：

- 当前 metadata 或约束链路可能没有真正生效
- 这会成为后续排查重点

## 6. 最后需要贴回来的结果

训练结束后，建议贴这三条输出：

```bash
sacct -j <JOBID> --format=JobID,State,ExitCode,Elapsed
```

```bash
grep -E "Joint debug|valid_sp_samples|Save checkpoint|Evaluation on ADM done|Evaluation on SD done|Evaluation on Midjourney done|Traceback|FAILED|Error" logs/fsd_joint_sp_stage1_strong_<JOBID>.out logs/fsd_joint_sp_stage1_strong_<JOBID>.err
```

```bash
ls -lh fsd/output/joint_sp_stage1_strong/ckpt
```
