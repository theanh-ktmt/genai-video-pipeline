import requests
import os
from dotenv import load_dotenv
from loguru import logger

# load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# request params
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
headers = {"Content-Type": "application/json"}
data = {
    "contents": [
        {
            "parts": [{"text": "Who is the first president of the United States?"}],
        }
    ]
}
params = {"key": api_key}

# send request
try:
    response = requests.post(url, headers=headers, json=data, params=params)
    response.raise_for_status()

    response_data = response.json()
    answer = response_data["candidates"][0]["content"]["parts"][0]["text"]
    logger.info(f"Answer: {answer}")

except Exception as e:
    logger.info(f"An error occurred: {e}")
