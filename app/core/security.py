import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.models.user import User
from fastapi import HTTPException
from jose import JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET = "abc"
ALGORITHM = "HS256"


# 🔐 HASH PASSWORD
def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


# 🔐 VERIFY PASSWORD
def verify_password(password: str, hashed_password: bytes):
    return bcrypt.checkpw(password.encode(), hashed_password)


# 🔑 CREATE TOKEN
def create_token(data: dict):
    to_encode = data.copy()

    # add expiry
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

def get_current_user(token:str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
   
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_user_dep(token: str = Depends(oauth2_scheme)):
    return get_current_user(token)