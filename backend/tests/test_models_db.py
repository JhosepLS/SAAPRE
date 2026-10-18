from datetime import date, datetime

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from app.domain.models import Base, ModelVersion, PatchVersion, Player
from app.persistence.repository import DataRepository


def make_session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    return engine, Session(engine)


def test_esquema_tiene_las_siete_tablas_del_er():
    engine, _ = make_session()
    assert set(inspect(engine).get_table_names()) == {
        "players",
        "patch_versions",
        "matches",
        "performance_metrics",
        "model_versions",
        "predictions",
        "drift_events",
    }


def test_resultado_pertenece_al_jugador():
    engine, _ = make_session()
    cols = {c["name"] for c in inspect(engine).get_columns("performance_metrics")}
    assert "win" in cols
    assert "result" not in {c["name"] for c in inspect(engine).get_columns("matches")}


def test_repositorio_consulta_parametrizada():
    _, s = make_session()
    repo = DataRepository(s)
    repo.add_player(Player(external_id="puuid-1", game="LOL", nickname="demo"))
    assert repo.get_player("puuid-1", "LOL").nickname == "demo"
    # Un intento de inyección se trata como un valor literal, no como SQL.
    assert repo.get_player("x' OR '1'='1", "LOL") is None


def test_modelo_activo_por_juego():
    _, s = make_session()
    patch = PatchVersion(game="LOL", version_tag="14.19", released_at=date(2024, 9, 25))
    s.add(patch)
    s.flush()
    s.add(ModelVersion(patch_id=patch.patch_id, algorithm="XGBoost", is_active=True, trained_at=datetime(2024, 9, 27)))
    s.flush()
    assert DataRepository(s).get_active_model("LOL").algorithm == "XGBoost"
    assert DataRepository(s).get_active_model("CS2") is None
