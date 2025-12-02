from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db_connection

router = APIRouter()

class Task(BaseModel):
    username: str
    title: str
    start_time: str
    end_time: str

@router.get("/")
def get_tasks(username: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE username=?", (username,))
    tasks = cur.fetchall()
    conn.close()
    return [dict(t) for t in tasks]

@router.post("/")
def add_task(task: Task):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (username, title, start_time, end_time) VALUES (?, ?, ?, ?)",
                (task.username, task.title, task.start_time, task.end_time))
    conn.commit()
    conn.close()
    return {"message": "Task added!"}




