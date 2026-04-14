from fastapi import APIRouter, HTTPException
from app.services.users_service import create_user_logic, login_user_logic
from app.core.security import hash_password, verify_password, create_token
from jose import jwt
from app.core.security import SECRET, ALGORITHM

router = APIRouter(prefix="/auth", tags=["authentication"])

stored_hash = None

@router.post("/signup")
def signup(email: str, password: str):
    global stored_hash
    stored_hash = hash_password(password)
    return {"msg": "user created"}

@router.post("/login")
def login(email: str, password: str):
    global stored_hash
   
    if stored_hash is None:
        return{"error": "no user found"}
    
    if not verify_password(password, stored_hash):
        return {"error":"wrong password"}
    
    token = create_token({"user_id":1})

    return {"access_token": token}

@router.get("/profile")
def profile(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms= [ALGORITHM])
        return data
        print(token)
    except:
        
        return {"error": "invalid token"}