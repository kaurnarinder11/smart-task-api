from app.models.user import User
from app.db.database import SessionLocal
from app.core.security import hash_password, verify_password, create_token as create_access_token  # NEW imports

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
    
    # CHANGED: Hash the password before storing
    hashed_password = hash_password(password)
    user = User(email=email, password=hashed_password)  # Store hashed version
    
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    
    return user

def login_user_logic(email: str, password: str):
    db = SessionLocal()
    
    user = db.query(User).filter(User.email == email).first()
    db.close()
    
    #  CHANGED: Verify password using hash comparison, not plain text
    if not user or not verify_password(password, user.password):
        return {"error": "Invalid credentials"}
    
    #  NEW: Create JWT token on successful login
    token = create_access_token(user.id)
    
    #  CHANGED: Return token instead of user object
    return {"access_token": token, "user_id": user.id, "email": user.email}