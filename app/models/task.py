from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(String(20), default="medium")  # low, medium, high
    due_date = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with user
    owner = relationship("User", back_populates="tasks")
    
    # ✅ ADDED: Database indexes for faster queries
    __table_args__ = (
        Index('idx_tasks_user_id', 'user_id'),           # For filtering by user
        Index('idx_tasks_completed', 'completed'),       # For filtering completed tasks
        Index('idx_tasks_created_at', 'created_at'),     # For sorting by date
        Index('idx_tasks_user_completed', 'user_id', 'completed'),  # Composite index
        Index('idx_tasks_priority', 'priority'),         # For filtering by priority
    )
    
    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"