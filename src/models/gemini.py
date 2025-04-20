import os
import time
import requests
from loguru import logger
from dotenv import load_dotenv
from src.utils.prompt_utils import load_prompt, apply_prompt_template


load_dotenv()


class GeminiModel:
    """
    Gemini is a class that provides methods to interact with the Gemini API.
    """

    def __init__(self, n_retry: int = 3, timeout: int = 5):
        """
        Initialize the Gemini class with API key and secret.

        :param n_retry: Number of retries for API calls.
        :param timeout: Timeout for API calls in seconds.
        """
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.n_retry = n_retry
        self.timeout = timeout

        # load system instruction and template
        self.system_instruction = load_prompt("prompts/system_instruction.md")
        logger.info(f"System instruction: \n{self.system_instruction}")

        self.video_generation_template = load_prompt(
            "prompts/templates/video_generation_template.md"
        )
        logger.info(f"Video generation template: \n{self.video_generation_template}")

    def process_single_prompt(self, prompt: str) -> str:
        """
        Call the Gemini API with the provided prompt.

        :param prompt: The prompt to send to the Gemini API.
        :return: The response from the Gemini API.
        """
        # apply the template to the prompt
        prompt = apply_prompt_template(prompt, self.video_generation_template)
        logger.info(f"Prompt after applying template: \n{prompt}")

        # request params
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {"Content-Type": "application/json"}
        data = {
            "system_instruction": {
                "parts": [
                    {
                        "text": self.system_instruction,
                    }
                ]
            },
            "contents": [
                {
                    "parts": [{"text": prompt}],
                }
            ],
        }
        params = {"key": self.api_key}

        # try to call the API with retries
        for try_i in range(self.n_retry):
            logger.info(f"Gemini API call attempt {try_i + 1}/{self.n_retry}")
            try:
                response = requests.post(
                    url, headers=headers, json=data, params=params, timeout=self.timeout
                )

                # check if the answer is valid
                response.raise_for_status()
                response_data = response.json()
                if "candidates" not in response_data:
                    logger.error("No candidates found in the response.")
                    return None
                if len(response_data["candidates"]) == 0:
                    logger.error("No candidates found in the response.")
                    return None
                answer = response_data["candidates"][0]["content"]["parts"][0]["text"]
                logger.info(f"Enhanced prompt: {answer}")
                return answer

            except requests.exceptions.RequestException as e:
                logger.error(f"Request {try_i + 1} failed: {e}")
                if try_i == self.n_retry - 1:
                    logger.error("Max retries reached. Exiting.")
                    raise e

    def process_batched_prompts(self, prompts: list) -> list:
        """
        Call the Gemini API with a batch of prompts.
        Note that the Gemini API does not support batch processing,
        so this method will call the API for each prompt individually.

        :param prompts: A list of prompts to send to the Gemini API.
        :return: A list of responses from the Gemini API.
        """
        responses = []
        for prompt in prompts:
            response = self.process_single_prompt(prompt)
            responses.append(response)
            time.sleep(1)
        return responses
