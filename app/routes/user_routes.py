from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.users_service import create_user_logic, login_user_logic
from app.core.security import get_current_user_dep
from fastapi import BackgroundTasks
from app.core.logger import get_logger

router = APIRouter(prefix="/auth", tags=["authentication"])

logger = get_logger("user_routes")

# REMOVE this old file logging - we're using proper logging now!
# def log_signup(email: str):
#     with open("signup_log.txt", "a") as f:
#         f.write(f"New user signed up: {email}\n")

@router.post("/signup")
def signup(email: str, password: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # ADD THIS LOG
    logger.info(f"📝 SIGNUP ATTEMPT - Email: {email}")
    
    result = create_user_logic(email, password, db)
    
    # ADD THESE LOGS based on result
    if result and "error" in result:
        logger.warning(f"❌ SIGNUP FAILED - {email} - Reason: {result['error']}")
    else:
        logger.info(f"✅ SIGNUP SUCCESS - New user created: {email} (ID: {result.id})")
        # Use proper logging instead of file writing
        background_tasks.add_task(lambda: logger.info(f"Background log: User {email} signed up"))
    
    return result

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    # ADD THIS LOG
    logger.info(f"🔐 LOGIN ATTEMPT - Email: {email}")
    
    result = login_user_logic(email, password, db)
    
    # ADD THESE LOGS based on result
    if result and "error" in result:
        logger.warning(f"❌ LOGIN FAILED - {email} - Reason: {result['error']}")
    else:
        logger.info(f"✅ LOGIN SUCCESS - User: {email} (ID: {result['user_id']})")
    
    return result

@router.get("/profile")
def profile(current_user=Depends(get_current_user_dep)):
    logger.info(f"👤 PROFILE ACCESS - User: {current_user.email} (ID: {current_user.id})")
    return current_user