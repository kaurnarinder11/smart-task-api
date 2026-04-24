from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token
from app.core.logger import get_logger
from fastapi import HTTPException

logger = get_logger("users_service")

def create_user_logic(user_data: UserCreate, db: Session):
    logger.info(f"Creating user with email: {user_data.email}")
    
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(400, "Email already registered")
        else:
            raise HTTPException(400, "Username already taken")
    
    hashed_pwd = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"User created successfully with ID: {db_user.id}")
    return db_user

def login_user_logic(email: str, password: str, db: Session):
    logger.info(f"Login attempt for email: {email}")
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(401, "Invalid email or password")
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")
    
    token = create_access_token(data={"sub": str(user.id), "email": user.email})
    
    logger.info(f"User {user.email} logged in successfully")
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "username": user.username
    }

def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user
