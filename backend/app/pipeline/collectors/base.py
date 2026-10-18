"""DataCollector: clase abstracta con control de límite y reintentos (RNF-02)."""

import logging
import time
from abc import ABC, abstractmethod
from typing import Any

import httpx

from app.pipeline.rate_limiter import TokenBucket

logger = logging.getLogger("saapre.collectors")

RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class DataCollector(ABC):
    def __init__(self, api_key: str | None, requests_per_second: float, max_retries: int = 3):
        self._api_key = api_key  # nunca se registra en logs
        self._bucket = TokenBucket(requests_per_second)
        self._max_retries = max_retries

    @property
    @abstractmethod
    def base_url(self) -> str: ...

    @property
    @abstractmethod
    def auth_header(self) -> str: ...

    @abstractmethod
    def fetch_matches(self, external_player_id: str, limit: int = 20) -> list[dict[str, Any]]:
        """Devuelve las partidas del jugador con su versión de parche (RF-01 / RF-02)."""

    def _get_json(self, path: str, params: dict[str, Any] | None = None) -> Any:
        if not self._api_key:
            raise RuntimeError("Falta la clave de la API externa (variables SAAPRE_*_API_KEY).")
        url = f"{self.base_url}{path}"
        headers = {self.auth_header: self._api_key}
        for attempt in range(self._max_retries + 1):
            self._bucket.acquire()
            response = httpx.get(url, params=params, headers=headers, timeout=10.0)
            if response.status_code not in RETRYABLE_STATUS:
                response.raise_for_status()
                return response.json()
            wait = float(response.headers.get("Retry-After", 2**attempt))
            logger.warning("API externa respondió %s; reintento %s en %.1f s", response.status_code, attempt + 1, wait)
            time.sleep(wait)
        raise RuntimeError("La API externa no respondió tras los reintentos permitidos.")
