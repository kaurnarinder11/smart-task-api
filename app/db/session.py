from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - switch to PostgreSQL in production
# For now, SQLite with connection pooling settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./coding_journal.db")

# SQLite specific settings for better concurrency
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Allow multiple threads
        pool_size=10,  # Connection pool size
        max_overflow=20,  # Extra connections if needed
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,  # Recycle connections every hour
    )
else:
    # PostgreSQL settings (for future)
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()