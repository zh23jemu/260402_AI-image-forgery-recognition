#!/bin/bash
#SBATCH -J fsd_eval_adm
#SBATCH -A mfk-gsr2
#SBATCH -p plcyf-gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH -t 04:00:00
#SBATCH -o logs/fsd_eval_adm_%j.out
#SBATCH -e logs/fsd_eval_adm_%j.err

cd /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition

mkdir -p logs

cd fsd
bash scripts/eval_adm.sh
