from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.services.task_service import (
    create_task_logic, get_all_tasks_logic, get_task_by_id_logic,
    update_task_logic, delete_task_logic, mark_complete_logic
)
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse
from app.core.security import get_current_user
from app.models.user import User
from app.models.task import Task
from app.core.logger import get_logger

router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = get_logger("tasks_route")

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Creating task for user: {current_user.email}")
    return create_task_logic(task, current_user.id, db)

@router.get("/")
def get_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    completed: Optional[bool] = None,
    sort: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Fetching tasks for user: {current_user.email}")
    return get_all_tasks_logic(current_user.id, db, page, limit, completed, sort)


@router.get("/paginated")
def get_tasks_paginated(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get tasks with pagination metadata
    """
    logger.info(f"Fetching paginated tasks for user: {current_user.email}")
    
    # Build query
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    # Apply completed filter if provided
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    # Get total count
    total = query.count()
    
    # Get paginated tasks
    tasks = query.order_by(Task.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    # Convert SQLAlchemy objects to dict (Pydantic-friendly)
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "user_id": task.user_id,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        })
    
    # Build pagination URLs
    base_url = "/tasks/paginated"
    next_url = f"{base_url}?skip={skip + limit}&limit={limit}" if skip + limit < total else None
    previous_url = f"{base_url}?skip={max(0, skip - limit)}&limit={limit}" if skip > 0 else None
    
    return {
        "data": tasks_data,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_next": skip + limit < total,
        "has_previous": skip > 0,
        "next_url": next_url,
        "previous_url": previous_url
    }

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Fetching task {task_id} for user: {current_user.email}")
    return get_task_by_id_logic(task_id, current_user.id, db)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Updating task {task_id} for user: {current_user.email}")
    return update_task_logic(task_id, task_update, current_user.id, db)

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Deleting task {task_id} for user: {current_user.email}")
    return delete_task_logic(task_id, current_user.id, db)

@router.patch("/{task_id}/complete", response_model=TaskResponse)
def mark_complete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Marking task {task_id} complete for user: {current_user.email}")
    return mark_complete_logic(task_id, current_user.id, db)