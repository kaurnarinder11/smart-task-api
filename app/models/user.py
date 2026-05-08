from sqlalchemy import Column, Integer, String, Boolean, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with tasks
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    
    # ✅ ADDED: Database indexes for faster queries
    __table_args__ = (
        Index('idx_users_created_at', 'created_at'),     # For sorting users by join date
        Index('idx_users_is_active', 'is_active'),       # For filtering active/inactive users
        Index('idx_users_email_username', 'email', 'username'),  # Composite for login queries
    )