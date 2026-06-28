import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ProductKnowledgeRetriever:
    def __init__(self, json_paths: list = None):
        """
        Initializes the retriever and loads the product knowledge JSON files.
        """
        if json_paths is None:
            json_paths = ["product_manual_rag_knowledge.json", "dosage_rag_knowledge.json"]
            
        self.chunks = []
        for path in json_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    new_chunks = data.get('chunks', [])
                    self.chunks.extend(new_chunks)
                    logger.info(f"Loaded {len(new_chunks)} product knowledge chunks from {path} for RAG.")
            except FileNotFoundError:
                logger.warning(f"Product knowledge file {path} not found. Skipping.")
            except json.JSONDecodeError:
                logger.error(f"Failed to decode JSON from {path}. Skipping.")

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
                text_content = chunk.get("text")
                if text_content:
                    matched_texts.append(text_content)
                else:
                    # If there's no flat 'text' field, serialize the entire chunk for the LLM
                    matched_texts.append(json.dumps(chunk, indent=2))

        if not matched_texts:
            return ""
        
        return "\n\n---\n\n".join(matched_texts)
