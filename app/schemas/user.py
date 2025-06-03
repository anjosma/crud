from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    is_active: Optional[bool] = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

class DeleteResponse(BaseModel):
    ok: bool

class UserListResponse(BaseModel):
    items: List[UserResponse]