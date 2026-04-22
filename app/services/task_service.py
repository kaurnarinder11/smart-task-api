from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.logger import get_logger
from fastapi import HTTPException
from datetime import datetime

logger = get_logger("task_service")

def create_task_logic(task_data: TaskCreate, user_id: int, db: Session):
    """Create a new task"""
    logger.info(f"Creating task for user {user_id}")
    
    if not task_data.title or len(task_data.title.strip()) == 0:
        raise HTTPException(400, "Task title cannot be empty")
    
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        priority=task_data.priority,
        due_date=task_data.due_date,
        user_id=user_id
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    logger.info(f"Task created with ID: {db_task.id}")
    return db_task

def get_all_tasks_logic(user_id: int, db: Session, page: int = 1, limit: int = 10, 
                        completed: bool = None, sort: str = "desc"):
    """Get all tasks for a user with pagination"""
    logger.debug(f"Fetching tasks for user {user_id}, page {page}")
    
    skip = (page - 1) * limit
    query = db.query(Task).filter(Task.user_id == user_id)
    
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    if sort == "desc":
        query = query.order_by(desc(Task.created_at))
    else:
        query = query.order_by(asc(Task.created_at))
    
    total = query.count()
    tasks = query.offset(skip).limit(limit).all()
    
    return {
        "tasks": tasks,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit if total > 0 else 1
    }

def get_task_by_id_logic(task_id: int, user_id: int, db: Session):
    """Get a single task by ID"""
    logger.debug(f"Fetching task {task_id} for user {user_id}")
    
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(404, f"Task with id {task_id} not found")
    
    return task

def update_task_logic(task_id: int, updated_data: TaskUpdate, user_id: int, db: Session):
    """Update an existing task"""
    logger.info(f"Updating task {task_id} for user {user_id}")
    
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(404, f"Task with id {task_id} not found")
    
    if task.completed and updated_data.completed is False:
        raise HTTPException(400, "Cannot uncomplete a completed task")
    
    # Update only provided fields
    update_data = updated_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    
    logger.info(f"Task {task_id} updated successfully")
    return task

def delete_task_logic(task_id: int, user_id: int, db: Session):
    """Delete a task"""
    logger.info(f"Deleting task {task_id} for user {user_id}")
    
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(404, f"Task with id {task_id} not found")
    
    db.delete(task)
    db.commit()
    
    logger.info(f"Task {task_id} deleted successfully")
    return {"message": "Task deleted successfully"}

def mark_complete_logic(task_id: int, user_id: int, db: Session):
    """Mark a task as completed"""
    logger.info(f"Marking task {task_id} complete for user {user_id}")
    
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(404, f"Task with id {task_id} not found")
    
    if task.completed:
        raise HTTPException(400, "Task is already completed")
    
    task.completed = True
    db.commit()
    db.refresh(task)
    
    logger.info(f"Task {task_id} marked complete")
    return task