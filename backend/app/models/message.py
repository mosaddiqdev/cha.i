from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    meta_data = Column(Text)
    
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}')>"


class ConversationMemory(Base):
    __tablename__ = "conversation_memory"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    memory_type = Column(String)
    content = Column(Text, nullable=False)
    importance = Column(Integer, default=5)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    conversation = relationship("Conversation", back_populates="memory")
    
    def __repr__(self):
        return f"<ConversationMemory(id={self.id}, type='{self.memory_type}')>"
