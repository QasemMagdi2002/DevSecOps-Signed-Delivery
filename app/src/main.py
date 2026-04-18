import hashlib
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src import __version__
from src.config import get_settings

settings = get_settings()

app = FastAPI(
    title="DevSecOps Demo Service",
    version=__version__,
    description="A small FastAPI service used to demonstrate a production-style DevSecOps pipeline.",
)


@app.get("/", tags=["general"])
def root() -> dict:
    return {
        "service": settings.app_name,
        "environment": settings.app_env,
        "message": settings.app_message,
        "version": __version__,
    }


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}


@app.get("/ready", tags=["health"])
def readiness() -> dict:
    return {
        "status": "ready",
        "service": settings.app_name,
        "environment": settings.app_env,
    }


@app.get("/config", tags=["config"])
def config() -> dict:
    return {
        "app_name": settings.app_name,
        "app_env": settings.app_env,
        "app_message": settings.app_message,
        "log_level": settings.log_level,
        "workers": settings.workers,
    }


@app.get("/secret-check", tags=["security"])
def secret_check() -> JSONResponse:
    if not settings.app_secret:
        return JSONResponse(
            status_code=200,
            content={"secret_present": False},
        )

    masked_hash = hashlib.sha256(settings.app_secret.encode("utf-8")).hexdigest()[:12]

    return JSONResponse(
        status_code=200,
        content={
            "secret_present": True,
            "secret_fingerprint": masked_hash,
        },
    )


@app.get("/cpu", tags=["demo"])
def cpu_burn(iterations: int = 500_000) -> dict:
    if iterations < 1 or iterations > 10_000_000:
        return {
            "status": "rejected",
            "reason": "iterations must be between 1 and 10000000",
        }

    total = 0
    for i in range(iterations):
        total += i * i

    return {
        "status": "completed",
        "iterations": iterations,
        "result_sample": str(total)[:12],
    }