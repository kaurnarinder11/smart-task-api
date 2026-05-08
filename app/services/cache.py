import time
import hashlib
import json
from functools import wraps
from typing import Any, Dict, Optional

class SimpleCache:
    """
    Simple in-memory cache with TTL support.
    Note: For production, use Redis. This is for learning/demo.
    """
    
    def __init__(self):
        self._cache: Dict[str, tuple[Any, float]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                return value
            # Expired, remove it
            del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: int = 60):
        """Store value in cache with TTL"""
        self._cache[key] = (value, time.time() + ttl_seconds)
    
    def clear(self):
        """Clear entire cache"""
        self._cache.clear()
    
    def delete(self, key: str):
        """Delete specific key"""
        if key in self._cache:
            del self._cache[key]

# Global cache instance
cache = SimpleCache()

def cached(ttl_seconds: int = 60, key_prefix: str = ""):
    """
    Decorator to cache function results.
    
    Usage:
        @cached(ttl_seconds=300)  # Cache for 5 minutes
        async def get_news():
            return await fetch_news()
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{key_prefix or func.__name__}:{hashlib.md5(json.dumps(kwargs, sort_keys=True).encode()).hexdigest()}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            return result
        return wrapper
    return decorator