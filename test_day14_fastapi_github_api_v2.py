from typing import Any

from fastapi.testclient import TestClient

from day14_fastapi_github_api_v2 import app, get_github_fetcher


def fake_fetch_github_user(username: str) -> dict[str, Any]:
    return {
        "id": 1,
        "login": username,
        "name": "Test User",
        "bio": "This is a fake GitHub user for testing.",
        "public_repos": 12,
        "followers": 100,
        "following": 8,
        "html_url": f"https://github.com/{username}",
        "type": "User",
        "created_at": "2020-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
    }


def test_get_github_user_success() -> None:
    app.dependency_overrides[get_github_fetcher] = lambda: fake_fetch_github_user

    client = TestClient(app)
    response = client.get("/github/users/octocat")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "GitHub user fetched successfully."
    assert body["data"]["username"] == "octocat"
    assert body["data"]["public_repos"] == 12
    assert body["data"]["has_many_public_repos"] is True
    assert body["data"]["raw"] is None

    app.dependency_overrides.clear()


def test_get_github_user_with_include_raw() -> None:
    app.dependency_overrides[get_github_fetcher] = lambda: fake_fetch_github_user

    client = TestClient(app)
    response = client.get("/github/users/octocat?include_raw=true")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["raw"]["id"] == 1
    assert body["data"]["raw"]["type"] == "User"

    app.dependency_overrides.clear()


def test_get_github_user_with_custom_repo_threshold() -> None:
    app.dependency_overrides[get_github_fetcher] = lambda: fake_fetch_github_user

    client = TestClient(app)
    response = client.get("/github/users/octocat?repo_level_threshold=20")

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["public_repos"] == 12
    assert body["data"]["has_many_public_repos"] is False

    app.dependency_overrides.clear()


def test_get_github_user_validation_error() -> None:
    client = TestClient(app)
    response = client.get("/github/users/octocat?repo_level_threshold=-1")

    assert response.status_code == 422