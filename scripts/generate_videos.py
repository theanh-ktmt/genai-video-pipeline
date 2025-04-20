import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import time
import requests
from loguru import logger
from src.utils.prompt_utils import get_input_prompts


# configs
API_URL = "http://127.0.0.1:5000/generate"
PROMPTS = get_input_prompts()
OUTPUT_DIR = "videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def send_request_and_save_video(prompt):
    """Send a single request and save the video file"""
    logger.info(f"Sending request for: '{prompt}'")
    save_path = f"{OUTPUT_DIR}/{prompt[:50]}.mp4"
    start = time.time()

    try:
        response = requests.post(
            API_URL,
            json={"prompt": prompt},
            stream=True,
        )
        response.raise_for_status()

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.success(f"Video saved to {save_path}!")
        logger.info(
            f"Request for '{prompt}' completed in {time.time() - start:.2f} seconds."
        )

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to process '{prompt}': {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error with '{prompt}': {str(e)}")


for prompt in PROMPTS:
    send_request_and_save_video(prompt)
