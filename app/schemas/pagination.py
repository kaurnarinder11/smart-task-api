from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from fastapi import Query

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Pagination query parameters"""
    skip: int = Query(0, ge=0, description="Number of records to skip")
    limit: int = Query(20, ge=1, le=100, description="Number of records to return")
    
    class Config:
        json_schema_extra = {
            "example": {
                "skip": 0,
                "limit": 20
            }
        }

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response with metadata"""
    data: List[T]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool
    next_url: Optional[str] = None
    previous_url: Optional[str] = None
    
    @classmethod
    def create(cls, data: List[T], total: int, skip: int, limit: int, request_url: str):
        """Factory method to create paginated response with URLs"""
        has_next = skip + limit < total
        has_previous = skip > 0
        
        next_url = f"{request_url}?skip={skip + limit}&limit={limit}" if has_next else None
        previous_url = f"{request_url}?skip={max(0, skip - limit)}&limit={limit}" if has_previous else None
        
        return cls(
            data=data,
            total=total,
            skip=skip,
            limit=limit,
            has_next=has_next,
            has_previous=has_previous,
            next_url=next_url,
            previous_url=previous_url
        )