import logging
from fastapi import FastAPI

from app.api.v1.task import router as task_router


def get_application() -> FastAPI:
    """Application factory so tests can spin up fresh instances."""

    # Configure root logger only once
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )

    app = FastAPI(
        title="Async Task API",
        version="1.0.0",
        description=(
            "Demo application showcasing async FastAPI endpoints backed by a "
            "synchronous *file-based* SQLite repository (cleared on shutdown) "
            "and organised using a clean hexagonal architecture."
        ),
    )

    # Routes
    app.include_router(task_router, prefix="/tasks", tags=["tasks"])

    return app


app = get_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 