
OUTPUT_PATH='./output_dir'
SEED=42

# test class
TEST_CLASS="Midjourney"

CKPT_PATH="../checkpoints/fsd/resnet50_exclude_midjourney_step[200000]_converted.pth"

data_root=(
    "../data/GenImage" \
)

# execution
../.venv/bin/python test.py \
    --data_root "$data_root" \
    --test_class $TEST_CLASS \
    --ckpt_path $CKPT_PATH \
    --num_workers 0 \
    --seed $SEED \
    --use_fp16 False \
