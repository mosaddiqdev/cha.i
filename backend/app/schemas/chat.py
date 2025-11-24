
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CharacterResponse(BaseModel):
    id: str
    name: str
    title: str
    image: str
    description: str
    domain: str
    personality: str
    useCases: List[str]
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    character_id: str
    message: str
    conversation_id: Optional[int] = None
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: int
    character_response: str
    timestamp: datetime
    metadata: Optional[dict] = None


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: int
    character_id: str
    title: Optional[str]
    started_at: datetime
    last_message_at: datetime
    messages: List[MessageResponse]
    
    class Config:
        from_attributes = True
