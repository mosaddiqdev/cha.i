"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import characters, chat, health, auth
from app.core.database import init_db
import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Backend API for character AI chat application with Phase 2 enhancements"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_request_origin(request, call_next):
    origin = request.headers.get("origin")
    logger.info(f"🌐 Request Origin: {origin}")
    logger.info(f"📋 Allowed Origins: {settings.cors_origins}")
    response = await call_next(request)
    return response

app.include_router(auth.router)
app.include_router(characters.router)
app.include_router(chat.router)
app.include_router(health.router)


from app.core.seed import seed_data

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()
    seed_data()
    logger.info(f"✅ {settings.app_name} v{settings.version} started successfully!")
    logger.info(f"🔒 CORS Origins loaded: {settings.cors_origins}")


@app.get("/")
def root():
    return {
        "message": "cha.i Backend API",
        "version": settings.version,
        "docs": "/docs"
    }
