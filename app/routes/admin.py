from fastapi import APIRouter, Depends, HTTPException
from app.services.cache import cache
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/cache/stats")
async def get_cache_stats(current_user: User = Depends(get_current_user)):
    """Get cache statistics (admin only)"""
    # Only allow admin users (you can add is_admin field to User)
    if current_user.email != "admin@example.com":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return {
        "cache_size": len(cache._cache),
        "cache_keys": list(cache._cache.keys())
    }

@router.delete("/cache/clear")
async def clear_cache(current_user: User = Depends(get_current_user)):
    """Clear entire cache (admin only)"""
    if current_user.email != "admin@example.com":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    cache.clear()
    return {"message": "Cache cleared successfully"}