from fastapi import APIRouter, Depends, HTTPException
from app.schemas.task import TaskCreate
from fastapi import BackgroundTasks
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

def log_task_creation(title: str):
        with open("task_log.txt", "a") as f:
           f.write(f"Task created: {title}\n")


# ============ CREATE ============
@router.post("/")
def create_task(task: TaskCreate, background_tasks: BackgroundTasks, current_user=Depends(get_current_user_dep)):
    new_task = create_task_logic(task, current_user.id)
    background_tasks.add_task(log_task_creation, task.title)

    return {
        "success": True,
        "data": new_task,
        "message": "Task created successfully"
    }


# ============ READ ALL ============
@router.get("/")
def get_tasks(
    page: int = 1,
    limit: int = 5,
    completed: bool = None,
    sort: str = "desc",
    current_user=Depends(get_current_user_dep)
):
    tasks = get_all_tasks_logic(current_user.id, page, limit, completed, sort)

    return {
        "success": True,
        "data": tasks,
        "page": page,
        "limit": limit,
        "message": "Tasks fetched successfully"
    }


# ============ READ ONE ============
@router.get("/{task_id}")
def get_task(task_id: int, current_user=Depends(get_current_user_dep)):
    task = get_task_by_id_logic(task_id, current_user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "data": task,
        "message": "Task fetched successfully"
    }


# ============ UPDATE ============
@router.put("/{task_id}")
def update_task(task_id: int, task: TaskCreate, current_user=Depends(get_current_user_dep)):
    result = update_task_logic(task_id, task, current_user.id)

    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "success": True,
        "data": result,
        "message": "Task updated successfully"
    }


# ============ DELETE ============
@router.delete("/{task_id}")
def delete_task(task_id: int, current_user=Depends(get_current_user_dep)):
    result = delete_task_logic(task_id, current_user.id)

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "message": "Task deleted successfully"
    }


# ============ MARK COMPLETE ============
@router.patch("/{task_id}/complete")
def mark_complete(task_id: int, current_user=Depends(get_current_user_dep)):
    result = mark_complete_logic(task_id, current_user.id)

    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "success": True,
        "data": result,
        "message": "Task marked as complete"
    }

    