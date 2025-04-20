import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from loguru import logger
from dotenv import load_dotenv
from src.models.mochi import MochiModel
from src.utils.video_utils import save_video_buffer

load_dotenv()
model = MochiModel(
    width=848,
    height=480,
    num_inference_steps=64,
    num_frames=84,
    fps=30,
)
prompts = [
    "A cat playing with a ball of yarn",
]

video_buffers = model.process_batched_prompts(prompts)
os.makedirs("videos", exist_ok=True)
for prompt, video_buffer in zip(prompts, video_buffers):
    if video_buffer:
        path = os.path.join("videos", f"{prompt}.mp4")
        save_video_buffer(video_buffer, path)
        logger.info(f"Video saved successfully to {path}.")
    else:
        logger.error(f"Video generation failed for prompt {prompt}.")
