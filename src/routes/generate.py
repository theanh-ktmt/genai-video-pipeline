from flask import Blueprint, request, send_file
import time
from src.utils.server_args import ARGS
from src.manage.scheduler import scheduler
from loguru import logger
import io


module = Blueprint("generate", __name__)


@module.route("/", methods=["POST"])
def generate():
    start = time.time()

    # extract prompt
    content = request.json
    prompt = content.get("prompt", "")
    logger.info(f"Received prompt: {prompt}")

    # schedule the video generation
    request_id = scheduler.schedule(prompt)
    video_buffer = scheduler.wait(request_id)

    logger.info(f"Video generation completed in {time.time() - start:.2f} seconds.")
    return send_file(
        video_buffer,
        mimetype="video/mp4",
        as_attachment=True,
        download_name="generated_video.mp4",
    )
