import logging
from typing import Annotated, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.dependencies import get_session

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)

@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> User:
    """Create a new user"""
    user = User(**user_data.model_dump())
    return user_repo.create(user)

@router.get("/", response_model=List[UserResponse])
def read_users(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> List[User]:
    """Get all users"""
    return user_repo.get_all(offset=offset, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> User:
    """Get a specific user by ID"""
    return user_repo.get_by_id(user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> User:
    """Update a user"""
    return user_repo.update(user_id, user_data.model_dump(exclude_unset=True))

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> dict:
    """Delete a user"""
    user_repo.delete(user_id)
    return {"ok": True} 