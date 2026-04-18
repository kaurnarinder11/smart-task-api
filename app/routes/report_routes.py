# backend/smart-task-api/app/routes/report_routes.py

from fastapi import APIRouter, Depends, Query
from app.services.report_service import generate_task_report
from app.core.security import get_current_user_dep

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/tasks")
def get_task_report(
    format: str = Query("txt", regex="^(txt|csv)$"),
    current_user = Depends(get_current_user_dep)
):
    """
    Generate a report of all tasks for the logged-in user.
    
    - **format**: "txt" for text report, "csv" for CSV export
    """
    result = generate_task_report(current_user.id, format=format)
    return result