import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from loguru import logger
from dotenv import load_dotenv
from src.models.gemini import GeminiModel
from src.utils.prompt_utils import get_input_prompts


load_dotenv()
model = GeminiModel(n_retry=3, timeout=20)
prompts = get_input_prompts()[:3]

answers = model.process_batch_prompts(prompts)
for prompt, answer in zip(prompts, answers):
    logger.info(f"Prompt: {prompt}\nAnswer: {answer}\n")
