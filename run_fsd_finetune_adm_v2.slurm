#!/bin/bash
#SBATCH -J fsd_ft_adm_v2
#SBATCH -A mfk-gsr2
#SBATCH -p plcyf-gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH -o logs/fsd_finetune_adm_v2_%j.out
#SBATCH -e logs/fsd_finetune_adm_v2_%j.err

cd /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition

mkdir -p logs
mkdir -p fsd/output/finetune_adm_stage2

cd fsd

export EXCLUDE_CLASS=ADM
export DATA_ROOT=../data/GenImage
export OUTPUT_PATH=./output/finetune_adm_stage2
export INIT_CKPT_PATH=../checkpoints/fsd/resnet50_exclude_adm_step[200000]_converted.pth
export GPU_NUM=1
export NUM_WORKERS=8
export BATCH_SIZE=16
export LR=5e-6
export TOTAL_TRAINING_STEPS=5000
export SAVE_INTERVAL=5000
export EVAL_INTERVAL=5000
export LOG_INTERVAL=500
export ACCUMULATION_STEPS=1
export USE_FP16=True
export PRETRAINED_BACKBONE=False

bash scripts/train.sh
