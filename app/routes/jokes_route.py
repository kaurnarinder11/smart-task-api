# backend/smart-task-api/app/routes/joke_routes.py

from fastapi import APIRouter
from app.services.external_api import get_joke

router = APIRouter(prefix="/joke", tags=["jokes"])

@router.get("/random")
def random_joke():
    """Get a random joke from external API"""
    result = get_joke()
    
    if result["success"]:
        return {
            "status": "success",
            "data": {
                "setup": result["setup"],
                "punchline": result["punchline"]
            }
        }
    else:
        return {
            "status": "error",
            "message": result["error"]
        }