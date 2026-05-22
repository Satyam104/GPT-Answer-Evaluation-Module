from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.api.routes import router
from app.utils.helpers import setup_logging

setup_logging()

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=(
        "An AI-powered answer evaluation engine that uses GPT to assess candidate responses "
        "across correctness, depth, and clarity — returning structured JSON feedback."
    ),
    contact={
        "name": "API Support",
    },
    license_info={"name": "MIT"},
)

# ── Custom validation error handler ──────────────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    messages = [f"{e['loc'][-1]}: {e['msg']}" for e in errors]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "; ".join(messages), "error_type": "ValidationError"}
    )

# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(router, prefix="/api/v1", tags=["Evaluation"])

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "GPT Answer Evaluation API is running",
        "docs": "/docs",
        "version": settings.APP_VERSION
    }
