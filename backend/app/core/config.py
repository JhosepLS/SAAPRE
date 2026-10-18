"""Configuración del sistema (RNF-06, RNF-08).

Todos los secretos se leen de variables de entorno con prefijo SAAPRE_ o de un
archivo .env local que nunca se versiona. Los secretos se guardan como
SecretStr para que no aparezcan en logs ni en repr().
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="SAAPRE_", extra="ignore", case_sensitive=False)

    env: Literal["development", "test", "production"] = "development"

    # Secretos: sin valores por defecto para evitar credenciales en el código.
    database_url: SecretStr | None = None
    riot_api_key: SecretStr | None = None
    faceit_api_key: SecretStr | None = None
    admin_api_key: SecretStr | None = None

    cors_origins: list[str] = ["http://localhost:5173"]
    rate_limit_per_minute: int = 60
    admin_rate_limit_per_minute: int = 10
    docs_enabled: bool | None = None  # None: activo salvo en producción

    models_dir: Path = Path("models")
    random_seed: int = 42

    # Límites de las APIs externas (RNF-02)
    riot_requests_per_second: float = 20.0
    faceit_requests_per_second: float = 5.0
    http_max_retries: int = 3

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value):
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        return value

    @field_validator("cors_origins")
    @classmethod
    def _no_wildcard(cls, value):
        if "*" in value:
            raise ValueError("CORS no admite '*'; indica los orígenes explícitos.")
        return value

    @model_validator(mode="after")
    def _production_requirements(self):
        if self.env == "production":
            missing = [name for name in ("database_url", "admin_api_key") if getattr(self, name) is None]
            if missing:
                raise ValueError(f"En producción son obligatorias: {', '.join(missing)}")
            if "sslmode=require" not in self.database_url.get_secret_value():
                raise ValueError("En producción la conexión a la base de datos exige sslmode=require.")
        return self

    @property
    def docs_active(self) -> bool:
        if self.docs_enabled is not None:
            return self.docs_enabled
        return self.env != "production"


@lru_cache
def get_default_settings() -> Settings:
    return Settings()
