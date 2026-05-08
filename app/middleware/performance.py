import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log slow requests
        if duration > 1.0:  # 1 second threshold
            logger.warning(
                f"Slow request: {request.method} {request.url.path} - {duration:.2f}s"
            )
        
        # Add header with response time
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        
        return response