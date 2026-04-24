from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.users_service import create_user_logic, login_user_logic
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.logger import get_logger

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = get_logger("user_routes")

@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    logger.info(f"Signup attempt for email: {user_data.email}")
    return create_user_logic(user_data, db)

@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    logger.info(f"Login attempt for email: {login_data.email}")
    return login_user_logic(login_data.email, login_data.password, db)