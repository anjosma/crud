from fastapi import HTTPException

class UserException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class UserNotFoundError(UserException):
    def __init__(self, user_id: int):
        super().__init__(status_code=404, detail=f"User with id {user_id} not found")

class UserAlreadyExistsError(UserException):
    def __init__(self, email: str):
        super().__init__(status_code=400, detail=f"User with email {email} already exists") 