import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ProductKnowledgeRetriever:
    def __init__(self, json_path: str = "product_manual_rag_knowledge.json"):
        """
        Initializes the retriever and loads the product knowledge JSON file.
        """
        self.chunks = []
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.chunks = data.get('chunks', [])
                logger.info(f"Loaded {len(self.chunks)} product knowledge chunks for RAG.")
        except FileNotFoundError:
            logger.warning(f"Product knowledge file {json_path} not found. RAG will return empty strings.")
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON from {json_path}. RAG will return empty strings.")

    def retrieve_context(self, query: str) -> str:
        """
        Retrieves matching product chunks based on keyword presence in the query.
        Returns a concatenated string of the matched texts.
        """
        if not query or not self.chunks:
            return ""

        query_lower = query.lower()
        matched_texts = []
        
        for chunk in self.chunks:
            product_name = chunk.get("product_name", "")
            if product_name and product_name.lower() in query_lower:
                matched_texts.append(chunk.get("text", ""))

        if not matched_texts:
            return ""
        
        return "\n\n---\n\n".join(matched_texts)
