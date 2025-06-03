from abc import ABC, abstractmethod
from typing import Generator, Any

from sqlmodel import Session

class Database(ABC):
    @abstractmethod
    def __init__(self, url: str, **kwargs: Any) -> None:
        """Initialize database connection"""
        pass

    @abstractmethod
    def create_db_and_tables(self) -> None:
        """Create database and tables"""
        pass

    @abstractmethod
    def get_session(self) -> Generator[Session, None, None]:
        """Get database session"""
        pass

    @abstractmethod
    def get_engine(self) -> Any:
        """Get database engine"""
        pass 