#TASK DATABASE MODEL

from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed=Column(Boolean, default=False)

def __repr__(self):
    return f<"Task(id={self.id}, title='{self.title}', completed={self.completed})>"