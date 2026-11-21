from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="서버 상태 확인")
async def check_health() -> HealthResponse:
    """Check that the API process responds; no DB or model checks are performed."""
    return HealthResponse()
