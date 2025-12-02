from fastapi import FastAPI
from routers import auth, tasks
from database import create_tables

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(tasks.router, prefix="/tasks")

@app.on_event("startup")
def startup():
    create_tables()

