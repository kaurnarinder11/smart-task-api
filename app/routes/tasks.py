from fastapi import APIRouter, HTTPException
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    result = task_service.create_task_logic(task)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/", response_model=list[TaskResponse])
def get_all_tasks():
    return task_service.get_tasks_logic()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = task_service.get_task_by_id_logic(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    result = task_service.update_task_logic(task_id, task_update)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    deleted = task_service.delete_task_logic(task_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return None