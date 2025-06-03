import logging
from typing import List
from sqlmodel import Session, select

from app.models.user import User
from app.exceptions import UserNotFoundError, UserAlreadyExistsError

logger = logging.getLogger(__name__)

class UserRepository:
    """Repository for managing user data in the database.

    This class handles all database operations related to users, following
    the repository pattern to encapsulate data access logic.

    Attributes:
        session (Session): The SQLModel session for database operations.
    """

    def __init__(self, session: Session):
        """Initialize the UserRepository.

        Args:
            session (Session): Database session to use for operations.
        """
        self.session = session

    def create(self, user: User) -> User:
        """Create a new user in the database.

        Args:
            user (User): The user object to create.

        Returns:
            User: The created user with updated ID.

        Raises:
            UserAlreadyExistsError: If a user with the same email already exists.
        """
        logger.debug(f"Creating user with email: {user.email}")

        existing_user = self.session.exec(
            select(User).where(User.email == user.email)
        ).first()
        if existing_user:
            raise UserAlreadyExistsError(user.email)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        logger.info(f"User created successfully with id: {user.id}")
        return user

    def get_all(self, offset: int = 0, limit: int = 100) -> List[User]:
        """Retrieve all users with pagination.

        Args:
            offset (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to return. Defaults to 100.

        Returns:
            List[User]: List of users matching the pagination criteria.
        """
        logger.debug(f"Fetching users with offset: {offset} and limit: {limit}")
        users = self.session.exec(select(User).offset(offset).limit(limit)).all()
        return users

    def get_by_id(self, user_id: int) -> User:
        """Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The requested user.

        Raises:
            UserNotFoundError: If no user exists with the given ID.
        """
        logger.debug(f"Fetching user with id: {user_id}")
        user = self.session.get(User, user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

    def update(self, user_id: int, user_data: dict) -> User:
        """Update a user's information.

        Args:
            user_id (int): The ID of the user to update.
            user_data (dict): Dictionary containing the fields to update.

        Returns:
            User: The updated user.

        Raises:
            UserNotFoundError: If no user exists with the given ID.
        """
        logger.debug(f"Updating user with id: {user_id}")
        db_user = self.get_by_id(user_id)
        
        for key, value in user_data.items():
            if hasattr(db_user, key) and value is not None:
                setattr(db_user, key, value)

        self.session.commit()
        self.session.refresh(db_user)
        logger.info(f"User {user_id} updated successfully")
        return db_user

    def delete(self, user_id: int) -> None:
        """Delete a user from the database.

        Args:
            user_id (int): The ID of the user to delete.

        Raises:
            UserNotFoundError: If no user exists with the given ID.
        """
        logger.debug(f"Deleting user with id: {user_id}")
        user = self.get_by_id(user_id)
        self.session.delete(user)
        self.session.commit()
        logger.info(f"User {user_id} deleted successfully") 