import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.database import MongoDBUsers
import os

# JWT Secret and Algorithm
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User and Token models


class User(BaseModel):
    username: str
    password: str


class UserInDB(User):
    hashed_password: str

# Authenticate user


def authenticate_user(users_db: MongoDBUsers, username: str, password: str):
    user = users_db.get_user(username)
    if not user:
        return None
    # assuming 'password' is stored in hashed form
    if not verify_password(password, user["password"]):
        return None
    return user

# Password hashing and verification


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT creation and verification


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + \
            expires_delta  # Always use UTC time
    else:
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        # Token has expired
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        # General error in decoding JWT (e.g., invalid signature)
        raise HTTPException(status_code=401, detail="Invalid token")
