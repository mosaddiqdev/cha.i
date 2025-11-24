
from sqlalchemy.orm import Session
from app.models import Conversation, Message
from datetime import datetime
from typing import List, Dict, Optional


class ConversationService:
    
    @staticmethod
    def create_conversation(
        db: Session,
        character_id: str,
        user_id: Optional[str] = None,
        title: Optional[str] = None
    ) -> Conversation:
        conversation = Conversation(
            character_id=character_id,
            user_id=user_id,
            title=title
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    @staticmethod
    def get_conversation(db: Session, conversation_id: int) -> Optional[Conversation]:
        return db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    @staticmethod
    def get_user_conversations(
        db: Session,
        user_id: str,
        character_id: Optional[str] = None
    ) -> List[Conversation]:
        query = db.query(Conversation).filter(Conversation.user_id == user_id)
        if character_id:
            query = query.filter(Conversation.character_id == character_id)
        return query.order_by(Conversation.last_message_at.desc()).all()
    
    @staticmethod
    def add_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        db.add(message)
        
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        if conversation:
            conversation.last_message_at = datetime.utcnow()
        
        db.commit()
        db.refresh(message)
        return message
    
    @staticmethod
    def get_conversation_history(db: Session, conversation_id: int) -> List[Dict[str, str]]:
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp).all()
        
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
    
    
    @staticmethod
    def get_active_conversation(
        db: Session,
        user_id: str,
        character_id: str
    ) -> Optional[Conversation]:
        return db.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.character_id == character_id
        ).order_by(Conversation.last_message_at.desc()).first()
    
    @staticmethod
    def update_conversation_title(
        db: Session,
        conversation_id: int,
        title: str
    ):
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        if conversation and not conversation.title:
            conversation.title = title
            db.commit()


conversation_service = ConversationService()
