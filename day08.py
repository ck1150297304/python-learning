import requests


def fetch_httpbin_data() -> dict:
    url: str = "https://httpbin.org/get"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data: dict = response.json()
    return data


def print_httpbin_report(data: dict) -> None:
    print("HTTP 请求结果：")
    print(f"请求地址：{data.get('url')}")
    print(f"请求来源 IP：{data.get('origin')}")

    headers: dict = data.get("headers", {})
    print(f"User-Agent：{headers.get('User-Agent')}")


def main() -> None:
    httpbin_data: dict = fetch_httpbin_data()
    print_httpbin_report(httpbin_data)


if __name__ == "__main__":
    main()