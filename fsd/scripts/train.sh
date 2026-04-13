# example for training with 4 GPUs
# values can be overridden by environment variables in slurm scripts

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FSD_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$FSD_DIR/.." && pwd)"

GPU_NUM=${GPU_NUM:-1}
WORLD_SIZE=${WORLD_SIZE:-1}
NUM_WORKERS=${NUM_WORKERS:-8}
SEED=${SEED:-42}

DISTRIBUTED_ARGS="
    --nproc_per_node $GPU_NUM \
    --nnodes $WORLD_SIZE \
"

data_root=(
    "${DATA_ROOT:-$REPO_ROOT/data/GenImage}" \
)


OUTPUT_PATH=${OUTPUT_PATH:-$FSD_DIR/output_dir}

# test class
EXCLUDE_CLASS=${EXCLUDE_CLASS:-ADM}

BATCH_SIZE=${BATCH_SIZE:-16}
LR=${LR:-1e-4}
TOTAL_TRAINING_STEPS=${TOTAL_TRAINING_STEPS:-50000}
ACCUMULATION_STEPS=${ACCUMULATION_STEPS:-1}
USE_FP16=${USE_FP16:-True}
PRETRAINED_BACKBONE=${PRETRAINED_BACKBONE:-False}
INIT_CKPT_PATH=${INIT_CKPT_PATH:-}

# execution
OMP_NUM_THREADS=1 "$REPO_ROOT/.venv/bin/torchrun" $DISTRIBUTED_ARGS "$FSD_DIR/train.py" \
    --data_root "$data_root" \
    --output_dir $OUTPUT_PATH \
    --num_workers $NUM_WORKERS \
    --seed $SEED \
    --batch_size $BATCH_SIZE \
    --lr $LR \
    --exclude_class $EXCLUDE_CLASS \
    --total_training_steps $TOTAL_TRAINING_STEPS \
    --accumulation_steps $ACCUMULATION_STEPS \
    --use_fp16 $USE_FP16 \
    --pretrained_backbone $PRETRAINED_BACKBONE \
    --init_ckpt_path "$INIT_CKPT_PATH" \
