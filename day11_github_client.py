from typing import Any

import requests


def build_github_user_url(username: str) -> str:
    return f"https://api.github.com/users/{username}"


def fetch_github_user(username: str) -> dict[str, Any] | None:
    url = build_github_user_url(username)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return data
    except requests.HTTPError as error:
        status_code = error.response.status_code if error.response is not None else "未知"

        if status_code == 403:
            print("请求失败：GitHub API 访问频率受限，请稍后重试，或换网络再试。")
        elif status_code == 404:
            print(f"请求失败：没有找到 GitHub 用户 {username}")
        else:
            print(f"请求 GitHub 用户信息失败，状态码：{status_code}")

        return None
    except requests.RequestException as error:
        print(f"请求 GitHub 用户信息失败：{error}")
        return None
    except ValueError as error:
        print(f"解析 JSON 数据失败：{error}")
        return None


def get_user_summary(user_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "login": user_data.get("login", "未知"),
        "name": user_data.get("name") or "未设置",
        "html_url": user_data.get("html_url", "未知"),
        "public_repos": user_data.get("public_repos", 0),
        "followers": user_data.get("followers", 0),
        "following": user_data.get("following", 0),
        "created_at": user_data.get("created_at", "未知"),
    }


def print_github_user_info(user_data: dict[str, Any]) -> None:
    login = user_data.get("login", "未知")
    name = user_data.get("name") or "未设置"
    html_url = user_data.get("html_url", "未知")
    public_repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)
    following = user_data.get("following", 0)
    created_at = user_data.get("created_at", "未知")

    print("GitHub 用户信息")
    print("-" * 30)
    print(f"用户名：{login}")
    print(f"昵称：{name}")
    print(f"主页：{html_url}")
    print(f"公开仓库数：{public_repos}")
    print(f"粉丝数：{followers}")
    print(f"关注数：{following}")
    print(f"账号创建时间：{created_at}")


def main() -> None:
    username = input("请输入 GitHub 用户名：").strip()

    if not username:
        print("用户名不能为空")
        return

    user_data = fetch_github_user(username)

    if user_data is None:
        return

    user_summary = get_user_summary(user_data)
    print_github_user_info(user_summary)


if __name__ == "__main__":
    main()