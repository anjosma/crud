import logging
from typing import Generator
from sqlmodel import Session

from app.database.sqlite import SQLiteDatabase

logger = logging.getLogger(__name__)

SQLITE_FILE_NAME = "database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"
SQLITE_CONNECT_ARGS = {"check_same_thread": False}

db = SQLiteDatabase(
    url=SQLITE_URL,
    connect_args=SQLITE_CONNECT_ARGS,
    echo=True
)

def get_session() -> Generator[Session, None, None]:
    """Dependency for getting database session"""
    logger.debug("Creating new database session")
    yield from db.get_session() 