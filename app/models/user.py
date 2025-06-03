from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    """User model representing a user in the system.

    This model is used for both database operations and API responses.

    Attributes:
        id (int | None): The unique identifier for the user. Auto-generated if not provided.
        name (str): The user's full name. Indexed for faster searches.
        email (str): The user's email address. Must be unique and is indexed.
        is_active (bool): Flag indicating if the user account is active. Defaults to True.
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True) 