# backend/smart-task-api/app/routes/jokes_route.py

from fastapi import APIRouter, Depends, HTTPException
from app.services.external_api import get_joke
from app.core.security import get_current_user
from app.models.user import User
from app.core.logger import get_logger

router = APIRouter(prefix="/joke", tags=["jokes"])
logger = get_logger("jokes_route")

@router.get("/random")
def random_joke(current_user: User = Depends(get_current_user)):
    """Get a random joke from external API with proper error handling"""
    
    logger.info(f"User {current_user.email} requested a joke")
    
    # Call the external API service
    result = get_joke()
    
    # 🔥 IMPROVED: Use HTTPException instead of returning error object
    if not result["success"]:
        logger.warning(f"Joke API failed for user {current_user.email}: {result['error']}")
        raise HTTPException(
            status_code=503,  # Service Unavailable
            detail=f"Joke service unavailable: {result['error']}"
        )
    
    # Success case
    logger.info(f"Joke delivered successfully to {current_user.email}")
    return {
        "status": "success",
        "data": {
            "setup": result["setup"],
            "punchline": result["punchline"]
        }
    }

@router.get("/random/public")
def random_joke_public():
    """Public endpoint for jokes (no authentication required)"""
    
    logger.info("Public joke requested (no auth)")
    
    result = get_joke()
    
    if not result["success"]:
        logger.warning(f"Joke API failed for public request: {result['error']}")
        raise HTTPException(
            status_code=503,
            detail=f"Joke service unavailable: {result['error']}"
        )
    
    return {
        "status": "success",
        "data": {
            "setup": result["setup"],
            "punchline": result["punchline"]
        }
    }