from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from ..database import get_db

router = APIRouter()

# Pydantic model for creating a post
class PostCreate(BaseModel):
    user_id: int
    title: str
    content: str

# Pydantic model for returning posts
class PostOut(BaseModel):
    id: int
    user_id: int
    title: str
    content: str

# Route to create a new post
@router.post("/create")
def create_post(post: PostCreate, db=Depends(get_db)):
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO posts (user_id, title, content) VALUES (%s, %s, %s)",
            (post.user_id, post.title, post.content)
        )
        db.commit()
        post_id = cursor.lastrowid
        return {"message": "Post created successfully", "post_id": post_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()

# Route to fetch all posts
@router.get("/", response_model=List[PostOut])
def get_all_posts(db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM posts ORDER BY id DESC")
        posts = cursor.fetchall()
        return posts
    finally:
        cursor.close()
        db.close()

# Route to fetch posts by a specific user
@router.get("/user/{user_id}", response_model=List[PostOut])
def get_user_posts(user_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM posts WHERE user_id = %s ORDER BY id DESC", (user_id,))
        posts = cursor.fetchall()
        return posts
    finally:
        cursor.close()
        db.close()

# Optional: Get single post by ID
@router.get("/{post_id}", response_model=PostOut)
def get_post_by_id(post_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    finally:
        cursor.close()
        db.close()
