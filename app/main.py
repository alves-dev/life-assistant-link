import logging
import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import Response

from app.api.v1.zone import zone_event
from app.config.setting import setting
from app.core.middleware.error_handler import ResponseException

app = FastAPI(
    title="Assistant link",
    openapi_url="/openapi.json" if setting.SWAGGER_ENABLED else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=setting.LOG_LEVEL)


@app.exception_handler(ResponseException)
def response_error_handler(_: Request, exc: ResponseException) -> Response:
    """Turns any ResponseException into a JSON with the exception content"""
    return JSONResponse(status_code=exc.code, content=exc.content)


@app.exception_handler(Exception)
def generic_exception_handler(_: Request, _exc: Exception) -> Response:
    """Torna uma exceção qualquer em uma reposta de Internal Server Error"""

    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"},
    )


app.include_router(zone_event, prefix="/api/v1")


@app.get("/api/v1/")
def healthcheck() -> Response:
    return JSONResponse(
        status_code=200,
        content={"status": True},
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)