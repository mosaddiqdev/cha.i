from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings
import os
import logging

logger = logging.getLogger(__name__)

os.makedirs("data", exist_ok=True)

# Conditional connect_args based on database type
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create engine with production-ready pooling settings
engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verify connection before usage
    pool_recycle=300,    # Recycle connections every 5 minutes
    pool_size=5,         # Maintain 5 connections
    max_overflow=10      # Allow up to 10 temporary connections
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully!")
