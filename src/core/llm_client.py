"""
LLM Client wrapper. Interfaces with the Google Gemini API
and handles generation requests securely.
"""
from google import genai
from google.genai import types
from config import get_gemini_api_key, DEFAULT_MODEL

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

    def generate_campaign_post(self, prompt: str, system_instruction: str) -> str:
        """
        Generates content using the Gemini model with a specified system instruction
        for brand guidelines.
        """
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7, # Slightly creative but constrained for marketing
            response_mime_type="application/json" # Enforce JSON schema
        )
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config
        )
        return response.text
