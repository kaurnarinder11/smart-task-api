# app/services/task_service.py
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.db.database import SessionLocal

# ============ CREATE ============
def create_task_logic(task: TaskCreate, user_id: int):
    """Create a new task in database"""
    db = SessionLocal()
    try:
        db_task = Task(title=task.title, completed=task.completed, user_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    finally:
        db.close()

# ============ READ ALL ============
def get_all_tasks_logic(user_id, page, limit, completed=None, sort="desc"):
    db = SessionLocal()
    try:
        skip = (page - 1) * limit

        query = db.query(Task).filter(Task.user_id == user_id)

        if completed is not None:
            query = query.filter(Task.completed == completed)

        # SORTING
        if sort == "desc":
            query = query.order_by(Task.id.desc())
        else:
            query = query.order_by(Task.id.asc())

        tasks = query.offset(skip).limit(limit).all()

        return tasks
    finally:
        db.close()

# ============ UPDATE ============
def update_task_logic(task_id: int, updated_data: TaskCreate, user_id: int):
    """
    Update an existing task
    Returns: Updated task OR None if not found
    """
    db = SessionLocal()
    try:
        # Step 1: Find the task
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        
        # Step 2: If not found, return None
        if not task:
            return None
        
        # Step 3: BUSINESS RULE 1 - Cannot update completed tasks
        if task.completed:
            # You can handle this differently - let's return a special response
            return {"error": "completed_task_cannot_be_updated"}
        
        # Step 4: BUSINESS RULE 2 - Title cannot be empty
        if len(updated_data.title.strip()) == 0:
            return {"error": "title_cannot_be_empty"}
        
        # Step 5: Update the fields
        task.title = updated_data.title
        task.completed = updated_data.completed
        
        # Step 6: Save to database
        db.commit()
        db.refresh(task)
        
        return task
        
    finally:
        db.close()

# ============ DELETE ============
def delete_task_logic(task_id: int, user_id: int):
    """
    Delete a task by ID
    Returns: True if deleted, False if not found
    """
    db = SessionLocal()
    try:
        # Step 1: Find the task
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        
        # Step 2: If not found, return False
        if not task:
            return False
        
        # Step 3: Delete the task
        db.delete(task)
        db.commit()
        
        return True
        
    finally:
        db.close()

# ============ MARK COMPLETE (CHALLENGE) ============
def mark_complete_logic(task_id: int, user_id: int):
    """
    Mark a task as completed
    Returns: Updated task OR None if not found OR error if already completed
    """
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        
        if not task:
            return None
        
        if task.completed:
            return {"error": "task_already_completed"}
        
        task.completed = True
        db.commit()
        db.refresh(task)
        
        return task
        
    finally:
        db.close()