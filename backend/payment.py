import razorpay
import os
from dotenv import load_dotenv
from fastapi import APIRouter

load_dotenv()

router = APIRouter()

razorpay_client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY"),
        os.getenv("RAZORPAY_SECRET")
    )
)

@router.post("/create-payment/{user_id}")
def create_payment(user_id: int, amount: int):
    payment = razorpay_client.order.create({
        "amount": amount * 100,  # amount in paise
        "currency": "INR",
        "payment_capture": "1"
    })
    # Save order details to DB (optional)
    return payment
