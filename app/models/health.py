from pydantic import BaseModel

class HealthResponse(BaseModel):
    """Response model for basic health check endpoint.

    This model represents the basic health status of the API.

    Attributes:
        status (str): The health status of the API. Usually "healthy".
    """
    status: str

class ReadinessResponse(BaseModel):
    """Response model for readiness check endpoint.

    This model represents the readiness status of the API and its dependencies.

    Attributes:
        status (str): The overall readiness status ("ready" or "not ready").
        database (str): The database connection status ("connected" or "disconnected").
        error (str | None): Error message if any component is not ready. None if all is well.
    """
    status: str
    database: str
    error: str | None = None 