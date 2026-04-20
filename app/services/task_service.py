from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.core.logger import get_logger

logger = get_logger("task_service")

# ============ CREATE ============
def create_task_logic(task: TaskCreate, user_id: int, db: Session):
    """Create a new task in database"""
    logger.info(f"Service: Creating task for user {user_id}")
    
    db_task = Task(title=task.title, completed=task.completed, user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    logger.debug(f"Service: Task saved to DB with ID {db_task.id}")
    return db_task

# ============ READ ALL ============
def get_all_tasks_logic(user_id, page, limit, db: Session, completed=None, sort="desc"):
    logger.debug(f"Service: Fetching tasks for user {user_id}, page {page}")
    skip = (page - 1) * limit

    query = db.query(Task).filter(Task.user_id == user_id)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    if sort == "desc":
        query = query.order_by(Task.id.desc())
    else:
        query = query.order_by(Task.id.asc())

    return query.offset(skip).limit(limit).all()

# ============ READ ONE ============
def get_task_by_id_logic(task_id: int, user_id: int, db: Session):
    """Get a single task by ID for the given user"""
    logger.debug(f"Service: Fetching task {task_id} for user {user_id}")
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

# ============ UPDATE ============
def update_task_logic(task_id: int, updated_data: TaskCreate, user_id: int, db: Session):
    """
    Update an existing task
    Returns: Updated task OR None if not found
    """
    logger.info(f"Service: Updating task {task_id} for user {user_id}")
    
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        logger.warning(f"Service: Task {task_id} not found for user {user_id}")
        return None

    if task.completed:
        logger.warning(f"Service: Cannot update completed task {task_id}")
        return {"error": "completed_task_cannot_be_updated"}

    if len(updated_data.title.strip()) == 0:
        logger.warning(f"Service: Empty title for task {task_id}")
        return {"error": "title_cannot_be_empty"}

    task.title = updated_data.title
    task.completed = updated_data.completed

    db.commit()
    db.refresh(task)
    
    logger.info(f"Service: Task {task_id} updated successfully")
    return task

# ============ DELETE ============
def delete_task_logic(task_id: int, user_id: int, db: Session):
    """
    Delete a task by ID
    Returns: True if deleted, False if not found
    """
    logger.info(f"Service: Deleting task {task_id} for user {user_id}")
    
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        logger.warning(f"Service: Task {task_id} not found for deletion")
        return False

    db.delete(task)
    db.commit()
    
    logger.info(f"Service: Task {task_id} deleted successfully")
    return True

# ============ MARK COMPLETE ============
def mark_complete_logic(task_id: int, user_id: int, db: Session):
    """
    Mark a task as completed
    Returns: Updated task OR None if not found OR error if already completed
    """
    logger.info(f"Service: Marking task {task_id} complete for user {user_id}")
    
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        logger.warning(f"Service: Task {task_id} not found for completion")
        return None

    if task.completed:
        logger.warning(f"Service: Task {task_id} already completed")
        return {"error": "task_already_completed"}

    task.completed = True
    db.commit()
    db.refresh(task)
    
    logger.info(f"Service: Task {task_id} marked complete")
    return task