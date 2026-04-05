#!/bin/bash
#SBATCH -J sp_mj_eval
#SBATCH -A mfk-gsr2
#SBATCH -p plcyf-gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH -t 02:00:00
#SBATCH -o logs/stay_positive_mj_%j.out
#SBATCH -e logs/stay_positive_mj_%j.err

cd /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition

mkdir -p logs
mkdir -p stay_positive_runs

cd stay_positive/test_code

../../.venv/bin/python main.py \
  --in_csv ../../stay_positive_runs/real_val.csv \
  --out_csv ../../stay_positive_runs/real_scores.csv \
  --device cuda:0 \
  --weights_dir ./weights \
  --models corvi-plus,rajan-ours-plus

../../.venv/bin/python main.py \
  --in_csv ../../stay_positive_runs/midjourney_val.csv \
  --out_csv ../../stay_positive_runs/fake_scores.csv \
  --device cuda:0 \
  --weights_dir ./weights \
  --models corvi-plus,rajan-ours-plus

../../.venv/bin/python eval.py \
  --real ../../stay_positive_runs/real_scores.csv \
  --fake ../../stay_positive_runs/fake_scores.csv \
  --ix 2
