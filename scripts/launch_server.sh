#!/bin/bash
python3 src/app.py \
    --host 0.0.0.0 --port 5000 \
    --mock-video-generation \
    --parallel-size 2 \
    --max-batch-size 1 \
    --batch-interval 1 \
    --poll-interval 0.1 \q