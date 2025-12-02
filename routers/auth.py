from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
from database import get_db_connection

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
        conn.commit()
        return {"message": "Account created!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()

@router.post("/login")
def login(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, user.password))
    db_user = cur.fetchone()
    conn.close()
    if db_user:
        return {"message": "Logged in successfully!"}
    else:
        raise HTTPException(status_code=400, detail="Wrong username or password")

