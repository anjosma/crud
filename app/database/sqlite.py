import logging
from typing import Generator, Any
from sqlmodel import Session, SQLModel, create_engine

from app.database import Database

logger = logging.getLogger(__name__)

class SQLiteDatabase(Database):
    def __init__(self, url: str, **kwargs: Any) -> None:
        """Initialize SQLite database connection
        
        Args:
            url (str): Database URL in format sqlite:///path/to/database.db
            **kwargs: Additional arguments
        """
        self.url = url
        self.kwargs = kwargs
        self._engine = None

    def get_engine(self) -> Any:
        """Get or create SQLite engine"""
        if self._engine is None:
            logger.debug(f"Creating new SQLite engine with URL: {self.url}")
            self._engine = create_engine(
                self.url,
                **self.kwargs
            )
        return self._engine

    def create_db_and_tables(self) -> None:
        """Create database and tables"""
        logger.info("Creating SQLite database and tables")
        SQLModel.metadata.create_all(self.get_engine())

    def get_session(self) -> Generator[Session, None, None]:
        """Get database session"""
        logger.debug("Creating new SQLite database session")
        with Session(self.get_engine()) as session:
            yield session

    def close_connection(self) -> None:
        """Close database connection"""
        if self._engine is not None:
            logger.info("Closing SQLite database connection")
            self._engine.dispose()
            self._engine = None 