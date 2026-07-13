# python-learning

My Python and AI Application Engineering learning journey.

This repository records my daily learning progress as I transition from iOS development to AI Application Engineering.

本仓库用于记录我从 iOS 开发转向 AI 应用开发过程中的 Python 工程化学习、API 开发练习和后续 AI 应用项目实践。

---

## Featured Project / 核心项目

### Local LLM Q&A API / 本地大模型 AI 问答 API

A structured and testable AI question-answering backend built with FastAPI, Ollama and Qwen3 through an OpenAI-compatible Responses API.

基于 FastAPI 开发的本地大模型问答后端，通过 OpenAI 兼容协议接入 Ollama 和 Qwen3，完成从 HTTP API、参数校验、依赖注入、LLM 服务封装、异常映射到自动化测试的完整工程闭环。

**Tech Stack / 技术栈**

`Python` · `FastAPI` · `Pydantic` · `OpenAI SDK` · `Ollama` · `Qwen3` · `Pytest`

**Core Capabilities / 核心能力**

* `GET /health` health check
* `POST /ai/ask` AI question-answering endpoint
* OpenAI-compatible Responses API integration
* Local LLM inference with Ollama and `qwen3:4b`
* Environment-based model configuration
* Route and LLM service decoupling with `Depends` and `Protocol`
* Structured mapping of LLM errors to HTTP status codes
* Isolated API testing with `dependency_overrides`
* Automated coverage for success, validation and upstream error scenarios
* 16 automated tests passing across the repository

**Architecture / 调用链路**

```text
Client
  ↓
FastAPI Route
  ↓
Pydantic Validation
  ↓
LLMService Protocol
  ↓
OpenAI Python SDK
  ↓
Ollama OpenAI-compatible API
  ↓
Qwen3 Local Model
```

**Error Handling / 异常处理**

| Scenario                   | HTTP Status |
| -------------------------- | ----------: |
| Invalid request parameters |       `422` |
| LLM rate limit             |       `429` |
| LLM configuration error    |       `503` |
| LLM service unavailable    |       `503` |
| Upstream LLM service error |       `502` |

**Testing / 自动化测试**

The real LLM service is replaced with fake implementations through FastAPI `dependency_overrides`. Automated tests therefore do not require Ollama, external network access, API keys or real model inference.

测试通过依赖覆盖注入 Fake LLM Service，在不启动 Ollama、不访问外部网络、不使用真实模型的情况下，验证接口成功路径、请求参数校验以及不同 LLM 异常到 HTTP 状态码的映射。

Project source:

* [`day16_ai_qa_project/`](./day16_ai_qa_project/)
* [`tests/test_day16_ai_qa_project.py`](./tests/test_day16_ai_qa_project.py)

Run the complete test suite:

```bash
python -m pytest -v
```

Current result:

```text
16 passed
```

---

## Goal / 学习目标

Build practical Python engineering skills for AI application development.

目标是逐步掌握 AI Application Engineer 所需的工程能力，包括 Python、FastAPI、API Client、LLM API、RAG、Agent Workflow 和部署基础。

---

## Current Focus / 当前重点

- FastAPI project structure
- Pydantic request and response models
- Dependency injection with FastAPI `Depends`
- Automated API testing with Pytest and TestClient
- External service isolation with `dependency_overrides`
- LLM API integration
- OpenAI-compatible API development
- Local LLM inference with Ollama and Qwen3
- Environment variables and model configuration
- Error handling for external AI services

---

## Future Focus / 后续方向

