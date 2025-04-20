from loguru import logger
import queue
import time
from src.utils.server_args import ARGS
from src.manage.worker import WorkerThread
from src.manage.tracker import ResultTracker
from src.utils.request_utils import _generate_request_id


class RequestScheduler:
    def __init__(self):
        self.max_batch_size = ARGS.max_batch_size
        self.request_queue = queue.Queue()
        self.result_queue = queue.Queue()

        # intialized worker threads
        self.workers = []
        for gpu_id in range(ARGS.parallel_size):
            logger.info(f"Start worker thread on GPU {gpu_id}")
            worker = WorkerThread(
                gpu_id,
                self.request_queue,
                self.result_queue,
            )
            worker.start()
            logger.success(f"Worker thread on GPU {gpu_id} started.")
            self.workers.append(worker)

        # intialized result tracker thread
        self.result_tracker = ResultTracker(self.result_queue)
        self.result_tracker.start()
        self.results = self.result_tracker.results

    def schedule(self, prompt: str):
        """Schedule a request with the given prompt."""
        request_id = _generate_request_id()
        self.request_queue.put((request_id, prompt))
        logger.success(f"Request {request_id} scheduled.")
        return request_id

    def wait(self, request_id: str):
        """Wait until all results for the given request are ready."""
        while True:
            if request_id in self.results:
                logger.success(f"Result for request {request_id} is ready.")
                result = self.results[request_id]
                self.result_tracker.remove_request(request_id)
                return result
            time.sleep(ARGS.poll_interval)

    def shutdown(self):
        """Shutdown all worker threads."""
        # stop all worker threads
        logger.info("Shutting down worker threads...")
        for worker in self.workers:
            worker.stop()
            worker.join()

        # stop result tracker thread
        logger.info("Shutting down result tracker thread...")
        self.result_tracker.stop()
        self.result_tracker.join()

        logger.success("All threads stopped.")


scheduler = RequestScheduler()
