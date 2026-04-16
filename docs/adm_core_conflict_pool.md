# ADM 核心冲突代表样本池

目标模式：`SP=fake;FSD=real/real/real`

| case_id | sample_id | prompt_type | score_bin | stay_positive_score | source_name |
| --- | --- | --- | --- | --- | --- |
| adm_core_conflict_01 | adm_auto_2143 | adm_153 | 0.58-0.60 | 0.592478 | 421_adm_153.PNG |
| adm_core_conflict_02 | adm_auto_2720 | adm_174 | 0.58-0.60 | 0.590573 | 508_adm_174.PNG |
| adm_core_conflict_03 | adm_auto_2875 | adm_153 | 0.56-0.58 | 0.568101 | 531_adm_153.PNG |
| adm_core_conflict_04 | adm_auto_0355 | adm_153 | 0.56-0.58 | 0.562310 | 153_adm_153.PNG |
| adm_core_conflict_05 | adm_auto_2984 | adm_174 | 0.54-0.56 | 0.555450 | 548_adm_174.PNG |
| adm_core_conflict_06 | adm_auto_1421 | adm_85 | 0.54-0.56 | 0.555412 | 312_adm_85.PNG |
| adm_core_conflict_07 | adm_auto_1390 | adm_7 | 0.54-0.56 | 0.549081 | 308_adm_7.PNG |
| adm_core_conflict_08 | adm_auto_1383 | adm_34 | 0.52-0.54 | 0.539390 | 307_adm_34.PNG |
| adm_core_conflict_09 | adm_auto_0280 | adm_7 | 0.52-0.54 | 0.533666 | 141_adm_7.PNG |
| adm_core_conflict_10 | adm_auto_2252 | adm_174 | 0.52-0.54 | 0.526472 | 438_adm_174.PNG |
| adm_core_conflict_11 | adm_auto_1438 | adm_7 | 0.52-0.54 | 0.525240 | 315_adm_7.PNG |
| adm_core_conflict_12 | adm_auto_2693 | adm_85 | 0.52-0.54 | 0.523895 | 503_adm_85.PNG |
| adm_core_conflict_13 | adm_auto_2537 | adm_85 | 0.50-0.52 | 0.519793 | 480_adm_85.PNG |
| adm_core_conflict_14 | adm_auto_2573 | adm_85 | 0.50-0.52 | 0.519691 | 486_adm_85.PNG |
| adm_core_conflict_15 | adm_auto_1102 | adm_7 | 0.50-0.52 | 0.517705 | 265_adm_7.PNG |
| adm_core_conflict_16 | adm_auto_2052 | adm_91 | 0.50-0.52 | 0.516421 | 407_adm_91.PNG |
| adm_core_conflict_17 | adm_auto_2606 | adm_174 | 0.50-0.52 | 0.515026 | 491_adm_174.PNG |
| adm_core_conflict_18 | adm_auto_2382 | adm_91 | 0.50-0.52 | 0.512472 | 457_adm_91.PNG |
| adm_core_conflict_19 | adm_auto_2235 | adm_34 | 0.50-0.52 | 0.507450 | 435_adm_34.PNG |
| adm_core_conflict_20 | adm_auto_2472 | adm_91 | 0.48-0.50 | 0.499560 | 470_adm_91.PNG |
| adm_core_conflict_21 | adm_auto_1377 | adm_34 | 0.48-0.50 | 0.493499 | 306_adm_34.PNG |
| adm_core_conflict_22 | adm_auto_2787 | adm_34 | 0.48-0.50 | 0.491388 | 518_adm_34.PNG |
| adm_core_conflict_23 | adm_auto_1266 | adm_91 | 0.48-0.50 | 0.490613 | 28_adm_91.PNG |
| adm_core_conflict_24 | adm_auto_2947 | adm_153 | 0.48-0.50 | 0.490231 | 542_adm_153.PNG |

## 说明

- 这批样本全部来自 `SP=fake;FSD=real/real/real` 的核心互补模式。
- 当前按 `prompt_type` 做均衡抽样，避免再次只看到单一模板。
- 这批样本适合继续做真实视觉观察、LVLM 分析或进一步图片同步。