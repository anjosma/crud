import logging
from typing import List
from sqlmodel import Session, select

from app.models.user import User
from app.exceptions import UserNotFoundError, UserAlreadyExistsError

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
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
        logger.debug(f"Fetching users with offset: {offset} and limit: {limit}")
        users = self.session.exec(select(User).offset(offset).limit(limit)).all()
        return users

    def get_by_id(self, user_id: int) -> User:
        logger.debug(f"Fetching user with id: {user_id}")
        user = self.session.get(User, user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

    def update(self, user_id: int, user_data: dict) -> User:
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
        logger.debug(f"Deleting user with id: {user_id}")
        user = self.get_by_id(user_id)
        self.session.delete(user)
        self.session.commit()
        logger.info(f"User {user_id} deleted successfully") 