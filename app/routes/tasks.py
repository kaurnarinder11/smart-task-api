from fastapi import APIRouter, HTTPException

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
@router.post("/tasks")
def create_task(task: dict):
    global task_id_counter
    
    # Validation: title is required
    if "title" not in task:
        raise HTTPException(status_code=400, detail="Title is required")
    
    new_task = {
        "id": task_id_counter,
        "title": task["title"],
        "status": task.get("status", "pending")  # Default status = "pending"
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