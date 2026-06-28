"""
LLM Client wrapper. Interfaces with the Google Gemini API
and handles generation requests securely.
"""
import io
import time
import logging
from PIL import Image
from google import genai
from google.genai import types
from google.genai.errors import APIError
from config import get_gemini_api_key, DEFAULT_MODEL

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, api_key: str = None):
        """
        Initializes the Gemini Client. 
        It will prioritize a passed API key, otherwise it falls back to the .env key.
        """
        self.api_key = api_key or get_gemini_api_key()
        if not self.api_key:
            raise ValueError(
                "Gemini API key is missing! Please set GEMINI_API_KEY in your .env file "
                "or input it via the Streamlit dashboard."
            )
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = DEFAULT_MODEL

    def generate_campaign_post(self, prompt: str, system_instruction: str, image_bytes: bytes = None) -> str:
        """
        Generates content using the Gemini model with a specified system instruction
        for brand guidelines. Optionally processes an image for context.
        """
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
            response_mime_type="application/json"
        )
        
        max_retries = 5
        for attempt in range(max_retries):
            # Recreate contents (and Image stream) on every attempt to prevent EOF/hang bugs
            contents = [prompt]
            if image_bytes:
                try:
                    img = Image.open(io.BytesIO(image_bytes))
                    contents.append(img)
                except Exception as e:
                    logger.error("Failed to load image: %s", e)
            
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=config
                )
                return response.text
            except APIError as e:
                # Catch specific API errors (like 503, 429) and apply exponential backoff
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning("API Error encountered. Retrying in %s seconds... (Attempt %s/%s) - Error: %s", wait_time, attempt + 1, max_retries, e)
                    time.sleep(wait_time)
                else:
                    raise e

    def extract_text_from_image(self, prompt: str, image_bytes: bytes) -> str:
        """
        Generates text using the Gemini model given an image and a prompt.
        Useful for quick OCR tasks before the main generation step.
        """
        config = types.GenerateContentConfig(temperature=0.1)
        contents = [prompt]
        if image_bytes:
            try:
                img = Image.open(io.BytesIO(image_bytes))
                contents.append(img)
            except Exception as e:
                logger.error("Failed to load image: %s", e)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )
            return response.text
        except Exception as e:
            logger.error("Failed image text extraction: %s", e)
            return ""
