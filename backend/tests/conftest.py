import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app

ADMIN_KEY = "clave-de-prueba-admin"


@pytest.fixture
def settings() -> Settings:
    return Settings(env="test", admin_api_key=ADMIN_KEY, rate_limit_per_minute=1000, _env_file=None)


@pytest.fixture
def client(settings) -> TestClient:
    return TestClient(create_app(settings))
