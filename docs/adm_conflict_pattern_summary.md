# ADM 冲突模式结构化统计

校准阈值：`0.388818`

## 1. 关键发现

- 总样本数为 `3000`，其中 `Stay-Positive` 校准后与三组 FSD 全冲突的样本数为 `1241`。
- 最主要的冲突模式为 `SP=fake;FSD=real/real/real`，共 `1137` 个样本，对应 Stay-Positive 平均分数约为 `0.4202`。
- 按文件名模板统计，`adm_34` 是当前最密集的冲突模板之一，其主导冲突模式为 `SP=fake;FSD=real/real/real`，样本数为 `200`。
- `Stay-Positive` 校准后判 `fake` 且三组 FSD 全判 `real` 的样本共有 `1137` 个，这是当前最值得优先解释的互补性子集。

## 2. 冲突模式 Top 10

| conflict_pattern | sample_count | mean_sp_score | min_sp_score | max_sp_score |
| --- | --- | --- | --- | --- |
| SP=fake;FSD=real/real/real | 1137 | 0.4202 | 0.3888 | 0.5925 |
| SP=fake;FSD=fake/fake/fake | 874 | 0.4419 | 0.3889 | 0.7573 |
| SP=real;FSD=real/real/real | 252 | 0.3800 | 0.3604 | 0.3888 |
| SP=fake;FSD=real/real/fake | 156 | 0.4199 | 0.3889 | 0.5254 |
| SP=real;FSD=fake/fake/fake | 104 | 0.3814 | 0.3661 | 0.3887 |
| SP=fake;FSD=fake/fake/real | 97 | 0.4286 | 0.3889 | 0.5654 |
| SP=fake;FSD=real/fake/fake | 88 | 0.4458 | 0.3889 | 0.6606 |
| SP=fake;FSD=real/fake/real | 69 | 0.4423 | 0.3897 | 0.6126 |
| SP=fake;FSD=fake/real/real | 67 | 0.4184 | 0.3888 | 0.5106 |
| SP=fake;FSD=fake/real/fake | 61 | 0.4226 | 0.3891 | 0.5167 |

## 3. prompt_type Top 10

| prompt_type | conflict_pattern | sample_count | mean_sp_score |
| --- | --- | --- | --- |
| adm_34 | SP=fake;FSD=real/real/real | 200 | 0.4200 |
| adm_7 | SP=fake;FSD=real/real/real | 191 | 0.4193 |
| adm_85 | SP=fake;FSD=real/real/real | 190 | 0.4200 |
| adm_153 | SP=fake;FSD=real/real/real | 187 | 0.4202 |
| adm_174 | SP=fake;FSD=real/real/real | 185 | 0.4225 |
| adm_91 | SP=fake;FSD=real/real/real | 184 | 0.4193 |
| adm_91 | SP=fake;FSD=fake/fake/fake | 162 | 0.4386 |
| adm_34 | SP=fake;FSD=fake/fake/fake | 147 | 0.4428 |
| adm_85 | SP=fake;FSD=fake/fake/fake | 145 | 0.4404 |
| adm_7 | SP=fake;FSD=fake/fake/fake | 142 | 0.4434 |

## 4. 分数区间 Top 15

| score_bin | conflict_pattern | sample_count | min_sp_score | max_sp_score |
| --- | --- | --- | --- | --- |
| 0.36-0.38 | SP=real;FSD=real/real/real | 103 | 0.3604 | 0.3800 |
| 0.36-0.38 | SP=real;FSD=fake/fake/fake | 36 | 0.3661 | 0.3800 |
| 0.36-0.38 | SP=real;FSD=real/real/fake | 13 | 0.3717 | 0.3797 |
| 0.36-0.38 | SP=real;FSD=fake/fake/real | 11 | 0.3647 | 0.3791 |
| 0.36-0.38 | SP=real;FSD=fake/real/real | 9 | 0.3670 | 0.3789 |
| 0.36-0.38 | SP=real;FSD=fake/real/fake | 6 | 0.3688 | 0.3774 |
| 0.36-0.38 | SP=real;FSD=real/fake/fake | 3 | 0.3661 | 0.3761 |
| 0.36-0.38 | SP=real;FSD=real/fake/real | 2 | 0.3726 | 0.3783 |
| 0.38-0.40 | SP=fake;FSD=real/real/real | 272 | 0.3888 | 0.3999 |
| 0.38-0.40 | SP=real;FSD=real/real/real | 149 | 0.3800 | 0.3888 |
| 0.38-0.40 | SP=fake;FSD=fake/fake/fake | 109 | 0.3889 | 0.4000 |
| 0.38-0.40 | SP=real;FSD=fake/fake/fake | 68 | 0.3802 | 0.3887 |
| 0.38-0.40 | SP=fake;FSD=real/real/fake | 37 | 0.3889 | 0.3991 |
| 0.38-0.40 | SP=fake;FSD=fake/fake/real | 23 | 0.3889 | 0.3999 |
| 0.38-0.40 | SP=fake;FSD=fake/real/real | 18 | 0.3888 | 0.3990 |