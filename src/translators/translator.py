"""
Translator module for executing the Two-Stage Transcreation Workflow using Batch JSON.
"""
import json

BATCH_TRANSLATION_PROMPT = """
You are an expert bilingual agricultural marketer for Bayer Crop Science.
Your task is to 'Transcreate' the following JSON object containing English social media posts EXCLUSIVELY into {target_language}.
You MUST verify that the output language is strictly {target_language}. Do not output any other regional languages (e.g., if asked for Punjabi, do not output Kannada).

STRICT CONSTRAINTS:
1. Target Language: ALL translated marketing copy MUST be in {target_language}.
2. Brand Names: ANY seed brand (e.g., DEKALB®, Asgrow®) or crop protection product (e.g., Roundup®) MUST remain in English characters. Do NOT transliterate them.
3. Hashtags: ALL hashtags (e.g., #BayerCropScience) MUST remain exactly as they are in English.
4. Formatting: Preserve all emojis and Markdown formatting (e.g., WhatsApp *bold* text, Instagram [Image Suggestion] brackets). Do not strip these out.
5. Tone & Culture: Adapt the greeting and tone to sound natural and respectful to farmers in the {target_language} region. Do not translate idioms literally.

Original English JSON:
{source_json}

Return a single JSON object with the exact same keys, but with the values strictly translated to {target_language}.
"""

class CampaignTranslator:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        
    def translate_post(self, source_dict: dict, target_language: str) -> dict:
        """
        Translates a batch dictionary of campaign posts into the target language.
        """
        if target_language.lower() in ["en", "english"]:
            return source_dict
            
        print(f"DEBUG: Translator module requesting LLM translation to -> {target_language}")
            
        prompt = BATCH_TRANSLATION_PROMPT.format(
            target_language=target_language,
            source_json=json.dumps(source_dict, indent=2)
        )
        
        response_text = self.llm_client.generate_campaign_post(
            prompt=prompt, 
            system_instruction="You are an expert bilingual transcreator. Always output valid JSON."
        )
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            print(f"ERROR: Translator module failed to decode JSON for {target_language}")
            # Fallback if the LLM breaks the JSON schema
            return source_dict
