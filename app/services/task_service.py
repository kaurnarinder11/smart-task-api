"""
SERVICE LAYER - Contains all business rules for tasks
"""

from app.schemas.task import TaskCreate


def validate_and_prepare_task(task: TaskCreate) -> dict:
    """
    Business Rules:
    1. Title cannot be empty
    2. Title must be at least 3 characters
    """
    # Rule 1: Title cannot be empty
    if not task.title or not task.title.strip():
        return {"valid": False, "error": "Title cannot be empty"}
    
    # Rule 2: Title must be at least 3 characters
    if len(task.title.strip()) < 3:
        return {"valid": False, "error": "Title must be at least 3 characters"}
    
    # All rules passed
    return {
        "valid": True,
        "data": {
            "title": task.title.strip(),
            "status": task.status
        }
    }