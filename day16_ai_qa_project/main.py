from fastapi import FastAPI

from .routes import router


app = FastAPI(
    title="AI Q&A API",
    description=(
        "A minimal AI question-answering API built with "
        "FastAPI and an OpenAI-compatible LLM service."
    ),
    version="0.1.0",
)

app.include_router(router)