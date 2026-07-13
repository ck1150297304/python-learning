import pytest
from fastapi.testclient import TestClient

from day16_ai_qa_project.main import app
from day16_ai_qa_project.services import (
    LLMConfigurationError,
    LLMRateLimitError,
    LLMServiceError,
    LLMUnavailableError,
    get_llm_service,
)


client = TestClient(app)


class FakeLLMService:
    model = "fake-model"

    def ask(self, question: str) -> str:
        return f"Mock answer for: {question}"


class ErrorLLMService:
    model = "fake-model"

    def __init__(self, error: LLMServiceError) -> None:
        self.error = error

    def ask(self, question: str) -> str:
        raise self.error


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


def test_ask_question_rejects_too_long_question() -> None:
    response = client.post(
        "/ai/ask",
        json={"question": "a" * 2001},
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("error", "expected_status"),
    [
        (
            LLMConfigurationError("Mock configuration error"),
            503,
        ),
        (
            LLMRateLimitError("Mock rate limit error"),
            429,
        ),
        (
            LLMUnavailableError("Mock LLM service unavailable"),
            503,
        ),
        (
            LLMServiceError("Mock upstream service error"),
            502,
        ),
    ],
)
def test_ask_question_maps_llm_errors_to_http_status(
    error: LLMServiceError,
    expected_status: int,
) -> None:
    app.dependency_overrides[get_llm_service] = (
        lambda: ErrorLLMService(error)
    )

    response = client.post(
        "/ai/ask",
        json={"question": "What is FastAPI?"},
    )

    assert response.status_code == expected_status
    assert response.json() == {"detail": str(error)}