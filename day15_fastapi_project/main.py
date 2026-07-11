from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from day15_fastapi_project.models import ApiError, ErrorResponse
from day15_fastapi_project.routes import router

app = FastAPI(
    title="Day 15 FastAPI GitHub API",
    version="1.0.0",
    description="A refactored FastAPI project for querying GitHub users.",
)

app.include_router(router)


@app.exception_handler(ApiError)
async def api_error_handler(
    request: Request,
    exc: ApiError,
) -> JSONResponse:
    error_response = ErrorResponse(
        code=exc.code,
        message=exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
    )