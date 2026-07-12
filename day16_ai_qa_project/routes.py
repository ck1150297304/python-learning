from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from .models import AskRequest, AskResponse, ErrorResponse
from .services import (
    LLMConfigurationError,
    LLMRateLimitError,
    LLMService,
    LLMServiceError,
    LLMUnavailableError,
    get_llm_service,
)


router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/ai/ask",
    response_model=AskResponse,
    responses={
        429: {
            "model": ErrorResponse,
            "description": "LLM 服务请求过于频繁",
        },
        502: {
            "model": ErrorResponse,
            "description": "LLM 上游服务返回异常",
        },
        503: {
            "model": ErrorResponse,
            "description": "LLM 服务配置错误或暂时不可用",
        },
    },
)
def ask_question(
    request: AskRequest,
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
) -> AskResponse:
    try:
        answer = llm_service.ask(request.question)
    except LLMConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except LLMRateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        ) from exc
    except LLMUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except LLMServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return AskResponse(
        answer=answer,
        model=llm_service.model,
    )