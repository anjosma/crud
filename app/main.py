import logging
import os
from fastapi import FastAPI
from app.routes import users, health
from app.dependencies import db

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="User Management API",
    description="User management API with SQLite database",
    version="1.0.0",
    root_path="/api/v1"
)

logger.info("Starting application")

app.include_router(users.router)
logger.debug("Included users router")

app.include_router(health.router)
logger.debug("Included health router")

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
