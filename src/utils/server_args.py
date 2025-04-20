import argparse
import pprint
from loguru import logger


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")

    parser.add_argument("--port", type=int, default=5000)
    return parser.parse_args()


ARGS = parse_args()
logger.info(f"Server arguments: {pprint.pformat(vars(ARGS))}")
