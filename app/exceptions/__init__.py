from fastapi import HTTPException

class UserException(HTTPException):
    """Base exception class for user-related errors.

    Args:
        status_code (int): HTTP status code for the error.
        detail (str): Detailed error message.
    """
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class UserNotFoundError(UserException):
    """Exception raised when a requested user is not found.

    Args:
        user_id (int): ID of the user that was not found.
    """
    def __init__(self, user_id: int):
        super().__init__(status_code=404, detail=f"User with id {user_id} not found")

class UserAlreadyExistsError(UserException):
    """Exception raised when trying to create a user with an email that already exists.

    Args:
        email (str): Email address that caused the conflict.
    """
    def __init__(self, email: str):
        super().__init__(status_code=400, detail=f"User with email {email} already exists") 