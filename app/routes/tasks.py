# app/routes/tasks.py
from fastapi import APIRouter, HTTPException, status
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import (
    create_task_logic,
    get_all_tasks_logic,
    get_task_by_id_logic,
    update_task_logic,
    delete_task_logic,
    mark_complete_logic
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


# ============= CREATE =============
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    """
    Create a new task
    POST /tasks/
    """
    return create_task_logic(task)


# ============= READ ALL =============
@router.get("/", response_model=list[TaskResponse])
def get_all_tasks():
    """
    Get all tasks
    GET /tasks/
    """
    return get_all_tasks_logic()


# ============= READ ONE =============
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """
    Get a single task by ID
    GET /tasks/{task_id}
    """
    task = get_task_by_id_logic(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    return task


# ============= UPDATE =============
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate):
    """
    Update an existing task
    PUT /tasks/{task_id}
    
    RULES:
    - Task must exist
    - Title cannot be empty
    - Completed tasks cannot be updated
    """
    try:
        updated_task = update_task_logic(task_id, task)
        
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        
        return updated_task
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============= DELETE =============
@router.delete("/{task_id}")
def delete_task(task_id: int):
    """
    Delete a task
    DELETE /tasks/{task_id}
    """
    result = delete_task_logic(task_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    return result


# ============= MARK COMPLETE (Bonus) =============
@router.patch("/{task_id}/complete", response_model=TaskResponse)
def mark_complete(task_id: int):
    """
    Mark a task as completed
    PATCH /tasks/{task_id}/complete
    
    RULE: Cannot mark already completed task
    """
    try:
        completed_task = mark_complete_logic(task_id)
        
        if not completed_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        
        return completed_task
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )