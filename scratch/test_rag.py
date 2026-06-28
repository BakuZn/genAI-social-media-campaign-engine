import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from core.rag import ProductKnowledgeRetriever

rag = ProductKnowledgeRetriever(["product_manual_rag_knowledge.json", "dosage_rag_knowledge.json"])
query = "Seminis Adhik & Camalus® highlighting the synergistic benefits of Seminis Adhik hybrid tomatoes and Camalus® insecticide."
res = rag.retrieve_context(query)
print("RETRIEVED LENGTH:", len(res))
print("RETRIEVED DATA:\n", res)
