from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.responses import Response

router = APIRouter(prefix="/api/v1", tags=['Health'])


@router.get("/health")
def health_check() -> Response:
    return JSONResponse(
        status_code=200,
        content={"status": True},
    )
