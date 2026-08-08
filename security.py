from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
BASE_DIR = Path(__file__).resolve().parent.parent
from pathlib import Path

SECRET_KEY = SECRET_KEY_FILE = BASE_DIR / 'secret_key.txt'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

try:
    with open(SECRET_KEY_FILE, 'r', encoding='utf-8') as f:
        SECRET_KEY = f.read().strip()
except FileNotFoundError:
    SECRET_KEY = 'django-insecure-development-key-change-me'
def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

def get_password_hash(password):

    return password

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
