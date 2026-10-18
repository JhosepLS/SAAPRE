from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from tests.conftest import ADMIN_KEY


def test_health_publico(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_cabeceras_de_seguridad(client):
    h = client.get("/api/v1/health").headers
    assert h["x-content-type-options"] == "nosniff"
    assert h["x-frame-options"] == "DENY"
    assert "default-src 'none'" in h["content-security-policy"]
    assert "x-process-time-ms" in h


def test_endpoints_admin_exigen_autenticacion(client):
    body = {"game": "LOL", "player_id": 1}
    assert client.post("/api/v1/admin/collect", json=body).status_code == 401
    assert client.post("/api/v1/admin/collect", json=body, headers={"X-API-Key": "incorrecta"}).status_code == 401
    assert client.post("/api/v1/admin/collect", json=body, headers={"X-API-Key": ADMIN_KEY}).status_code == 501


def test_admin_sin_clave_configurada_rechaza_todo():
    c = TestClient(create_app(Settings(env="test", _env_file=None)))
    r = c.post("/api/v1/admin/collect", json={"game": "LOL", "player_id": 1}, headers={"X-API-Key": ""})
    assert r.status_code == 401


def test_rechaza_campos_adicionales(client):
    r = client.post("/api/v1/players", json={"game": "LOL", "nickname": "jugador_demo", "is_admin": True})
    assert r.status_code == 422


def test_valida_entradas(client):
    assert client.post("/api/v1/players", json={"game": "DOTA", "nickname": "jugador_demo"}).status_code == 422
    xss = {"game": "LOL", "nickname": "<script>alert(1)</script>"}
    assert client.post("/api/v1/players", json=xss).status_code == 422
    assert client.post("/api/v1/players", json={"game": "LOL", "nickname": "ab"}).status_code == 422
    assert client.get("/api/v1/players/0/analysis?game=LOL").status_code == 422
    assert client.get("/api/v1/players/abc/analysis?game=LOL").status_code == 422


def test_entrada_valida_llega_a_la_logica(client):
    r = client.post("/api/v1/players", json={"game": "LOL", "nickname": "jugador_demo"})
    assert r.status_code == 501


def test_limite_de_peticiones():
    c = TestClient(create_app(Settings(env="test", rate_limit_per_minute=3, _env_file=None)))
    codes = [c.get("/api/v1/health").status_code for _ in range(5)]
    assert codes[:3] == [200, 200, 200] and codes[3:] == [429, 429]
    assert "retry-after" in c.get("/api/v1/health").headers


def test_cors_solo_origenes_permitidos(client):
    ok = client.get("/api/v1/health", headers={"Origin": "http://localhost:5173"})
    assert ok.headers.get("access-control-allow-origin") == "http://localhost:5173"
    bad = client.get("/api/v1/health", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in bad.headers


def test_docs_desactivadas_en_produccion():
    s = Settings(
        env="production",
        admin_api_key="x",
        database_url="postgresql+psycopg://u:p@h/db?sslmode=require",
        _env_file=None,
    )
    c = TestClient(create_app(s))
    assert c.get("/docs").status_code == 404
    assert c.get("/openapi.json").status_code == 404
