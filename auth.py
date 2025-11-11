from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3, hashlib

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/register")
def register(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                    (user.username, hash_password(user.password)))
        conn.commit()
        return {"message": "User registered!"}
    except:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()

@app.post("/login")
def login(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (user.username, hash_password(user.password)))
    result = cur.fetchone()
    conn.close()
    if result:
        return {"message": "Login successful!"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
uvicorn auth:app --reload
