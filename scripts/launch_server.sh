#!/bin/bash
python3 src/app.py \
    --host 0.0.0.0 --port 5000 \
    --parallel-size 1 \
    --max-batch-size 1 \
    --batch-interval 1 \
    --poll-interval 0.1 \
    --num-frames 84 \
    --num-inference-steps 64 \
    --fps 30 --seed 2025 \
    --enhance-prompt \
    # --mock-video-generation \