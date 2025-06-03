import logging
import os
from fastapi import FastAPI
from app.routes import users, health
from app.dependencies import db

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, os.getenv("LOG_LEVEL", "INFO")))

app = FastAPI(
    title="User Management API",
    description="User management API with SQLite database",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(health.router)

@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    logger.info("Initializing database")
    db.create_db_and_tables()

@app.on_event("shutdown")
def on_shutdown():
    """Close database connection on shutdown"""
    logger.info("Closing database connection")
    db.close_connection()
