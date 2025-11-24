from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(String, ForeignKey("characters.id"), nullable=False)
    user_id = Column(String)
    title = Column(String)
    started_at = Column(TIMESTAMP, server_default=func.now())
    last_message_at = Column(TIMESTAMP, server_default=func.now())
    is_active = Column(Boolean, default=True)
    meta_data = Column(Text)
    
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    memory = relationship("ConversationMemory", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, character='{self.character_id}')>"
