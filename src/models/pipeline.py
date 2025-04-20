from src.utils.server_args import ARGS
from src.models.gemini import GeminiModel
from src.models.mochi import MochiModel


class VideoGenerationPipeline:
    def __init__(self, gpu_id: int = 0):
        """
        Initialize the video generation pipeline with the specified GPU ID.
        :param gpu_id: The GPU ID to use for processing.
        """
        self.gpu_id = gpu_id

        # initialize the models
        if ARGS.llm == "gemini":
            self.llm = GeminiModel()
        else:
            raise ValueError(f"Unsupported LLM model: {ARGS.llm}")
        if ARGS.video_generation_model == "mochi":
            self.vid_gen = MochiModel(self.gpu_id)
        else:
            raise ValueError(
                f"Unsupported video generation model: {ARGS.video_generation_model}"
            )

    def generate(self, prompts: str):
        """
        Generate a video from the given prompts.
        1. Enhance the prompts using the LLM.
        2. Generate a video using the enhanced prompts.

        :param prompts: The prompts to generate a video for.
        :return: A buffer containing the generated video.
        """
        prompts = self.llm.process_batch_prompts(prompts)
        video_buffers = self.vid_gen.process_batch_prompts(prompts)
        return video_buffers


pipeline = VideoGenerationPipeline()
