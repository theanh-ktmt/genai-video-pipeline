from io import BytesIO
import numpy as np
import tempfile
import cv2
import io
from PIL import Image, ImageDraw, ImageFont
from loguru import logger


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


def generate_mock_frames(
    num_frames: int,
    width: int,
    height: int,
    text="Mock Video",
    font_size=120,
    text_color="black",
) -> list:
    """
    Generates a list of PIL Image frames with specified width and height,
    writing the given text in the middle of each frame.

    :param num_frames: Number of frames to generate.
    :param width: Width of each frame.
    :param height: Height of each frame.
    :param text: Text to write in the middle of each frame.
    :param font_size: Font size of the text.
    :param text_color: Color of the text.
    :return: List of PIL images.
    """
    frames = []
    font = ImageFont.load_default(font_size)
    for _ in range(num_frames):
        frame = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(frame)

        # draw text in the middle
        text_width = draw.textlength(text, font=font)
        text_height = font_size * len(text.split())
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2
        draw.text((text_x, text_y), text, fill=text_color, font=font)

        frames.append(frame)
    return frames
