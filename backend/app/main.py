"""Punto de entrada de la API (FastAPI)."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.v1.router import api_router
from app.core.config import Settings, get_default_settings
from app.core.security import (
    RateLimitMiddleware,
    RequestTimingMiddleware,
    SecurityHeadersMiddleware,
)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_default_settings()
    app = FastAPI(
        title="SAAPRE API",
        version=__version__,
        description="Análisis predictivo de rendimiento con detección de concept drift.",
        docs_url="/docs" if settings.docs_active else None,
        redoc_url="/redoc" if settings.docs_active else None,
        openapi_url="/openapi.json" if settings.docs_active else None,
    )
    app.state.settings = settings

    # El último middleware agregado es el más externo.
    app.add_middleware(
        RateLimitMiddleware,
        per_minute=settings.rate_limit_per_minute,
        admin_per_minute=settings.admin_rate_limit_per_minute,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "X-API-Key"],
        allow_credentials=False,
    )
    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware, hsts=settings.env == "production")

    app.include_router(api_router)
    return app


app = create_app()
