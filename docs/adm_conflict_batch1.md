# ADM 下一批冲突案例清单

筛选类型：`strong_conflict`

| case_id | sample_id | postcal_pred | official | v1 | v2 | score | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| adm_conflict_batch_01 | adm_auto_2143 | fake | real | real | real | 0.592478 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_02 | adm_auto_2720 | fake | real | real | real | 0.590573 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_03 | adm_auto_2875 | fake | real | real | real | 0.568101 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_04 | adm_auto_0355 | fake | real | real | real | 0.562310 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_05 | adm_auto_2984 | fake | real | real | real | 0.555450 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_06 | adm_auto_1421 | fake | real | real | real | 0.555412 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_07 | adm_auto_1390 | fake | real | real | real | 0.549081 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_08 | adm_auto_1383 | fake | real | real | real | 0.539390 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_09 | adm_auto_0280 | fake | real | real | real | 0.533666 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_10 | adm_auto_2252 | fake | real | real | real | 0.526472 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_11 | adm_auto_1438 | fake | real | real | real | 0.525240 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_12 | adm_auto_2693 | fake | real | real | real | 0.523895 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_13 | adm_auto_2537 | fake | real | real | real | 0.519793 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_14 | adm_auto_2573 | fake | real | real | real | 0.519691 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_15 | adm_auto_1102 | fake | real | real | real | 0.517705 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_16 | adm_auto_2052 | fake | real | real | real | 0.516421 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_17 | adm_auto_2606 | fake | real | real | real | 0.515026 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_18 | adm_auto_2408 | fake | real | real | real | 0.513585 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_19 | adm_auto_2382 | fake | real | real | real | 0.512472 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |
| adm_conflict_batch_20 | adm_auto_2235 | fake | real | real | real | 0.507450 | Stay-Positive 校准后判 fake，但 FSD 三个版本仍判 real，属于高价值互补案例。 |

## 简要说明

- 这批样本的共同特点是：`Stay-Positive` 在校准后已经稳定判为 `fake`，但 `FSD` 官方基线、首轮微调和第二轮保守微调仍全部判为 `real`。
- 因此，这批样本更适合作为“FSD 系统性盲区”与“方法互补性”分析入口。