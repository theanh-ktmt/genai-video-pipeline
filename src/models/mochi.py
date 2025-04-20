from loguru import logger

import torch
from diffusers import MochiPipeline
from src.utils.video_utils import pil_list_to_mp4, generate_mock_frames
from src.utils.server_args import ARGS


class MochiModel:
    def __init__(
        self,
        width: int = 848,
        height: int = 480,
        num_frames=84,
        num_inference_steps: int = 64,
        fps=30,
    ):
        """
        Initialize the MochiModel with the specified number of frames and frames per second.

        :param fps: Frames per second for the video.
        :param num_frames: Number of frames to generate.
        """
        self.width = width
        self.height = height
        self.num_frames = num_frames
        self.num_inference_steps = num_inference_steps
        self.fps = fps
        self.mock_video_generation = ARGS.mock_video_generation

        # load the model
        if not self.mock_video_generation:
            logger.info("Loading Mochi model...")
            self.pipe = MochiPipeline.from_pretrained(
                "genmo/mochi-1-preview", variant="bf16", torch_dtype=torch.bfloat16
            )
            # enable memory savings
            self.pipe.enable_model_cpu_offload()
            self.pipe.enable_vae_tiling()
        else:
            logger.info("Mock video generation enabled. Skipping model loading.")
            self.pipe = None

    def generate_video(self, prompt):
        """
        Generate a video from the given prompt.
        :param prompt: The prompt to generate a video for.
        :return: A buffer containing the generated video.
        """
        try:
            if self.mock_video_generation:
                frames = generate_mock_frames(
                    num_frames=self.num_frames,
                    width=self.width,
                    height=self.height,
                    text="Mock Video",
                )
            else:
                frames = self.pipe(
                    prompt,
                    width=self.width,
                    height=self.height,
                    num_frames=self.num_frames,
                    num_inference_steps=self.num_inference_steps,
                ).frames[0]

            # save frames to a buffer
            video_buffer = pil_list_to_mp4(frames, fps=self.fps)
            return video_buffer
        except Exception as e:
            logger.error(f"Error generating video: {e}")
            return None

    def process_single_prompt(self, prompt):
        """
        Process a single prompt to generate a video.

        :param prompt: The prompt to generate a video for.
        :return: A buffer containing the generated video.
        """
        logger.info(f"Processing prompt: {prompt}")
        video_buffer = self.generate_video(prompt)
        if video_buffer:
            logger.info("Video generation successful.")
            return video_buffer
        else:
            logger.error("Video generation failed.")
            return None

    def process_batched_prompts(self, prompts):
        """
        Process a batch of prompts to generate videos.

        :param prompts: A list of prompts to generate videos for.
        :return: A list of buffers containing the generated videos.
        """
        video_buffers = []
        for prompt in prompts:
            logger.info(f"Processing prompt: {prompt}")
            video_buffer = self.generate_video(prompt)
            if video_buffer:
                logger.info("Video generation successful.")
                video_buffers.append(video_buffer)
            else:
                logger.error("Video generation failed.")
                video_buffers.append(None)
        return video_buffers

    def save_video(self, video_buffer, filename):
        """
        Save the generated video to a file.
        :param video_buffer: The buffer containing the video data.
        :param filename: The name of the file to save the video to.
        """
        try:
            with open(filename, "wb") as f:
                f.write(video_buffer.getbuffer())
            logger.info(f"Video saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving video: {e}")
