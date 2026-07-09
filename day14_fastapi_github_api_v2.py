from typing import Annotated, Any, Callable

from fastapi import Depends, FastAPI, Path, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from day12_github_client_v2 import (
    GitHubClientError,
    GitHubHTTPError,
    GitHubRateLimitError,
    GitHubUserNotFoundError,
    fetch_github_user,
)


app = FastAPI(
    title="GitHub User API",
    description="A local FastAPI wrapper for GitHub user information.",
    version="0.2.0",
)


class GitHubUserData(BaseModel):
    username: str = Field(description="GitHub login username")
    name: str | None = Field(default=None, description="GitHub display name")
    bio: str | None = Field(default=None, description="GitHub user bio")
    public_repos: int = Field(description="Number of public repositories")
    followers: int = Field(description="Number of followers")
    following: int = Field(description="Number of following users")
    profile_url: str = Field(description="GitHub profile URL")
    has_many_public_repos: bool = Field(
        description="Whether public repos count reaches the configured threshold"
    )
    raw: dict[str, Any] | None = Field(
        default=None,
        description="Optional selected raw fields from GitHub API",
    )


class GitHubUserResponse(BaseModel):
    success: bool = Field(description="Whether the request succeeded")
    message: str = Field(description="Human-readable response message")
    data: GitHubUserData


class ErrorResponse(BaseModel):
    success: bool = Field(default=False, description="Whether the request succeeded")
    error_code: str = Field(description="Machine-readable error code")
    message: str = Field(description="Human-readable error message")


class ApiError(Exception):
    def __init__(self, status_code: int, error_code: str, message: str) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.message = message


@app.exception_handler(ApiError)
async def api_error_handler(_, exc: ApiError) -> JSONResponse:
    error_response = ErrorResponse(
        success=False,
        error_code=exc.error_code,
        message=exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
    )


def get_github_fetcher() -> Callable[[str], dict[str, Any]]:
    return fetch_github_user


def build_github_user_data(
    user: dict[str, Any],
    include_raw: bool,
    repo_level_threshold: int,
) -> GitHubUserData:
    public_repos = user.get("public_repos") or 0

    raw_data: dict[str, Any] | None = None
    if include_raw:
        raw_data = {
            "id": user.get("id"),
            "type": user.get("type"),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at"),
        }

    return GitHubUserData(
        username=user.get("login", ""),
        name=user.get("name"),
        bio=user.get("bio"),
        public_repos=public_repos,
        followers=user.get("followers") or 0,
        following=user.get("following") or 0,
        profile_url=user.get("html_url", ""),
        has_many_public_repos=public_repos >= repo_level_threshold,
        raw=raw_data,
    )


@app.get(
    "/github/users/{username}",
    response_model=GitHubUserResponse,
    responses={
        404: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def get_github_user(
    username: Annotated[
        str,
        Path(
            min_length=1,
            max_length=39,
            description="GitHub username",
        ),
    ],
    include_raw: Annotated[
        bool,
        Query(
            description="Whether to include selected raw GitHub fields",
        ),
    ] = False,
    repo_level_threshold: Annotated[
        int,
        Query(
            ge=0,
            le=1000,
            description="Threshold used to calculate has_many_public_repos",
        ),
    ] = 10,
    github_fetcher: Annotated[
        Callable[[str], dict[str, Any]],
        Depends(get_github_fetcher),
    ] = fetch_github_user,
) -> GitHubUserResponse:
    try:
        user = github_fetcher(username)
    except GitHubUserNotFoundError as exc:
        raise ApiError(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="GITHUB_USER_NOT_FOUND",
            message=str(exc),
        ) from exc
    except GitHubRateLimitError as exc:
        raise ApiError(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="GITHUB_RATE_LIMIT",
            message=str(exc),
        ) from exc
    except GitHubHTTPError as exc:
        raise ApiError(
            status_code=status.HTTP_502_BAD_GATEWAY,
            error_code="GITHUB_UPSTREAM_ERROR",
            message=str(exc),
        ) from exc
    except GitHubClientError as exc:
        raise ApiError(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="GITHUB_CLIENT_ERROR",
            message=str(exc),
        ) from exc

    data = build_github_user_data(
        user=user,
        include_raw=include_raw,
        repo_level_threshold=repo_level_threshold,
    )

    return GitHubUserResponse(
        success=True,
        message="GitHub user fetched successfully.",
        data=data,
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}