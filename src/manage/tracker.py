import threading
import queue
import time
from loguru import logger
from src.utils.server_args import ARGS


class ResultTracker(threading.Thread):
    def __init__(self, result_queue: queue.Queue):
        super().__init__()
        self.result_queue = result_queue
        self.stop_event = threading.Event()
        self.result_lock = threading.Lock()
        self.results = {}

    def run(self):
        while not self.stop_event.is_set():
            time.sleep(ARGS.poll_interval)  # wait for results
            try:
                request_id, result = self.result_queue.get(timeout=ARGS.poll_interval)
                with self.result_lock:  # thread-safe access to results
                    self.results[request_id] = result
            except queue.Empty:
                pass

    def remove_request(self, request_id: str):
        with self.result_lock:
            del self.results[request_id]

    def stop(self):
        self.stop_event.set()
        self.join()
        logger.success("Result tracker thread stopped.")
