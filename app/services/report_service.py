# app/services/report_service.py

import csv
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.user import User
from app.core.storage import get_storage
from app.core.config import settings
from app.core.logger import get_logger
import os

logger = get_logger("report_service")

def generate_task_report(user_id: int, db: Session, format: str = "txt"):
    """
    Generate a report of all tasks for a specific user.

    Args:
        user_id: The ID of the user
        db: Database session
        format: "txt" or "csv"

    Returns:
        dict with file path and summary info
    """
    tasks = db.query(Task).filter(Task.user_id == user_id).all()

    if not tasks:
        return {
            "message": "No tasks found for this user",
            "file_path": None,
            "summary": {"total": 0, "completed": 0, "pending": 0}
        }

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.completed)
    pending_tasks = total_tasks - completed_tasks

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"task_report_user_{user_id}_{timestamp}.{format}"
    
    # Use storage path (not hardcoded)
    storage_path = f"{settings.REPORTS_DIR}/{filename}"
    
    # Generate content based on format
    if format == "csv":
        content = generate_csv_content(tasks, total_tasks, completed_tasks, pending_tasks)
    else:
        content = generate_txt_content(tasks, total_tasks, completed_tasks, pending_tasks)
    
    # Save using storage abstraction (auto-switches to S3 in production!)
    storage = get_storage()
    saved_path = storage.save(storage_path, content)
    
    logger.info(f"Report saved: {saved_path} (user_id={user_id}, format={format})")
    
    # Determine display path (show full URL for S3, local path for local)
    display_path = saved_path if "s3://" in saved_path or "https://" in saved_path else storage_path

    return {
        "message": f"Report generated successfully",
        "file_path": display_path,
        "format": format,
        "summary": {
            "total": total_tasks,
            "completed": completed_tasks,
            "pending": pending_tasks
        }
    }


def generate_txt_content(tasks, total, completed, pending):
    """Generate text content (returns string, doesn't write to file)"""
    content = []
    
    content.append("=" * 50 + "\n")
    content.append("TASK REPORT\n")
    content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    content.append("=" * 50 + "\n\n")
    
    content.append("SUMMARY\n")
    content.append("-" * 30 + "\n")
    content.append(f"Total Tasks: {total}\n")
    content.append(f"Completed: {completed}\n")
    content.append(f"Pending: {pending}\n")
    content.append("\n" + "=" * 50 + "\n\n")
    
    content.append("TASK DETAILS\n")
    content.append("-" * 30 + "\n\n")
    
    completed_tasks = [t for t in tasks if t.completed]
    pending_tasks = [t for t in tasks if not t.completed]
    
    if pending_tasks:
        content.append("PENDING TASKS:\n")
        content.append("-" * 20 + "\n")
        for idx, task in enumerate(pending_tasks, 1):
            content.append(f"{idx}. {task.title}\n")
        content.append("\n")
    
    if completed_tasks:
        content.append("COMPLETED TASKS:\n")
        content.append("-" * 20 + "\n")
        for idx, task in enumerate(completed_tasks, 1):
            content.append(f"{idx}. {task.title}\n")
        content.append("\n")
    
    content.append("=" * 50 + "\n")
    content.append("End of Report\n")
    
    return "".join(content)


def generate_csv_content(tasks, total, completed, pending):
    """Generate CSV content (returns string, doesn't write to file)"""
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["# TASK REPORT SUMMARY"])
    writer.writerow(["Generated Date", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow(["Total Tasks", total])
    writer.writerow(["Completed Tasks", completed])
    writer.writerow(["Pending Tasks", pending])
    writer.writerow([])
    
    writer.writerow(["TASK DETAILS"])
    writer.writerow(["Task ID", "Title", "Status", "Created Date"])
    
    for task in tasks:
        status = "Completed" if task.completed else "Pending"
        created_date = task.created_date.strftime("%Y-%m-%d") if task.created_date else "N/A"
        writer.writerow([task.id, task.title, status, created_date])
    
    return output.getvalue()