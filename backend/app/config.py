from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """Application configuration settings."""
    
    app_name: str = "cha.i Backend"
    version: str = "1.0.0"
    
    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"
    temperature: float = 0.9
    max_output_tokens: int = 8192
    
    secret_key: str
    
    database_url: str = "sqlite:///./data/chat.db"
    
    cors_origins: Union[List[str], str] = []
    
    log_level: str = "INFO"
    max_conversation_history: int = 50
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
