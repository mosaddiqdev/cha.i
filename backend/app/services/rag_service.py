import logging
from typing import List, Dict
from app.core.vector_store import vector_store
from app.services.embedding_service import embedding_service
from app.services.conversation_service import conversation_service
from sqlalchemy.orm import Session
from app.models import Message
from datetime import datetime

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
    
    def index_message(
        self,
        message_id: int,
        conversation_id: int,
        user_id: str,
        character_id: str,
        role: str,
        content: str,
        timestamp: datetime
    ):
        try:
            embedding = self.embedding_service.generate_embedding(content)
            metadata = {
                "message_id": str(message_id),
                "conversation_id": str(conversation_id),
                "user_id": user_id,
                "character_id": character_id,
                "role": role,
                "timestamp": timestamp.isoformat()
            }
            memory_id = f"msg_{message_id}"
            self.vector_store.add_memory(
                memory_id=memory_id,
                text=content,
                embedding=embedding,
                metadata=metadata
            )
        except Exception as e:
            logger.error(f"Failed to index message {message_id}: {e}", exc_info=True)
    
    def index_conversation(
        self,
        db: Session,
        conversation_id: int,
        user_id: str,
        character_id: str
    ):
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp).all()
        
        for msg in messages:
            self.index_message(
                message_id=msg.id,
                conversation_id=conversation_id,
                user_id=user_id,
                character_id=character_id,
                role=msg.role,
                content=msg.content,
                timestamp=msg.timestamp
            )
    
    def retrieve_relevant_context(
        self,
        user_message: str,
        user_id: str,
        character_id: str,
        current_conversation_id: int,
        n_results: int = 5
    ) -> str:
        try:
            query_embedding = self.embedding_service.generate_query_embedding(user_message)
            memories = self.vector_store.search_similar(
                query_embedding=query_embedding,
                user_id=user_id,
                character_id=character_id,
                n_results=n_results * 2
            )
            
            relevant_memories = [
                m for m in memories
                if m['metadata'].get('conversation_id') != str(current_conversation_id)
            ][:n_results]
            
            if not relevant_memories:
                return ""
            
            context_parts = ["RELEVANT PAST CONTEXT:"]
            total_chars = len(context_parts[0])
            max_context_chars = 1500
            
            # Build context incrementally, respecting token limits
            # Each memory is truncated individually, then we stop adding when total limit is reached
            # This prevents overwhelming the AI model while maintaining conversation continuity
            for i, memory in enumerate(relevant_memories, 1):
                role = memory['metadata'].get('role', 'unknown')
                text = memory['text']
                
                max_memory_chars = 200
                if len(text) > max_memory_chars:
                    text = text[:max_memory_chars] + "..."
                
                memory_line = f"{i}. [{role.upper()}]: {text}"
                
                if total_chars + len(memory_line) > max_context_chars:
                    logger.info(f"RAG context limit reached at {i} memories")
                    break
                
                context_parts.append(memory_line)
                total_chars += len(memory_line)
            
            return "\n".join(context_parts)
        except Exception as e:
            logger.error(f"Failed to retrieve RAG context: {e}", exc_info=True)
            return ""
    
    def get_memory_stats(self) -> Dict:
        return {
            "total_memories": self.vector_store.get_collection_count()
        }

rag_service = RAGService()
