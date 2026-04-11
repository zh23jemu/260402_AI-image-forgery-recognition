#!/bin/bash
#SBATCH -J fsd_train_adm
#SBATCH -A mfk-gsr2
#SBATCH -p plcyf-gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH -o logs/fsd_train_adm_%j.out
#SBATCH -e logs/fsd_train_adm_%j.err

cd /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition

mkdir -p logs
mkdir -p fsd/output/train_adm_stage1

cd fsd

export EXCLUDE_CLASS=ADM
export OUTPUT_PATH=./output/train_adm_stage1
export DATA_ROOT=../data/GenImage
export GPU_NUM=1
export NUM_WORKERS=8
export BATCH_SIZE=16
export LR=1e-4
export TOTAL_TRAINING_STEPS=50000
export ACCUMULATION_STEPS=1
export USE_FP16=True
export PRETRAINED_BACKBONE=False

bash scripts/train.sh
