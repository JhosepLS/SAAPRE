"""Control de la tasa de peticiones hacia las APIs externas (RNF-02)."""

import time
from collections.abc import Callable


class TokenBucket:
    """Cubeta de fichas: permite ráfagas de hasta `capacity` y luego `rate` por segundo."""

    def __init__(
        self,
        rate_per_second: float,
        capacity: int | None = None,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ):
        if rate_per_second <= 0:
            raise ValueError("rate_per_second debe ser positivo")
        self.rate = rate_per_second
        self.capacity = capacity or max(1, int(rate_per_second))
        self._clock = clock
        self._sleep = sleep
        self._tokens = float(self.capacity)
        self._last = clock()

    def _refill(self) -> None:
        now = self._clock()
        self._tokens = min(self.capacity, self._tokens + (now - self._last) * self.rate)
        self._last = now

    def acquire(self) -> None:
        """Espera hasta disponer de una ficha."""
        self._refill()
        if self._tokens < 1:
            self._sleep((1 - self._tokens) / self.rate)
            self._refill()
        self._tokens -= 1
