from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.dependencies import db
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("", response_model=HealthResponse)
async def health_check() -> JSONResponse:
    """Basic health check endpoint that returns the status of the API"""
    return JSONResponse(
        content=HealthResponse(status="healthy").model_dump()
    )

@router.get("/readiness", response_model=ReadinessResponse)
async def readiness_check(session: Session = Depends(db.get_session)) -> JSONResponse:
    """Readiness check endpoint that verifies database connectivity"""
    try:
        session.exec(select(1))
        return JSONResponse(
            status_code=200,
            content=ReadinessResponse(
                status="ready",
                database="connected"
            ).model_dump()
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content=ReadinessResponse(
                status="not ready",
                database="disconnected",
                error=str(e)
            ).model_dump()
        ) 