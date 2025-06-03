import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    DeleteResponse,
    UserListResponse
)
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
) -> JSONResponse:
    """Create a new user"""
    logger.debug("Creating new user with data: %s", user_data.model_dump())
    user = User(**user_data.model_dump())
    created_user = user_repo.create(user)
    logger.info("User created successfully with id: %s", created_user.id)
    return JSONResponse(
        status_code=201,
        content=UserResponse(**created_user.model_dump()).model_dump()
    )

@router.get("/", response_model=UserListResponse)
def read_users(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> JSONResponse:
    """Get all users"""
    logger.debug("Fetching users with offset: %s, limit: %s", offset, limit)
    users = user_repo.get_all(offset=offset, limit=limit)
    logger.debug("Found %s users", len(users))
    return JSONResponse(
        content=UserListResponse(
            items=[UserResponse(**user.model_dump()) for user in users]
        ).model_dump()
    )

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> JSONResponse:
    """Get a specific user by ID"""
    logger.debug("Fetching user with id: %s", user_id)
    user = user_repo.get_by_id(user_id)
    return JSONResponse(
        content=UserResponse(**user.model_dump()).model_dump()
    )

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> JSONResponse:
    """Update a user"""
    logger.debug("Updating user %s with data: %s", user_id, user_data.model_dump())
    updated_user = user_repo.update(user_id, user_data.model_dump(exclude_unset=True))
    logger.info("User %s updated successfully", user_id)
    return JSONResponse(
        content=UserResponse(**updated_user.model_dump()).model_dump()
    )

@router.delete("/{user_id}", response_model=DeleteResponse)
def delete_user(
    user_id: int,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> JSONResponse:
    """Delete a user"""
    logger.debug("Deleting user with id: %s", user_id)
    user_repo.delete(user_id)
    logger.info("User %s deleted successfully", user_id)
    return JSONResponse(
        content=DeleteResponse(ok=True).model_dump()
    ) 