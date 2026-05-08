from fastapi import APIRouter, Depends
from app.services.cache import cached
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/")
@cached(ttl_seconds=300, key_prefix="news")  # ← Cache for 5 minutes
async def get_news(
    current_user: User = Depends(get_current_user)
):
    """Get news from external API (cached for 5 minutes)"""
    # Your existing news fetching code here
    # Example:
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get("https://newsapi.org/v2/top-headlines", params={
            "country": "us",
            "apiKey": "YOUR_API_KEY"
        })
        return response.json()