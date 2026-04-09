from fastapi import APIRouter, HTTPException
from app.schemas.task import TaskCreate, TaskResponse  # ADD THIS
from app.services.task_service import validate_and_prepare_task  # ADD THIS

router = APIRouter()

# Temporary storage (will be replaced with database later)
tasks_db = []
task_id_counter = 1

# GET /tasks - Get all tasks
@router.get("/tasks")
def get_all_tasks():
    return {"tasks": tasks_db, "count": len(tasks_db)}

# GET /tasks/{id} - Get one specific task
@router.get("/tasks/{task_id}")
def get_one_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return {"task": task}
    
    # If we reach here, task wasn't found
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# POST /tasks - Create a new task
@router.post("/tasks", response_model=dict)  # We'll improve response_model later
def create_task(task: TaskCreate):  # ← Changed from dict to TaskCreate
    global task_id_counter
    
    # Use service for validation
    result = validate_and_prepare_task(task)
    
    if not result["valid"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Create task using validated data
    new_task = {
        "id": task_id_counter,
        "title": result["data"]["title"],
        "status": result["data"]["status"]
    }
    
    tasks_db.append(new_task)
    task_id_counter += 1
    
    return {"message": "Task created", "task": new_task}

# DELETE /tasks/{id} - Remove a task
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            deleted = tasks_db.pop(index)
            return {"message": "Task deleted", "task": deleted}
    
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")