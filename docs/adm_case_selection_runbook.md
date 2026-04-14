# ADM 案例筛选运行说明

## 1. 用途

这份说明用于指导如何从已经生成的 `analysis/adm_sample_export.csv` 中进一步筛出首批 `ADM` 案例。

## 2. 推荐做法

优先在服务器上运行：

```bash
./.venv/bin/python tools/select_adm_case_candidates.py \
  --input_csv analysis/adm_sample_export.csv \
  --output_csv analysis/adm_case_candidates.csv \
  --top_k 20
```

## 3. 跑完后检查

```bash
ls -lh analysis/adm_case_candidates.csv
head -10 analysis/adm_case_candidates.csv
```

## 4. 当前建议

第一次筛样时，建议优先找三类：

1. `v2_regression`
2. `model_conflict`
3. `borderline_case`

这样最容易把首批 `6` 个案例补齐。
