# app/utils/auth_utils.py or similar location

from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Secret key and algorithm for JWT
SECRET_KEY = os.getenv("S1t@moyJu_ahj0spnoCbahtjS3o")
ALGORITHM = "HS256"

# Adjust this based on your actual route
# If your login route is under /users/token (as in your main.py), keep this:
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


router = APIRouter()

@router.get("/auth")
def auth_root():
    return {"message": "Auth route working"}

def create_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    """
    Create a JWT token with given data and expiration time.
    """
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str = Depends(oauth2_scheme)):
    """
    Decode and validate JWT token. Used as a dependency.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
