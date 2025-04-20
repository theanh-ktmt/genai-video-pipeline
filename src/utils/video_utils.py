from io import BytesIO
import numpy as np
import tempfile
import cv2
import io


def pil_list_to_mp4(pil_images, fps=30):
    """
    Converts a list of PIL images to an MP4 video buffer.

    :param pil_images: List of PIL images to convert.
    :param fps: Frames per second for the video.
    :return: BytesIO buffer containing the MP4 video.
    """
    if not pil_images:
        raise ValueError("Image list is empty.")

    temp_video = tempfile.NamedTemporaryFile(suffix=".mp4")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(temp_video.name, fourcc, fps, pil_images[0].size)
    for img in pil_images:
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        video_writer.write(frame)

    video_writer.release()
    video_buffer = io.BytesIO(temp_video.read())
    temp_video.close()
    video_buffer.seek(0)

    return video_buffer


def save_video_buffer(buffer: BytesIO, output_path: str) -> None:
    """
    Saves an MP4 buffer to a local file.

    :param buffer: BytesIO buffer containing MP4 video.
    :param output_path: Path where the file will be saved.
    """
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())
