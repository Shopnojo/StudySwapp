# =================== app/main.py ===================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chat import router as chat_router




from users import router as users_router
from posts import router as posts_router
from auth import router as auth_router

# ✅ Optional: Only needed if you're testing DB on startup
# from database import get_db  # Only if you need to test DB at startup

app = FastAPI()

# ✅ CORS setup - good for frontend/backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount routers (routes)
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(posts_router, prefix="/posts", tags=["Posts"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

# ✅ Health check
@app.get("/")
def home():
    return {"message": "StudySwapp Backend is up and running 🚀"}

# ✅ Optional: test DB connection on startup (not required)
# You can uncomment this to test DB once when app starts
# try:
#     conn = get_db()
#     print("✅ Database connected successfully!")
#     conn.close()
# except Exception as e:
#     print("❌ Database connection failed:", e)