- Async programming
- Conversation context management
- Streaming LLM responses
- LangGraph
- RAG application development
- Agent workflow
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
| Day 14 | FastAPI query validation, optional response fields and automated tests | `day14_fastapi_github_api_v2.py`, `test_day14_fastapi_github_api_v2.py` |
| Day 15 | FastAPI project refactoring with routes, models, services and dependency injection | `day15_fastapi_project/`, `tests/test_day15_fastapi_project.py` |
| Day 16 | Local AI Q&A API with FastAPI, Ollama, Qwen3 and OpenAI-compatible Responses API | `day16_ai_qa_project/`, `tests/test_day16_ai_qa_project.py` |

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
├── day15_fastapi_project/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── services.py
├── day16_ai_qa_project/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── services.py
├── tests/
│   ├── test_day15_fastapi_project.py
│   └── test_day16_ai_qa_project.py
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
├── day14_fastapi_github_api_v2.py
├── test_day14_fastapi_github_api_v2.py
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

Open Swagger UI:

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

## How to Run Day 14 / 如何运行 Day 14

Day 14 extends the FastAPI GitHub user API with query parameter validation, optional response fields and automated tests.

Day 14 在 Day 13 的基础上增加了查询参数校验、可选响应字段和自动化测试。

Run the FastAPI server:

```bash
python -m uvicorn day14_fastapi_github_api_v2:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to test the GitHub user endpoint and its query parameters.

Run the Day 14 tests:

```bash
python -m pytest test_day14_fastapi_github_api_v2.py -v
```

---

## How to Run Day 15 / 如何运行 Day 15

Run the structured FastAPI GitHub API project:

```bash
python -m uvicorn day15_fastapi_project.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Run the Day 15 tests:

```bash
python -m pytest tests/test_day15_fastapi_project.py -v
```

---

## How to Run Day 16 / 如何运行 Day 16

Day 16 uses Ollama and the local `qwen3:4b` model through an OpenAI-compatible API.

Day 16 通过 OpenAI 兼容协议接入 Ollama，并使用本地 `qwen3:4b` 模型完成 AI 问答。

### 1. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Install and prepare the local model

Make sure Ollama is installed, then download the model:

```bash
ollama pull qwen3:4b
```

Confirm that the model is available:

```bash
ollama list
```

You can test the model directly:

```bash
ollama run qwen3:4b
```

### 3. Configure environment variables

```bash
export OPENAI_API_KEY="ollama"
export OPENAI_BASE_URL="http://127.0.0.1:11434/v1"
export OPENAI_MODEL="qwen3:4b"
export NO_PROXY="localhost,127.0.0.1"
export no_proxy="localhost,127.0.0.1"
```

`OPENAI_API_KEY="ollama"` is only a placeholder required by the OpenAI Python SDK when connecting to the local Ollama service. It is not a real secret key.

### 4. Run the FastAPI server

```bash
python -m uvicorn day16_ai_qa_project.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### 5. Send an AI question

```bash
curl -X POST \
  "http://127.0.0.1:8000/ai/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "请用简单的话解释 FastAPI 的依赖注入"
  }'
```

Example response:

```json
{
  "answer": "FastAPI 的依赖注入可以理解为……",
  "model": "qwen3:4b"
}
```

### 6. Run automated tests

Run all repository tests:

```bash
python -m pytest -v
```

Run only the Day 16 tests:

```bash
python -m pytest tests/test_day16_ai_qa_project.py -v
```

The tests replace the real LLM service with fake implementations through FastAPI `dependency_overrides`, so they do not require Ollama, external network access or real model inference.

---

## Notes / 说明

This repository focuses on practical AI application engineering rather than isolated Python syntax exercises.

The learning path gradually evolves from Python fundamentals and HTTP API clients to structured FastAPI services, dependency injection, automated testing and real LLM integration.

本仓库重点不是单纯记录 Python 语法练习，而是逐步构建 AI 应用开发所需的工程能力，包括：

- Python 工程基础
- HTTP API Client
- FastAPI Web API
- Pydantic 数据校验
- FastAPI 项目结构
- 依赖注入
- 第三方服务异常处理
- Pytest 自动化测试
- OpenAI 兼容协议
- Ollama 本地模型运行
- LLM 问答服务开发

No real API key or secret should be committed to this repository.

任何真实 API Key、Token 或其他敏感信息都不应提交到 GitHub。