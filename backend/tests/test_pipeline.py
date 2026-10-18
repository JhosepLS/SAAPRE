import httpx
import pytest

from app.pipeline.collectors.base import DataCollector
from app.pipeline.rate_limiter import TokenBucket


class FakeClock:
    def __init__(self):
        self.t = 0.0
        self.slept = []

    def now(self):
        return self.t

    def sleep(self, s):
        self.slept.append(s)
        self.t += s


def test_token_bucket_respeta_la_tasa():
    clock = FakeClock()
    bucket = TokenBucket(2, capacity=2, clock=clock.now, sleep=clock.sleep)
    for _ in range(2):
        bucket.acquire()
    assert clock.slept == []  # la ráfaga inicial no espera
    bucket.acquire()
    assert clock.slept == [pytest.approx(0.5)]  # 2 req/s: la tercera espera medio segundo


class Dummy(DataCollector):
    base_url = "https://api.example"
    auth_header = "X-Key"

    def fetch_matches(self, external_player_id, limit=20):
        return self._get_json("/m")


def test_colector_exige_clave():
    with pytest.raises(RuntimeError):
        Dummy(api_key=None, requests_per_second=100).fetch_matches("x")


def test_colector_reintenta_ante_429(monkeypatch):
    calls = {"n": 0}

    def fake_get(url, params=None, headers=None, timeout=None):
        calls["n"] += 1
        status = 429 if calls["n"] < 3 else 200
        return httpx.Response(
            status, json=[{"ok": True}], headers={"Retry-After": "0"}, request=httpx.Request("GET", url)
        )

    monkeypatch.setattr("app.pipeline.collectors.base.httpx.get", fake_get)
    monkeypatch.setattr("app.pipeline.collectors.base.time.sleep", lambda s: None)
    assert Dummy(api_key="k", requests_per_second=100).fetch_matches("x") == [{"ok": True}]
    assert calls["n"] == 3
