from typing import List
from app.models import Message, ConversationMemory
from app.services.ai_service import ai_service
from sqlalchemy.orm import Session
from datetime import datetime
import json


class SummarizationService:
    def __init__(self):
        self.summarization_threshold = 30
        self.token_threshold = 15000
    
    def should_summarize(self, db: Session, conversation_id: int) -> bool:
        message_count = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).count()
        
        last_summary = db.query(ConversationMemory).filter(
            ConversationMemory.conversation_id == conversation_id,
            ConversationMemory.memory_type == "summary"
        ).order_by(ConversationMemory.created_at.desc()).first()
        
        if last_summary:
            messages_since_summary = db.query(Message).filter(
                Message.conversation_id == conversation_id,
                Message.timestamp > last_summary.created_at
            ).count()
            return messages_since_summary >= self.summarization_threshold
        
        return message_count >= self.summarization_threshold
    
    def create_progressive_summary(
        self,
        db: Session,
        conversation_id: int
    ) -> str:
        last_summary = db.query(ConversationMemory).filter(
            ConversationMemory.conversation_id == conversation_id,
            ConversationMemory.memory_type == "summary"
        ).order_by(ConversationMemory.created_at.desc()).first()
        
        if last_summary:
            new_messages = db.query(Message).filter(
                Message.conversation_id == conversation_id,
                Message.timestamp > last_summary.created_at
            ).order_by(Message.timestamp).all()
        else:
            all_messages = db.query(Message).filter(
                Message.conversation_id == conversation_id
            ).order_by(Message.timestamp).all()
            new_messages = all_messages[:-10]
        
        if not new_messages:
            return last_summary.content if last_summary else ""
        
        prompt = self._build_summarization_prompt(
            existing_summary=last_summary.content if last_summary else None,
            new_messages=new_messages
        )
        
        summary = ai_service.model.generate_content(prompt).text.strip()
        
        key_facts = self.extract_key_facts(new_messages)
        
        memory = ConversationMemory(
            conversation_id=conversation_id,
            memory_type="summary",
            content=summary,
            importance=0.8
        )
        db.add(memory)
        
        for fact in key_facts:
            fact_memory = ConversationMemory(
                conversation_id=conversation_id,
                memory_type="fact",
                content=fact,
                importance=0.7
            )
            db.add(fact_memory)
        
        db.commit()
        
        return summary
    
    def _build_summarization_prompt(
        self,
        existing_summary: str | None,
        new_messages: List[Message]
    ) -> str:
        messages_text = "\n".join([
            f"[{msg.role.upper()}]: {msg.content}"
            for msg in new_messages
        ])
        
        if existing_summary:
            return f"""You are summarizing a conversation progressively. Here is the existing summary:

EXISTING SUMMARY:
{existing_summary}

NEW MESSAGES:
{messages_text}

Please create an UPDATED SUMMARY that:
1. Incorporates the new messages into the existing summary
2. Maintains continuity and context
3. Highlights key topics, decisions, and emotional moments
4. Keeps it concise (max 200 words)

UPDATED SUMMARY:"""
        else:
            return f"""Summarize the following conversation. Focus on:
1. Main topics discussed
2. Key decisions or conclusions
3. Emotional tone and important moments
4. User preferences or interests mentioned

Keep it concise (max 200 words).

CONVERSATION:
{messages_text}

SUMMARY:"""
    
    def extract_key_facts(self, messages: List[Message]) -> List[str]:
        messages_text = "\n".join([
            f"[{msg.role.upper()}]: {msg.content}"
            for msg in messages
        ])
        
        prompt = f"""Extract KEY FACTS from this conversation. Focus on:
- User preferences (likes, dislikes, interests)
- Important personal information
- Decisions made
- Goals or plans mentioned
- Emotional states

Return as a JSON array of strings, max 5 facts.

CONVERSATION:
{messages_text}

KEY FACTS (JSON array):"""
        
        try:
            response = ai_service.model.generate_content(prompt).text.strip()
            if response.startswith('['):
                facts = json.loads(response)
                return facts[:5]
            else:
                return [f.strip('- ') for f in response.split('\n') if f.strip()][:5]
        except Exception as e:
            return []
    
    def get_conversation_summary(
        self,
        db: Session,
        conversation_id: int
    ) -> str:
        summary = db.query(ConversationMemory).filter(
            ConversationMemory.conversation_id == conversation_id,
            ConversationMemory.memory_type == "summary"
        ).order_by(ConversationMemory.created_at.desc()).first()
        
        return summary.content if summary else ""


summarization_service = SummarizationService()
