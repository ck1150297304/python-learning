import os
from typing import Protocol

import openai
from openai import OpenAI


DEFAULT_MODEL = "gpt-4.1"

SYSTEM_PROMPT = """
你是一名专业、准确、简洁的 AI 助手。

回答要求：
1. 默认使用中文回答。
2. 优先直接回答用户的问题。
3. 不确定的信息需要明确说明不确定。
4. 技术问题尽量给出清晰、可执行的解释。
""".strip()


class LLMServiceError(Exception):
    """LLM 服务基础异常。"""


class LLMConfigurationError(LLMServiceError):
    """LLM 服务配置错误。"""


class LLMRateLimitError(LLMServiceError):
    """LLM 服务触发限流。"""


class LLMUnavailableError(LLMServiceError):
    """LLM 服务暂时不可用。"""


class LLMService(Protocol):
    model: str

    def ask(self, question: str) -> str:
        """向 LLM 提问并返回回答。"""


class OpenAILLMService:
    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
        self.base_url = os.getenv("OPENAI_BASE_URL")

    def ask(self, question: str) -> str:
        if not self.api_key:
            raise LLMConfigurationError(
                "OPENAI_API_KEY environment variable is not configured"
            )

        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=30.0,
            max_retries=1,
        )

        try:
            response = client.responses.create(
                model=self.model,
                instructions=SYSTEM_PROMPT,
                input=question,
                max_output_tokens=600,
            )
        except openai.AuthenticationError as exc:
            raise LLMConfigurationError(
                "OpenAI API key is invalid or unavailable"
            ) from exc
        except openai.RateLimitError as exc:
            raise LLMRateLimitError(
                "OpenAI API rate limit exceeded"
            ) from exc
        except (
            openai.APITimeoutError,
            openai.APIConnectionError,
        ) as exc:
            raise LLMUnavailableError(
                "Unable to connect to the OpenAI API"
            ) from exc
        except openai.APIStatusError as exc:
            raise LLMServiceError(
                f"OpenAI API request failed with status {exc.status_code}"
            ) from exc

        answer = response.output_text.strip()

        if not answer:
            raise LLMServiceError("OpenAI API returned an empty answer")

        return answer


def get_llm_service() -> LLMService:
    return OpenAILLMService()