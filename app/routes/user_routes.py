from fastapi import APIRouter, HTTPException
from app.services.users_service import create_user_logic, login_user_logic

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup")
def signup(email: str, password: str):
    result = create_user_logic(email, password)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {"message": "User created successfully", "user_id": result.id, "email": result.email}

@router.post("/login")
def login(email: str, password: str):
    result = login_user_logic(email, password)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    
    return {"message": "Login successful", "user_id": result.id, "email": result.email}