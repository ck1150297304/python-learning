import requests
from typing import Any


def fetch_get_result(url: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def print_request_info(data: dict[str, Any]) -> None:
    print("请求 URL：")
    print(data["url"])

    print("\n请求参数：")
    print(data["args"])

    print("\n请求头中的 User-Agent：")
    print(data["headers"].get("user-agent"))


def get_request_url(data: dict[str, Any]) -> str:
    return data["url"]


def main() -> None:
    url = "https://postman-echo.com/get"

    params = {
        "name": "chuichui",
        "role": "ai_application_engineer",
    }

    try:
        data = fetch_get_result(url, params)
        print_request_info(data)

        request_url = get_request_url(data)
        print(f"\n从函数中获取到的请求 URL：{request_url}")
    except requests.RequestException as error:
        print(f"请求失败：{error}")


if __name__ == "__main__":
    main()