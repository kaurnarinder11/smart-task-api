from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_token as create_access_token
from app.core.logger import get_logger

logger = get_logger("users_service")

def create_user_logic(email: str, password: str, db: Session):
    logger.info(f"Service: Creating user with email {email}")
    
    if len(password.strip()) == 0:
        logger.warning(f"Service: Password empty for {email}")
        return {"error": "Password cannot be empty"}

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        logger.warning(f"Service: User {email} already exists")
        return {"error": "User already exists"}

    hashed_password = hash_password(password)
    user = User(email=email, password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"Service: User {email} created with ID {user.id}")
    return user

def login_user_logic(email: str, password: str, db: Session):
    logger.info(f"Service: Login attempt for {email}")
    
    user = db.query(User).filter(User.email == email).first()

    if not user:
        logger.warning(f"Service: User {email} not found")
        return {"error": "Invalid credentials"}
    
    if not verify_password(password, user.password):
        logger.warning(f"Service: Invalid password for {email}")
        return {"error": "Invalid credentials"}

    token = create_access_token({"user_id": user.id})
    
    logger.info(f"Service: User {email} authenticated successfully")
    return {"access_token": token, "user_id": user.id, "email": user.email}