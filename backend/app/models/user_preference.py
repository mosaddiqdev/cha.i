from sqlalchemy import Column, Integer, String, Float, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    character_id = Column(String, ForeignKey("characters.id"))
    preference_type = Column(String)
    preference_key = Column(String)
    preference_value = Column(Text)
    confidence = Column(Float, default=0.5)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
