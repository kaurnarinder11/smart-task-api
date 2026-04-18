# app/services/report_service.py

import csv
from datetime import datetime
from app.db.database import SessionLocal
from app.models.task import Task
from app.models.user import User

def generate_task_report(user_id: int, format: str = "txt"):
    """
    Generate a report of all tasks for a specific user.
    
    Args:
        user_id: The ID of the user
        format: "txt" or "csv"
    
    Returns:
        dict with file path and summary info
    """
    
    db = SessionLocal()
    
    try:
        # Get user's tasks
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        
        if not tasks:
            return {
                "message": "No tasks found for this user",
                "file_path": None,
                "summary": {"total": 0, "completed": 0, "pending": 0}
            }
        
        # Calculate summary stats
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.completed)
        pending_tasks = total_tasks - completed_tasks
        
        # Create filename with timestamp to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"task_report_user_{user_id}_{timestamp}.{format}"
        file_path = f"reports/{filename}"  # Will save in reports folder
        
        # Ensure reports directory exists
        import os
        os.makedirs("reports", exist_ok=True)
        
        # Generate report based on format
        if format == "csv":
            generate_csv_report(file_path, tasks, total_tasks, completed_tasks, pending_tasks)
        else:
            generate_txt_report(file_path, tasks, total_tasks, completed_tasks, pending_tasks)
        
        return {
            "message": f"Report generated successfully",
            "file_path": file_path,
            "format": format,
            "summary": {
                "total": total_tasks,
                "completed": completed_tasks,
                "pending": pending_tasks
            }
        }
        
    finally:
        db.close()


def generate_txt_report(file_path, tasks, total, completed, pending):
    """Generate a text format report"""
    
    with open(file_path, "w") as f:
        # Header
        f.write("=" * 50 + "\n")
        f.write("TASK REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        # Summary Section
        f.write("📊 SUMMARY\n")
        f.write("-" * 30 + "\n")
        f.write(f"Total Tasks: {total}\n")
        f.write(f"Completed: {completed} ✅\n")
        f.write(f"Pending: {pending} ⏳\n")
        f.write("\n" + "=" * 50 + "\n\n")
        
        # Task Details Section
        f.write("📋 TASK DETAILS\n")
        f.write("-" * 30 + "\n\n")
        
        # Separate completed and pending
        completed_tasks = [t for t in tasks if t.completed]
        pending_tasks = [t for t in tasks if not t.completed]
        
        if pending_tasks:
            f.write("⏳ PENDING TASKS:\n")
            f.write("-" * 20 + "\n")
            for idx, task in enumerate(pending_tasks, 1):
                f.write(f"{idx}. {task.title}\n")
            f.write("\n")
        
        if completed_tasks:
            f.write("✅ COMPLETED TASKS:\n")
            f.write("-" * 20 + "\n")
            for idx, task in enumerate(completed_tasks, 1):
                f.write(f"{idx}. {task.title}\n")
            f.write("\n")
        
        f.write("=" * 50 + "\n")
        f.write("End of Report\n")


def generate_csv_report(file_path, tasks, total, completed, pending):
    """Generate a CSV format report"""
    
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        
        # Write summary section
        writer.writerow(["# TASK REPORT SUMMARY"])
        writer.writerow(["Generated Date", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow(["Total Tasks", total])
        writer.writerow(["Completed Tasks", completed])
        writer.writerow(["Pending Tasks", pending])
        writer.writerow([])  # Empty row
        
        # Write task details header
        writer.writerow(["TASK DETAILS"])
        writer.writerow(["Task ID", "Title", "Status", "Created Date"])
        
        # Write each task
        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            created_date = task.created_date.strftime("%Y-%m-%d") if task.created_date else "N/A"
            writer.writerow([task.id, task.title, status, created_date])