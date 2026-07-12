from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
        description="用户希望询问 AI 的问题",
        examples=["请用简单的话解释 FastAPI 的依赖注入"],
    )


class AskResponse(BaseModel):
    answer: str
    model: str


class ErrorResponse(BaseModel):
    detail: str