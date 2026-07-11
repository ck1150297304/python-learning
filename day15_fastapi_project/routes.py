from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from day15_fastapi_project.models import (
    ErrorResponse,
    GitHubUserResponse,
    HealthResponse,
)
from day15_fastapi_project.services import get_github_user_profile

router = APIRouter()


def get_github_user_service() -> Callable[[str, int], GitHubUserResponse]:
    return get_github_user_profile


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="day15_fastapi_project",
    )


@router.get(
    "/github/users/{username}",
    response_model=GitHubUserResponse,
    responses={
        404: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def read_github_user(
    username: Annotated[str, Path(min_length=1)],
    repo_level_threshold: Annotated[int, Query(ge=0, le=1000)] = 50,
    service: Callable[[str, int], GitHubUserResponse] = Depends(
        get_github_user_service
    ),
) -> GitHubUserResponse:
    return service(username, repo_level_threshold)