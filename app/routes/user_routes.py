from fastapi import APIRouter, Depends
from app.services.users_service import create_user_logic, login_user_logic
from app.core.security import get_current_user_dep
from fastapi import BackgroundTasks

router = APIRouter(prefix="/auth", tags=["authentication"])

def log_signup(email: str):
    with open("signup_log.txt", "a") as f:
        f.write(f"New user signed up: {email}\n")

@router.post("/signup")
def signup(email: str, password: str, background_tasks: BackgroundTasks):
    result = create_user_logic(email, password)

    # add background task
    background_tasks.add_task(log_signup, email)
    
    return result


@router.post("/login")
def login(email: str, password: str):
    return login_user_logic(email, password)


@router.get("/profile")
def profile(current_user = Depends(get_current_user_dep)):
    return current_user