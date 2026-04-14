#!/bin/bash
#SBATCH -J adm_export
#SBATCH -A mfk-gsr2
#SBATCH -p plcyf-gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH -t 12:00:00
#SBATCH -o logs/adm_sample_export_%j.out
#SBATCH -e logs/adm_sample_export_%j.err

cd /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition

mkdir -p logs
mkdir -p analysis

cd fsd

../.venv/bin/python export_sample_scores.py \
  --data_root ../data/GenImage \
  --test_class ADM \
  --ckpt_path ../checkpoints/fsd/resnet50_exclude_adm_step[200000]_converted.pth \
  --output_csv ../analysis/adm_official_fsd.csv \
  --num_support 5 \
  --query_batch_size 64 \
  --use_fp16 True \
  --device cuda

../.venv/bin/python export_sample_scores.py \
  --data_root ../data/GenImage \
  --test_class ADM \
  --ckpt_path ./output/finetune_adm_stage1/ckpt/resnet50_step[10000].pth \
  --output_csv ../analysis/adm_finetune_v1.csv \
  --num_support 5 \
  --query_batch_size 64 \
  --use_fp16 True \
  --device cuda

../.venv/bin/python export_sample_scores.py \
  --data_root ../data/GenImage \
  --test_class ADM \
  --ckpt_path ./output/finetune_adm_stage2/ckpt/resnet50_step[5000].pth \
  --output_csv ../analysis/adm_finetune_v2.csv \
  --num_support 5 \
  --query_batch_size 64 \
  --use_fp16 True \
  --device cuda

cd ..

./.venv/bin/python tools/build_adm_sample_export.py \
  --official_csv analysis/adm_official_fsd.csv \
  --finetune_v1_csv analysis/adm_finetune_v1.csv \
  --finetune_v2_csv analysis/adm_finetune_v2.csv \
  --stay_positive_val_csv stay_positive_runs/adm_val.csv \
  --stay_positive_scores_csv stay_positive_runs/adm_scores.csv \
  --stay_positive_model rajan-ours-plus \
  --output_csv analysis/adm_sample_export.csv
