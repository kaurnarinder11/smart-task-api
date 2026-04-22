from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.services.task_service import (
    create_task_logic, get_all_tasks_logic, get_task_by_id_logic,
    update_task_logic, delete_task_logic, mark_complete_logic
)
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.core.security import get_current_user
from app.models.user import User
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
