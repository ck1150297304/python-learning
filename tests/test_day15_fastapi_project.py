import pytest
from fastapi.testclient import TestClient

from day15_fastapi_project.main import app
from day15_fastapi_project.models import ApiError, GitHubUserResponse
from day15_fastapi_project.routes import get_github_user_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_dependency_overrides() -> None:
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "day15_fastapi_project",
    }


def test_read_github_user_success() -> None:
    def fake_service(
        username: str,
        repo_level_threshold: int,
    ) -> GitHubUserResponse:
        return GitHubUserResponse(
            username=username,
            name="Test User",
            public_repos=100,
            repo_level="active",
        )

    app.dependency_overrides[get_github_user_service] = lambda: fake_service

    response = client.get("/github/users/octocat?repo_level_threshold=50")

    assert response.status_code == 200
    assert response.json() == {
        "username": "octocat",
        "name": "Test User",
        "public_repos": 100,
        "repo_level": "active",
    }


def test_read_github_user_query_validation_error() -> None:
    response = client.get("/github/users/octocat?repo_level_threshold=-1")

    assert response.status_code == 422


def test_read_github_user_not_found_error() -> None:
    def fake_service(
        username: str,
        repo_level_threshold: int,
    ) -> GitHubUserResponse:
        raise ApiError(
            status_code=404,
            code="GITHUB_USER_NOT_FOUND",
            message=f"GitHub user '{username}' was not found.",
        )

    app.dependency_overrides[get_github_user_service] = lambda: fake_service

    response = client.get("/github/users/not-exist-user?repo_level_threshold=50")

    assert response.status_code == 404
    assert response.json() == {
        "code": "GITHUB_USER_NOT_FOUND",
        "message": "GitHub user 'not-exist-user' was not found.",
    }