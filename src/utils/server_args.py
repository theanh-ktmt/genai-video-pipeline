import argparse
import pprint
from loguru import logger


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address")
    parser.add_argument("--port", type=int, default=5000, help="Port number")
    parser.add_argument(
        "--mock-video-generation",
        action="store_true",
        help="Whether to run mock video generation or not",
    )
    parser.add_argument(
        "--llm",
        type=str,
        default="gemini",
        choices=["gemini"],
        help="LLM model to use",
    )
    parser.add_argument(
        "--video-generation-model",
        type=str,
        default="mochi",
        choices=["mochi"],
        help="Video generation model to use",
    )
    parser.add_argument(
        "--max-batch-size",
        type=int,
        default=4,
        help="Maximum number of prompts to process in parallel",
    )
    parser.add_argument(
        "--batch-interval",
        type=int,
        default=1,
        help="Interval in seconds between batches of prompts",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=0.1,
        help="Interval in seconds to poll the request queue",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "--parallel-size",
        type=int,
        default=1,
        help="Number of GPUs to use for processing",
    )
    parser.add_argument(
        "--num-frames",
        type=int,
        default=84,
        help="Number of frames to generate for each video",
    )
    parser.add_argument(
        "--num-inference-steps",
        type=int,
        default=64,
        help="Number of inference steps for video generation",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second for the generated video",
    )
    parser.add_argument(
        "--enhance-prompts",
        action="store_true",
        help="Whether to enhance the prompt using LLM or not",
    )
    return parser.parse_args()


ARGS = parse_args()
logger.info(f"Server arguments: \n{pprint.pformat(vars(ARGS))}")
