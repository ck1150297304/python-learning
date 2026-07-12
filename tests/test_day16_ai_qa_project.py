import pytest
from fastapi.testclient import TestClient

from day16_ai_qa_project.main import app
from day16_ai_qa_project.services import (
    LLMUnavailableError,
    get_llm_service,
)


client = TestClient(app)


class FakeLLMService:
    model = "fake-model"

    def ask(self, question: str) -> str:
        return f"Mock answer for: {question}"


class UnavailableLLMService:
    model = "fake-model"

    def ask(self, question: str) -> str:
        raise LLMUnavailableError("Mock LLM service unavailable")


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    app.dependency_overrides.clear()

    yield

    app.dependency_overrides.clear()


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_question_success() -> None:
    app.dependency_overrides[get_llm_service] = (
        lambda: FakeLLMService()
    )

    response = client.post(
        "/ai/ask",
        json={"question": "What is FastAPI?"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Mock answer for: What is FastAPI?",
        "model": "fake-model",
    }


def test_ask_question_rejects_empty_question() -> None:
    response = client.post(
        "/ai/ask",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_ask_question_returns_503_when_llm_is_unavailable() -> None:
    app.dependency_overrides[get_llm_service] = (
        lambda: UnavailableLLMService()
    )

    response = client.post(
        "/ai/ask",
        json={"question": "What is FastAPI?"},
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Mock LLM service unavailable"
    }