#!/bin/bash
#SBATCH -J joint_meta
#SBATCH -A mfk-gsr2
#SBATCH -p plcyf-gpu
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH -t 02:00:00
#SBATCH -o logs/joint_meta_%j.out
#SBATCH -e logs/joint_meta_%j.err

set -euo pipefail

cd /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition

mkdir -p logs
mkdir -p analysis

./.venv/bin/python tools/build_joint_training_metadata.py \
  --data_root data/GenImage \
  --output_csv analysis/joint_training_metadata.csv \
  --generators real,ADM,SD,Midjourney \
  --splits train,val \
  --sp_score_csv analysis/adm_sample_export_enriched.csv \
  --priority_fake_generators ADM
