from fastapi import FastAPI
from database.db import create_table
from routers.auth import router as auth_router
from routers.todo import router as todo_router
from routers.user import router as user_router

app = FastAPI(
    title="LoopKaka's FastAPI Tutorial",
    version="0.0.1",
    description="Chapter 3 & 4: How to connect with database"
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(todo_router)

@app.on_event("startup")
def on_startup():
    create_table()