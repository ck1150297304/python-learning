import os
import sys
from typing import Any

import requests

GITHUB_API_BASE_URL = "https://api.github.com"
DEFAULT_TIMEOUT = 5


class GitHubClientError(Exception):
    """GitHub API 客户端基础异常。"""


class GitHubUserNotFoundError(GitHubClientError):
    """GitHub 用户不存在。"""


class GitHubRateLimitError(GitHubClientError):
    """GitHub API 请求频率受限。"""


class GitHubHTTPError(GitHubClientError):
    """GitHub API HTTP 请求错误。"""


def get_github_token() -> str | None:
    """
    从环境变量中读取 GitHub Token。

    注意：
    1. Token 不要写死在代码里。
    2. Token 不要提交到 GitHub。
    3. 如果没有配置 Token，也可以正常请求，只是更容易遇到 rate limit。
    """
    return os.getenv("GITHUB_TOKEN")


def build_github_user_url(username: str) -> str:
    username = username.strip()

    if not username:
        raise ValueError("GitHub username 不能为空")

    return f"{GITHUB_API_BASE_URL}/users/{username}"


def build_headers(token: str | None = None) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "python-learning-github-client",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def fetch_github_user(username: str, timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    url = build_github_user_url(username)
    token = get_github_token()
    headers = build_headers(token)

    try:
        response = requests.get(url, headers=headers, timeout=timeout)

        if response.status_code == 404:
            raise GitHubUserNotFoundError(f"GitHub 用户不存在：{username}")

        if response.status_code == 403:
            remaining = response.headers.get("X-RateLimit-Remaining")

            if remaining == "0":
                raise GitHubRateLimitError("GitHub API rate limit 已触发，请稍后再试或配置 GITHUB_TOKEN")

        response.raise_for_status()

        return response.json()

    except requests.Timeout as exc:
        raise GitHubClientError("请求 GitHub API 超时") from exc

    except requests.ConnectionError as exc:
        raise GitHubClientError("无法连接到 GitHub API，请检查网络") from exc

    except requests.HTTPError as exc:
        raise GitHubHTTPError(f"GitHub API HTTP 请求失败：{exc}") from exc

    except requests.RequestException as exc:
        raise GitHubClientError(f"GitHub API 请求异常：{exc}") from exc


def get_user_summary(user_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "login": user_data.get("login"),
        "name": user_data.get("name"),
        "bio": user_data.get("bio"),
        "public_repos": user_data.get("public_repos"),
        "followers": user_data.get("followers"),
        "following": user_data.get("following"),
        "html_url": user_data.get("html_url"),
    }


def print_github_user_info(summary: dict[str, Any]) -> None:
    print("GitHub 用户信息")
    print("-" * 30)
    print(f"用户名：{summary['login']}")
    print(f"昵称：{summary['name']}")
    print(f"简介：{summary['bio']}")
    print(f"公开仓库数：{summary['public_repos']}")
    print(f"粉丝数：{summary['followers']}")
    print(f"关注数：{summary['following']}")
    print(f"主页：{summary['html_url']}")


def get_username_from_args() -> str:
    if len(sys.argv) >= 2:
        return sys.argv[1]

    return input("请输入 GitHub 用户名：")


def main() -> None:
    try:
        username = get_username_from_args()
        user_data = fetch_github_user(username)
        summary = get_user_summary(user_data)
        print_github_user_info(summary)

    except ValueError as exc:
        print(f"输入错误：{exc}")

    except GitHubUserNotFoundError as exc:
        print(f"用户不存在：{exc}")

    except GitHubRateLimitError as exc:
        print(f"请求受限：{exc}")

    except GitHubClientError as exc:
        print(f"请求失败：{exc}")


if __name__ == "__main__":
    main()