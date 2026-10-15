"""
FinPilot Backend - Database Configuration
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://finpilot:finpilot_secret@localhost:5432/finpilot"
)

# SQLAlchemy 2.0 uses psycopg (v3) by default for postgresql://
# Normalize to postgresql+psycopg2:// if no driver is specified
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
