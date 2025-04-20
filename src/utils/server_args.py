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
    return parser.parse_args()


ARGS = parse_args()
logger.info(f"Server arguments: \n{pprint.pformat(vars(ARGS))}")
