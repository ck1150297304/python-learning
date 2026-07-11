from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    service: str


class GitHubUserResponse(BaseModel):
    username: str
    name: str | None
    public_repos: int
    repo_level: str


class ErrorResponse(BaseModel):
    code: str
    message: str


class ApiError(Exception):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)