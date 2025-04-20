import threading
import time
import queue
from loguru import logger

import torch

from src.utils.server_args import ARGS
from src.utils.common import seed_everything
from src.models.pipeline import VideoGenerationPipeline


class WorkerThread(threading.Thread):
    def __init__(
        self,
        gpu_id: int,
        request_queue: queue.Queue,
        result_queue: queue.Queue,
    ):
        super().__init__()
        seed_everything(ARGS.seed)
        self.gpu_id = gpu_id
        self.pipe = VideoGenerationPipeline(self.gpu_id)

        self.request_queue = request_queue
        self.result_queue = result_queue
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            time.sleep(ARGS.batch_interval)  # time to batch request

            # pop all available prompts (up to max_batch_size)
            batch = []
            while len(batch) < ARGS.max_batch_size:
                try:
                    request_id, prompt = self.request_queue.get(
                        timeout=ARGS.poll_interval
                    )
                    batch.append((request_id, prompt))
                except queue.Empty:
                    break  # no more prompts in the queue

            if not batch:
                continue  # o prompts to process
            logger.info(f"Processing batch of size {len(batch)} on GPU {self.gpu_id}")

            # extract request_ids and prompts
            request_ids, prompts = zip(*batch)
            video_buffers = self.pipe.generate(prompts)

            # send results to the result queue
            logger.success(
                f"Finished processing batch of size {len(batch)} on GPU {self.gpu_id}"
            )
            for request_id, video_buffer in zip(request_ids, video_buffers):
                self.result_queue.put((request_id, video_buffer))

    def stop(self):
        self.stop_event.set()
        self.join()
        logger.success(f"Worker thread on GPU {self.gpu_id} stopped.")
