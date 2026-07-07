from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from day12_github_client_v2 import (
    GitHubClientError,
    GitHubHTTPError,
    GitHubRateLimitError,
    GitHubUserNotFoundError,
    fetch_github_user,
    get_user_summary,
)


app = FastAPI(
    title="Day 13 GitHub User API",
    description="A local FastAPI wrapper around the Day 12 GitHub API client.",
    version="0.1.0",
)


class GitHubUserResponse(BaseModel):
    username: str
    name: str | None
    public_repos: int
    followers: int
    following: int
    profile_url: str


def pick_str(data: dict[str, Any], *keys: str, default: str = "") -> str:
    for key in keys:
        value = data.get(key)
        if value is not None:
            return str(value)

    return default


def pick_optional_str(data: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = data.get(key)
        if value is not None:
            return str(value)

    return None


def pick_int(data: dict[str, Any], *keys: str, default: int = 0) -> int:
    for key in keys:
        value = data.get(key)
        if value is not None:
            return int(value)

    return default


def build_github_user_response(
    username: str,
    summary: dict[str, Any],
) -> GitHubUserResponse:
    return GitHubUserResponse(
        username=pick_str(summary, "username", "login", default=username),
        name=pick_optional_str(summary, "name"),
        public_repos=pick_int(summary, "public_repos", "repos"),
        followers=pick_int(summary, "followers"),
        following=pick_int(summary, "following"),
        profile_url=pick_str(summary, "profile_url", "html_url"),
    )


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "Day 13 FastAPI GitHub API is running.",
        "docs": "Open http://127.0.0.1:8000/docs",
    }


@app.get(
    "/github/users/{username}",
    response_model=GitHubUserResponse,
)
def read_github_user(username: str) -> GitHubUserResponse:
    try:
        user_data = fetch_github_user(username)
        summary = get_user_summary(user_data)
        return build_github_user_response(username, summary)

    except GitHubUserNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except GitHubRateLimitError as error:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(error),
        ) from error

    except GitHubHTTPError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error

    except GitHubClientError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error