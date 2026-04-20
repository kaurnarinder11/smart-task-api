from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate
from fastapi import BackgroundTasks
from app.db.database import get_db
from app.services.task_service import (
    create_task_logic,
    get_all_tasks_logic,
    get_task_by_id_logic,
    update_task_logic,
    delete_task_logic,
    mark_complete_logic,
)
from app.core.security import get_current_user_dep
from app.core.logger import get_logger

router = APIRouter(prefix="/tasks", tags=["tasks"])
logger = get_logger("tasks_routes")

# REMOVE this - using proper logging
# def log_task_creation(title: str):
#     with open("task_log.txt", "a") as f:
#        f.write(f"Task created: {title}\n")

# ============ CREATE ============
@router.post("/")
def create_task(task: TaskCreate, background_tasks: BackgroundTasks, current_user=Depends(get_current_user_dep), db: Session = Depends(get_db)):
    # ADD THIS LOG
    logger.info(f"📝 CREATE TASK - User: {current_user.email} (ID: {current_user.id}) - Title: '{task.title}'")
    
    new_task = create_task_logic(task, current_user.id, db)
    
    # ADD THIS LOG
    logger.info(f"✅ TASK CREATED - User: {current_user.email}, Task ID: {new_task.id}")
    
    # Use proper logging
    background_tasks.add_task(lambda: logger.info(f"Background: Task '{task.title}' created by {current_user.email}"))

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
    current_user=Depends(get_current_user_dep),
    db: Session = Depends(get_db)
):
    logger.info(f"📋 FETCH TASKS - User: {current_user.email} (Page: {page}, Limit: {limit})")
    
    tasks = get_all_tasks_logic(current_user.id, page, limit, db, completed, sort)
    
    logger.info(f"✅ TASKS FETCHED - User: {current_user.email}, Count: {len(tasks)}")
    
    return {
        "success": True,
        "data": tasks,
        "page": page,
        "limit": limit,
        "message": "Tasks fetched successfully"
    }

# ============ READ ONE ============
@router.get("/{task_id}")
def get_task(task_id: int, current_user=Depends(get_current_user_dep), db: Session = Depends(get_db)):
    logger.info(f"🔍 GET TASK - User: {current_user.email}, Task ID: {task_id}")
    
    task = get_task_by_id_logic(task_id, current_user.id, db)

    if not task:
        logger.warning(f"❌ TASK NOT FOUND - User: {current_user.email}, Task ID: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")

    logger.info(f"✅ TASK RETRIEVED - User: {current_user.email}, Task: '{task.title}'")
    
    return {
        "success": True,
        "data": task,
        "message": "Task fetched successfully"
    }

# ============ UPDATE ============
@router.put("/{task_id}")
def update_task(task_id: int, task: TaskCreate, current_user=Depends(get_current_user_dep), db: Session = Depends(get_db)):
    logger.info(f"✏️ UPDATE TASK - User: {current_user.email}, Task ID: {task_id}, New Title: '{task.title}'")
    
    result = update_task_logic(task_id, task, current_user.id, db)

    if result is None:
        logger.warning(f"❌ UPDATE FAILED - Task {task_id} not found, User: {current_user.email}")
        raise HTTPException(status_code=404, detail="Task not found")

    if isinstance(result, dict) and "error" in result:
        logger.warning(f"⚠️ UPDATE BLOCKED - User: {current_user.email}, Task: {task_id}, Reason: {result['error']}")
        raise HTTPException(status_code=400, detail=result["error"])

    logger.info(f"✅ TASK UPDATED - User: {current_user.email}, Task ID: {task_id}")
    
    return {
        "success": True,
        "data": result,
        "message": "Task updated successfully"
    }

# ============ DELETE ============
@router.delete("/{task_id}")
def delete_task(task_id: int, current_user=Depends(get_current_user_dep), db: Session = Depends(get_db)):
    logger.info(f"🗑️ DELETE TASK - User: {current_user.email}, Task ID: {task_id}")
    
    result = delete_task_logic(task_id, current_user.id, db)

    if not result:
        logger.warning(f"❌ DELETE FAILED - Task {task_id} not found, User: {current_user.email}")
        raise HTTPException(status_code=404, detail="Task not found")

    logger.info(f"✅ TASK DELETED - User: {current_user.email}, Task ID: {task_id}")
    
    return {
        "success": True,
        "message": "Task deleted successfully"
    }

# ============ MARK COMPLETE ============
@router.patch("/{task_id}/complete")
def mark_complete(task_id: int, current_user=Depends(get_current_user_dep), db: Session = Depends(get_db)):
    logger.info(f"✅ MARK COMPLETE - User: {current_user.email}, Task ID: {task_id}")
    
    result = mark_complete_logic(task_id, current_user.id, db)

    if result is None:
        logger.warning(f"❌ MARK COMPLETE FAILED - Task {task_id} not found, User: {current_user.email}")
        raise HTTPException(status_code=404, detail="Task not found")

    if isinstance(result, dict) and "error" in result:
        logger.warning(f"⚠️ MARK COMPLETE BLOCKED - User: {current_user.email}, Task: {task_id}, Reason: {result['error']}")
        raise HTTPException(status_code=400, detail=result["error"])

    logger.info(f"✅ TASK COMPLETED - User: {current_user.email}, Task ID: {task_id}")
    
    return {
        "success": True,
        "data": result,
        "message": "Task marked as complete"
    }