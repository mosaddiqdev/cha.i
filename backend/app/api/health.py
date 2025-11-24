from fastapi import APIRouter
from datetime import datetime
from app.config import settings

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "app_name": settings.app_name,
        "version": settings.version
    }


@router.get("/info")
def get_info():
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "model": settings.gemini_model,
        "max_conversation_history": settings.max_conversation_history
    }
