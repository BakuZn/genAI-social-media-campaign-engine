"""
Orchestrator component. Coordinates processing of brief parsing, generating platform assets,
localizing/translating them, and formatting output packages using highly efficient Batch JSON.
"""
import json
from core.llm_client import GeminiClient
from core.templates import BATCH_SYSTEM_PROMPT, BATCH_MASTER_PROMPT
from translators.translator import CampaignTranslator
from core.rag import ProductKnowledgeRetriever

class CampaignOrchestrator:
    def __init__(self):
        """
        Initializes the orchestrator, loading the Gemini client and Translator.
        """
        self.llm_client = GeminiClient()
        self.translator = CampaignTranslator(self.llm_client)
        self.rag_retriever = ProductKnowledgeRetriever()

    def generate_campaign(self, event_data: dict, platforms: list, languages: list, image_bytes: bytes = None) -> dict:
        """
        Executes the Two-Stage Transcreation Workflow via Batch JSON.
        Returns a dictionary shaped: {language: {platform: generated_text}}
        """
        brief_json = json.dumps(event_data, indent=2)
        platforms_str = ", ".join(platforms)
        
        # Retrieve RAG context based on product focus or objective
        query = f"{event_data.get('product_focus', '')} {event_data.get('objective', '')}"
        product_knowledge = self.rag_retriever.retrieve_context(query)
        if not product_knowledge:
            product_knowledge = "No specific product knowledge retrieved from the manual."

        results = {}
        
        prompt = BATCH_MASTER_PROMPT.format(
            platforms_list=platforms_str, 
            brief_json=brief_json,
            product_knowledge=product_knowledge
        )
        english_master_text = self.llm_client.generate_campaign_post(
            prompt=prompt, 
            system_instruction=BATCH_SYSTEM_PROMPT,
            image_bytes=image_bytes
        )
        
        try:
            english_master = json.loads(english_master_text)
        except json.JSONDecodeError:
            english_master = {plat: "Error: LLM did not return valid JSON. Please try generating again." for plat in platforms}
        
        for lang in languages:
            print(f"DEBUG: Orchestrator processing target language: {lang}")
            if lang.lower() in ["en", "english"]:
                results[lang] = english_master
            else:
                translated_dict = self.translator.translate_post(english_master, lang)
                results[lang] = translated_dict
                    
        return results
