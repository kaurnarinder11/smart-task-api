from app.models.user import User
from app.db.database import SessionLocal

def create_user_login(email:str, password:str):
    if len(password.strip()) == 0:
        return {"error": "Password cannot be empty"}
    db = SessionLocal()

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        db.close()
        return {"error": "user already exists"}
    user = User(email=email, password=password)

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return user

from app.models.user import User
from app.db.database import SessionLocal

def create_user_logic(email: str, password: str):
    # Validation
    if len(password.strip()) == 0:
        return {"error": "Password cannot be empty"}
    
    db = SessionLocal()
    
    # Check if user already exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        db.close()
        return {"error": "User already exists"}
    
    # Create user (NOTE: Password is plain text for now - we'll hash tomorrow)
    user = User(email=email, password=password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    
    return user

def login_user_logic(email: str, password: str):
    db = SessionLocal()
    
    user = db.query(User).filter(User.email == email).first()
    db.close()
    
    if not user or user.password != password:
        return {"error": "Invalid credentials"}
    
    return user
