# otp.py
import random
import smtplib
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from mysql.connector import connect
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

from backend.database import get_db  # assuming get_db is your MySQL connector wrapper

load_dotenv()

router = APIRouter()

@router.post("/send-otp/{user_id}")
def send_otp(user_id: int, db=Depends(get_db)):
    otp = str(random.randint(100000, 999999))
    expires_at = datetime.now() + timedelta(minutes=10)

    cursor = db.cursor()

    # Get user email
    cursor.execute("SELECT college_email FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    recipient = result[0]

    #
