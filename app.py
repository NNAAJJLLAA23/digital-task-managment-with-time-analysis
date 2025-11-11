from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3
import hashlib
import numpy as np

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    title: str
    start_time: str
    end_time: str
    user: str

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

@app.post("/tasks")
def add_task(task: Task):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=?", (task.user,))
    user = cur.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user["id"]
    cur.execute(
        "INSERT INTO tasks (user_id, title, start_time, end_time) VALUES (?, ?, ?, ?)",
        (user_id, task.title, task.start_time, task.end_time)
    )
    conn.commit()
    conn.close()
    return {"message": "Task added!"}
