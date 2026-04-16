# 图片同步命令清单

本地目标目录：`analysis/adm_conflict_priority5_images`

## 1. 服务器侧复制命令

```bash
mkdir -p analysis/adm_conflict_priority5_images
cp /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/421_adm_153.PNG analysis/adm_conflict_priority5_images/adm_conflict_priority_01_421_adm_153.PNG
cp /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/508_adm_174.PNG analysis/adm_conflict_priority5_images/adm_conflict_priority_02_508_adm_174.PNG
cp /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/531_adm_153.PNG analysis/adm_conflict_priority5_images/adm_conflict_priority_03_531_adm_153.PNG
cp /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/153_adm_153.PNG analysis/adm_conflict_priority5_images/adm_conflict_priority_04_153_adm_153.PNG
cp /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/548_adm_174.PNG analysis/adm_conflict_priority5_images/adm_conflict_priority_05_548_adm_174.PNG
```

## 2. 服务器侧打包命令

```bash
mkdir -p analysis/adm_conflict_priority5_images
cp /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/421_adm_153.PNG analysis/adm_conflict_priority5_images/adm_conflict_priority_01_421_adm_153.PNG
cp /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/508_adm_174.PNG analysis/adm_conflict_priority5_images/adm_conflict_priority_02_508_adm_174.PNG
cp /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/531_adm_153.PNG analysis/adm_conflict_priority5_images/adm_conflict_priority_03_531_adm_153.PNG
cp /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/153_adm_153.PNG analysis/adm_conflict_priority5_images/adm_conflict_priority_04_153_adm_153.PNG
cp /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/548_adm_174.PNG analysis/adm_conflict_priority5_images/adm_conflict_priority_05_548_adm_174.PNG
tar -czf analysis/adm_conflict_priority5_images.tar.gz -C analysis adm_conflict_priority5_images
```

## 3. Windows 本地建议落点

```text
analysis/adm_conflict_priority5_images
```

## 4. 当前图片列表

| case_id | sample_id | server_image_path | local_filename |
| --- | --- | --- | --- |
| adm_conflict_priority_01 | adm_auto_2143 | /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/421_adm_153.PNG | adm_conflict_priority_01_421_adm_153.PNG |
| adm_conflict_priority_02 | adm_auto_2720 | /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/508_adm_174.PNG | adm_conflict_priority_02_508_adm_174.PNG |
| adm_conflict_priority_03 | adm_auto_2875 | /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/531_adm_153.PNG | adm_conflict_priority_03_531_adm_153.PNG |
| adm_conflict_priority_04 | adm_auto_0355 | /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/153_adm_153.PNG | adm_conflict_priority_04_153_adm_153.PNG |
| adm_conflict_priority_05 | adm_auto_2984 | /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/548_adm_174.PNG | adm_conflict_priority_05_548_adm_174.PNG |

## 5. 备注

- 若在服务器项目根目录 `/net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition` 下执行，建议把图片放入 `analysis/adm_conflict_priority5_images` 对应的相对目录后再打包。