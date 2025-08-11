from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
import mysql.connector
from ..database import get_db
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic model for user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Hashing password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Route to register user
@router.post("/register")
def register_user(user: UserCreate, db=Depends(get_db)):
    cursor = db.cursor()
    try:
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")

        # Insert user with hashed password
        hashed_pw = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (user.username, user.email, hashed_pw)
        )
        db.commit()
        return {"message": "User registered successfully"}
    finally:
        cursor.close()
        db.close()

# Route to fetch user by email
@router.get("/{email}")
def get_user(email: str, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, username, email FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        cursor.close()
        db.close()
