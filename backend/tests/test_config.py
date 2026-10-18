import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_secretos_no_aparecen_en_repr():
    s = Settings(env="test", admin_api_key="super-secreto", _env_file=None)
    assert "super-secreto" not in repr(s)
    assert "super-secreto" not in str(s.model_dump())


def test_produccion_exige_secretos():
    with pytest.raises(ValidationError):
        Settings(env="production", _env_file=None)


def test_produccion_exige_ssl_en_base_de_datos():
    with pytest.raises(ValidationError):
        Settings(
            env="production",
            admin_api_key="x",
            database_url="postgresql+psycopg://u:p@host/db",
            _env_file=None,
        )
    ok = Settings(
        env="production",
        admin_api_key="x",
        database_url="postgresql+psycopg://u:p@host/db?sslmode=require",
        _env_file=None,
    )
    assert ok.docs_active is False


def test_cors_rechaza_comodin():
    with pytest.raises(ValidationError):
        Settings(env="test", cors_origins="*", _env_file=None)
