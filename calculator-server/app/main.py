import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

from app.routers import calculator, history

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(
    os.environ.get("DATABASE_URL", "sqlite://"), pool_pre_ping=True
)


@app.get("/")
def read_root():
    return {"message": "FastAPI + MySQL running!"}


@app.get("/test-db")
def test_db():
    with engine.connect() as conn:
        return {"db_result": conn.execute(text("SELECT 1")).scalar_one()}


app.include_router(calculator.router)
app.include_router(history.router)
