#!/bin/bash
#SBATCH -J fsd_joint_s2
#SBATCH -A mfk-gsr2
#SBATCH -p plcyf-gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH -o logs/fsd_joint_stage2_min_%j.out
#SBATCH -e logs/fsd_joint_stage2_min_%j.err

set -euo pipefail

cd /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition

mkdir -p logs
mkdir -p fsd/output/joint_stage2_min

export GPU_NUM=1
export WORLD_SIZE=1
export NUM_WORKERS=8
export SEED=42

cd fsd

OMP_NUM_THREADS=1 ../.venv/bin/torchrun \
  --nproc_per_node $GPU_NUM \
  --nnodes $WORLD_SIZE \
  train_joint.py \
  --data_root ../data/GenImage \
  --output_dir ./output/joint_stage2_min \
  --num_workers $NUM_WORKERS \
  --seed $SEED \
  --batch_size 16 \
  --lr 1e-5 \
  --total_training_steps 10000 \
  --save_interval 5000 \
  --eval_interval 5000 \
  --log_interval 500 \
  --accumulation_steps 1 \
  --use_fp16 True \
  --pretrained_backbone False \
  --init_ckpt_path ../checkpoints/fsd/resnet50_exclude_adm_step[200000]_converted.pth \
  --train_generators real,ADM,SD,Midjourney \
  --real_class_name real \
  --metadata_csv ../analysis/joint_training_metadata_stage2.csv \
  --sp_loss_weight 0.3 \
  --sp_loss_type mse \
  --force_real_in_task True \
  --eval_generators ADM,SD,Midjourney \
  --enable_lvlm_head True \
  --lvlm_loss_weight 0.2 \
  --lvlm_loss_on_fake_only True
