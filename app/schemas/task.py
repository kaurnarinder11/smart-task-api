# app/schemas/task.py
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    
    class Config:
        from_attributes = True 