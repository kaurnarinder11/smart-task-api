from fastapi import APIRouter, Depends
from app.services.users_service import create_user_logic, login_user_logic
from app.core.security import get_current_user_dep

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup")
def signup(email: str, password: str):
    return create_user_logic(email, password)


@router.post("/login")
def login(email: str, password: str):
    return login_user_logic(email, password)


@router.get("/profile")
def profile(current_user = Depends(get_current_user_dep)):
    return current_user