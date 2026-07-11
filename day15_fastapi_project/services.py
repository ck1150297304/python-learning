from day12_github_client_v2 import (
    GitHubClientError,
    GitHubHTTPError,
    GitHubRateLimitError,
    GitHubUserNotFoundError,
    fetch_github_user,
)

from day15_fastapi_project.models import ApiError, GitHubUserResponse


def get_repo_level(public_repos: int, repo_level_threshold: int) -> str:
    if public_repos >= repo_level_threshold:
        return "active"

    return "normal"


def get_github_user_profile(
    username: str,
    repo_level_threshold: int,
) -> GitHubUserResponse:
    try:
        user_data = fetch_github_user(username)
    except GitHubUserNotFoundError as exc:
        raise ApiError(
            status_code=404,
            code="GITHUB_USER_NOT_FOUND",
            message=f"GitHub user '{username}' was not found.",
        ) from exc
    except GitHubRateLimitError as exc:
        raise ApiError(
            status_code=429,
            code="GITHUB_RATE_LIMIT_EXCEEDED",
            message="GitHub API rate limit exceeded. Please try again later.",
        ) from exc
    except GitHubHTTPError as exc:
        raise ApiError(
            status_code=502,
            code="GITHUB_UPSTREAM_ERROR",
            message="GitHub API returned an unexpected HTTP error.",
        ) from exc
    except GitHubClientError as exc:
        raise ApiError(
            status_code=503,
            code="GITHUB_CLIENT_ERROR",
            message="Failed to fetch data from GitHub API.",
        ) from exc

    public_repos = int(user_data.get("public_repos", 0))

    return GitHubUserResponse(
        username=user_data.get("login", username),
        name=user_data.get("name"),
        public_repos=public_repos,
        repo_level=get_repo_level(
            public_repos=public_repos,
            repo_level_threshold=repo_level_threshold,
        ),
    )