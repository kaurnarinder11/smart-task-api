import bcrypt
from jose import jwt
from datetime import datetime, timedelta

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