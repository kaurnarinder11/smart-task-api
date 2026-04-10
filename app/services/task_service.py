
#TASK SERVICE WITH DATABASE


from app.db.database import SessionLocal
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def create_task_logic(task: TaskCreate):
    """Create a new task in database"""
    
    # BUSINESS RULE: Title cannot be empty or just spaces
    if not task.title or len(task.title.strip()) == 0:
        return {"error": "Title cannot be empty"}
    
    # BUSINESS RULE: Title must be at least 3 characters
    if len(task.title.strip()) < 3:
        return {"error": "Title must be at least 3 characters"}
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create new Task object (NOT saved yet)
        new_task = Task(
            title=task.title.strip(),
            completed=task.completed if hasattr(task, 'completed') else False
        )
        
        # Add to session (stage for saving)
        db.add(new_task)
        
        # Commit to database (actually save)
        db.commit()
        
        # Refresh to get the auto-generated ID
        db.refresh(new_task)
        
        return new_task
    except Exception as e:
        # If something goes wrong, undo changes
        db.rollback()
        raise e
    finally:
        # ALWAYS close the session
        db.close()


def get_tasks_logic():
    """Get all tasks from database"""
    
    db = SessionLocal()
    
    try:
        # Query all tasks
        tasks = db.query(Task).all()
        return tasks
    finally:
        db.close()


def get_task_by_id_logic(task_id: int):
    """Get a single task by ID"""
    
    db = SessionLocal()
    
    try:
        # Query specific task
        task = db.query(Task).filter(Task.id == task_id).first()
        return task
    finally:
        db.close()


def update_task_logic(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    
    db = SessionLocal()
    
    try:
        # Find the task
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            return None
        
        # Update only fields that are provided
        if task_update.title is not None:
            if len(task_update.title.strip()) < 3:
                return {"error": "Title must be at least 3 characters"}
            task.title = task_update.title.strip()
        
        if task_update.completed is not None:
            task.completed = task_update.completed
        
        # Save changes
        db.commit()
        db.refresh(task)
        
        return task
    finally:
        db.close()


def delete_task_logic(task_id: int):
    """Delete a task"""
    
    db = SessionLocal()
    
    try:
        # Find the task
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            return False
        
        # Delete it
        db.delete(task)
        db.commit()
        
        return True
    finally:
        db.close()