import google.generativeai as genai
from typing import List
from app.config import settings


class EmbeddingService:
    
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = "models/text-embedding-004"
    
    def generate_embedding(self, text: str) -> List[float]:
        try:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return [0.0] * 768
    
    def generate_query_embedding(self, query: str) -> List[float]:
        try:
            result = genai.embed_content(
                model=self.model,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return [0.0] * 768
    
    def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            embeddings.append(self.generate_embedding(text))
        return embeddings

embedding_service = EmbeddingService()
