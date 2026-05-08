from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from datetime import datetime

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint for load balancers and monitoring"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
        "service": "smart-task-api",
        "version": "1.0.0"
    }

@router.get("/health/ready")
async def readiness_check():
    """Readiness check - called by load balancer before sending traffic"""
    return {"ready": True}

@router.get("/health/live")
async def liveness_check():
    """Liveness check - called by orchestrator to know if container should restart"""
    return {"alive": True}