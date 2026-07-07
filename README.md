# python-learning

My Python and AI Application Engineering learning journey.

This repository records my daily learning progress as I transition from iOS development to AI Application Engineering.

本仓库用于记录我从 iOS 开发转向 AI 应用开发过程中的 Python 工程化学习、API 开发练习和后续 AI 应用项目实践。

---

## Goal / 学习目标

Build practical Python engineering skills for AI application development.

目标是逐步掌握 AI Application Engineer 所需的工程能力，包括 Python、FastAPI、API Client、LLM API、RAG、Agent Workflow 和部署基础。

---

## Current Focus / 当前重点

- Python engineering fundamentals
- Git and GitHub workflow
- Python modules and packages
- Type hints
- Virtual environments
- Third-party dependencies
- HTTP API requests
- API client design
- Environment variables and API key management
- FastAPI web API development

---

## Future Focus / 后续方向

- FastAPI project structure
- Request and response models
- Async programming
- LLM API integration
- RAG application development
- Agent workflow
- LangGraph
- MCP
- Docker
- Deployment basics

---

## Learning Progress / 学习进度

| Day | Topic | File |
| --- | --- | --- |
| Day 1 | Python basics: variables, data types, input/output | `day01.py` |
| Day 2 | Condition statements | `day02.py` |
| Day 3 | Loops | `day03.py` |
| Day 4 | Modules and package import practice | `day04.py` |
| Day 5 | Type hints practice | `day05.py` |
| Day 6 | Python modules and packages | `day06.py`, `utils/score_analyzer.py` |
| Day 7 | Student score analyzer practice | `day07.py` |
| Day 8 | Virtual environment and dependencies | `day08.py`, `requirements.txt` |
| Day 9 | API client function practice | `day09.py` |
| Day 10 | Python review and student score analysis | `day10_review.py` |
| Day 11 | GitHub API client with error handling | `day11_github_client.py` |
| Day 12 | GitHub API client engineering upgrade: headers, token, custom exceptions, CLI arguments | `day12_github_client_v2.py` |
| Day 13 | FastAPI GitHub user API endpoint | `day13_fastapi_github_api.py` |

---

## Day 13 Highlight / 阶段成果

On Day 13, I built a local FastAPI web API that wraps the GitHub API client from Day 12.

Day 13 完成了一个本地 FastAPI Web API 服务，将前一天实现的 GitHub API Client 封装为 HTTP 接口。

Implemented endpoint:

```http
GET /github/users/{username}
```

Key practices:

- Created a FastAPI application
- Defined path parameters
- Used Pydantic response model
- Reused existing GitHub API client logic
- Converted custom Python exceptions into HTTP status codes
- Handled GitHub API rate limit with `GITHUB_TOKEN`
- Tested the API with browser and Swagger UI

---

## Repository Structure / 仓库结构

```text
python-learning/
├── utils/
│   └── score_analyzer.py
├── day01.py
├── day02.py
├── day03.py
├── day04.py
├── day05.py
├── day06.py
├── day07.py
├── day08.py
├── day09.py
├── day10_review.py
├── day11_github_client.py
├── day12_github_client_v2.py
├── day13_fastapi_github_api.py
├── requirements.txt
└── README.md
```

---

## How to Run Day 13 / 如何运行 Day 13

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the FastAPI server:

```bash
python -m uvicorn day13_fastapi_github_api:app --reload
```

Open Swagger UI in browser:

```text
http://127.0.0.1:8000/docs
```

Example request:

```text
http://127.0.0.1:8000/github/users/torvalds
```

If GitHub API rate limit is triggered, configure a temporary GitHub token:

```bash
export GITHUB_TOKEN="your_github_token"
```

Do not commit any token or secret key to GitHub.

---

## Notes / 说明

This repository is focused on practical engineering practice rather than pure syntax learning.

本仓库重点不是单纯记录语法练习，而是逐步积累 AI 应用开发所需的工程能力。