from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    """Schema for creating a new user.

    This model is used for validating user creation requests.

    Attributes:
        name (str): The user's full name.
        email (EmailStr): The user's email address. Validated as a proper email format.
        is_active (Optional[bool]): Flag indicating if the user account is active. Defaults to True.
    """
    name: str
    email: EmailStr
    is_active: Optional[bool] = True

class UserUpdate(BaseModel):
    """Schema for updating an existing user.

    All fields are optional, allowing partial updates.

    Attributes:
        name (Optional[str]): The user's full name.
        email (Optional[EmailStr]): The user's email address.
        is_active (Optional[bool]): Flag indicating if the user account is active.
    """
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    """Schema for user responses in the API.

    This model defines how user data is returned in API responses.

    Attributes:
        id (int): The unique identifier for the user.
        name (str): The user's full name.
        email (str): The user's email address.
        is_active (bool): Flag indicating if the user account is active.
    """
    id: int
    name: str
    email: str
    is_active: bool

class DeleteResponse(BaseModel):
    """Schema for delete operation responses.

    Attributes:
        ok (bool): Indicates if the delete operation was successful.
    """
    ok: bool

class UserListResponse(BaseModel):
    """Schema for list of users response.

    Attributes:
        items (List[UserResponse]): List of user objects with their details.
    """
    items: List[UserResponse]