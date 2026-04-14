from fastapi import APIRouter, Depends, HTTPException
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import (
    create_task_logic,
    get_all_tasks_logic,
    get_task_by_id_logic,
    update_task_logic,
    delete_task_logic,
    mark_complete_logic,
)
from app.core.security import get_current_user_dep

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, current_user=Depends(get_current_user_dep)):
    return create_task_logic(task, current_user.id)


@router.get("/", response_model=list[TaskResponse])
def get_tasks(current_user=Depends(get_current_user_dep)):
    return get_all_tasks_logic(current_user.id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, current_user=Depends(get_current_user_dep)):
    task = get_task_by_id_logic(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate, current_user=Depends(get_current_user_dep)):
    result = update_task_logic(task_id, task, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.delete("/{task_id}")
def delete_task(task_id: int, current_user=Depends(get_current_user_dep)):
    return delete_task_logic(task_id, current_user.id)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def mark_complete(task_id: int, current_user=Depends(get_current_user_dep)):
    result = mark_complete_logic(task_id, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
