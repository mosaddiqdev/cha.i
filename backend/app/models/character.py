from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base


class Character(Base):
    __tablename__ = "characters"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    title = Column(String)
    avatar_url = Column(String)
    description = Column(Text)
    domain = Column(String)
    personality = Column(Text)
    use_cases = Column(Text)
    system_prompt = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Character(id='{self.id}', name='{self.name}')>"
