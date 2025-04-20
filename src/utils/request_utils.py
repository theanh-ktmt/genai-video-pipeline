import time


def _generate_request_id() -> str:
    """Generate a unique request ID based on the current time."""
    return time.strftime("%Y%m%d_%H%M%S_") + f"{int(time.time() * 1000) % 1000:03d}"
