"""
main.py - FastAPI application entry point.

Run with:
    uvicorn main:app --reload
Docs available at:
    http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import os
from dotenv import load_dotenv

# Load .env from backend root
load_dotenv()

from app.database import Base, engine
from app.routes.transactions import router as tx_router
from app.routes.dashboard import dashboard_router, budget_router, recurring_router, savings_router
from app.routes.ai import router as ai_router
from app import scheduler

# Create all tables on startup (Alembic handles migrations in production)
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the background task
    task = asyncio.create_task(scheduler.recurring_task_loop())
    yield
    # Cancel the task on shutdown
    task.cancel()

app = FastAPI(
    title="Personal Finance Tracker",
    description="Track income, expenses, budgets, and recurring transactions.",
    version="1.0.0",
    lifespan=lifespan
)

# Allow React frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(tx_router)
app.include_router(dashboard_router)
app.include_router(budget_router)
app.include_router(recurring_router)
app.include_router(savings_router)
app.include_router(ai_router)



@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Personal Finance Tracker API is running."}
