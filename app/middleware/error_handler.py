"""
Global Error Handler Middleware
What: Catches ALL errors across your entire API in one place
Why: Instead of writing try-except in every route, write once here
"""

import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Create logger for this module
logger = logging.getLogger(__name__)

class GlobalErrorHandler(BaseHTTPMiddleware):
    """
    This middleware catches every error that happens in ANY route.
    
    How it works:
    1. Every request goes through this handler first
    2. If the route succeeds → return normal response
    3. If ANY error happens → caught here and handled properly
    
    Without this: Each route needs its own try-except blocks
    With this: Write once, applies to EVERY route automatically
    """
    
    async def dispatch(self, request: Request, call_next):
        try:
            # Try to process the request normally
            # This will call your actual route function
            response = await call_next(request)
            return response
            
        except HTTPException as http_exc:
            # FastAPI HTTP exceptions (400, 401, 404, etc.)
            # These are expected errors with proper status codes
            logger.warning(
                f"HTTP Exception: {http_exc.status_code} - {http_exc.detail} | "
                f"Path: {request.url.path} | Method: {request.method}"
            )
            # Pass through without changing (FastAPI already formatted it correctly)
            raise http_exc
            
        except Exception as e:
            # EVERY other error - database errors, logic errors, etc.
            # These are UNEXPECTED errors that should never happen in production
            
            error_type = type(e).__name__
            error_message = str(e)
            
            logger.error(
                f"UNHANDLED ERROR: {error_type} - {error_message} | "
                f"Path: {request.url.path} | Method: {request.method}",
                exc_info=True  # This adds full stack trace to logs
            )
            
            # IMPORTANT: Don't expose internal error details to the user (security risk!)
            # Return a generic message instead of the actual error
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error. Our team has been notified.",
                    "status": "error",
                    "error_code": "INTERNAL_SERVER_ERROR"
                }
            )