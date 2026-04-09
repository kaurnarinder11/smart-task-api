"""
Pydantic Schemas for Task API
Purpose: Define data shape, validation, and type hints
"""

from pydantic import BaseModel
from typing import Optional

# Request schema - What client sends to CREATE a task
class TaskCreate(BaseModel):
    title: str
    status: Optional[str] = "pending"  # Default value if not provided

# Response schema - What API sends back to client
class TaskResponse(BaseModel):
    id: int
    title: str
    status: str