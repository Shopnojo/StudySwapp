# chat.py
from fastapi import APIRouter, Depends, HTTPException
from mysql.connector import Error
from backend.database import get_db # Assuming your get_db is in database.py
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/send-message")
def send_message(sender_id: int, receiver_id: int, content: str, db=Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO messages (sender_id, receiver_id, content) VALUES (%s, %s, %s)",
            (sender_id, receiver_id, content)
        )
        db.commit()
        return {"msg": "Message sent"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        db.close()
