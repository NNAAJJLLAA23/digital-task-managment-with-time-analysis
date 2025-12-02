from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3

router = APIRouter()
conn = sqlite3.connect("task.db")
cursor = conn.cursor()

class Task(BaseModel):
    username: str
    title: str
    start_time: str
    end_time: str

@router.get("/tasks/")
def get_tasks(username: str):
    cursor.execute("SELECT title, start_time, end_time FROM tasks WHERE username=?", (username,))
    tasks = cursor.fetchall()
    return [{"title": t[0], "start_time": t[1], "end_time": t[2]} for t in tasks]

@router.post("/tasks/")
def add_task(task: Task):
    cursor.execute("INSERT INTO tasks (username, title, start_time, end_time) VALUES (?, ?, ?, ?)",
                   (task.username, task.title, task.start_time, task.end_time))
    conn.commit()
    return {"message": "Task added successfully"}

