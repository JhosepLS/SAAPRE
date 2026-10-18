"""Medidas de seguridad de la API (RNF-09).

- Cabeceras de seguridad en todas las respuestas.
- Autenticación por clave en los endpoints administrativos.
- Límite de peticiones por cliente (ventana deslizante en memoria).
- Medición del tiempo de respuesta (RQ-06).
"""

import hmac
import logging
import time
from collections import defaultdict, deque

from fastapi import Depends, Header, HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import Settings

logger = logging.getLogger("saapre.security")

DOCS_PATHS = {"/docs", "/redoc", "/openapi.json", "/docs/oauth2-redirect"}
ADMIN_PREFIX = "/api/v1/admin"


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Agrega cabeceras que reducen la superficie de ataque del navegador."""

    def __init__(self, app, hsts: bool = False):
        super().__init__(app)
        self.hsts = hsts

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cache-Control"] = "no-store"
        if request.url.path not in DOCS_PATHS:
            # La API solo devuelve JSON: no necesita cargar ningún recurso.
            response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        if self.hsts:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Registra el tiempo de cada consulta; sirve para verificar RQ-06 (≤ 2 s)."""

    SLOW_MS = 2000

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.1f}"
        if elapsed_ms > self.SLOW_MS:
            logger.warning("Consulta lenta: %s %s (%.0f ms)", request.method, request.url.path, elapsed_ms)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Límite de peticiones por IP en una ventana de 60 s.

    Es un limitador en memoria: suficiente para una instancia. Si el backend se
    escala a varias réplicas, debe reemplazarse por uno compartido (por ejemplo, Redis).
    """

    WINDOW_SECONDS = 60.0

    def __init__(self, app, per_minute: int, admin_per_minute: int, clock=time.monotonic):
        super().__init__(app)
        self.per_minute = per_minute
        self.admin_per_minute = admin_per_minute
        self.clock = clock
        self._hits: dict[tuple[str, bool], deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client = request.client.host if request.client else "unknown"
        is_admin = request.url.path.startswith(ADMIN_PREFIX)
        limit = self.admin_per_minute if is_admin else self.per_minute
        now = self.clock()
        hits = self._hits[(client, is_admin)]
        while hits and now - hits[0] >= self.WINDOW_SECONDS:
            hits.popleft()
        if len(hits) >= limit:
            retry_after = max(1, int(self.WINDOW_SECONDS - (now - hits[0])))
            return JSONResponse(
                {"detail": "Demasiadas peticiones. Intenta de nuevo más tarde."},
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={"Retry-After": str(retry_after)},
            )
        hits.append(now)
        return await call_next(request)


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def require_admin(
    settings: Settings = Depends(get_settings),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    """Exige la clave administrativa; la comparación es de tiempo constante."""
    expected = settings.admin_api_key
    valid = (
        expected is not None
        and x_api_key is not None
        and hmac.compare_digest(x_api_key.encode(), expected.get_secret_value().encode())
    )
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
