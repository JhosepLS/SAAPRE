"""Entidades de negocio y modelo de datos (Figuras 10 a 12 y Figura 14).

Cada clase corresponde a una tabla del diagrama entidad-relación. Solo se
guardan identificadores públicos y estadísticas de partidas (RNF-07).
"""

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"
    __table_args__ = (UniqueConstraint("external_id", "game", name="uq_players_external_game"),)

    player_id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String(100))
    game: Mapped[str] = mapped_column(String(10))
    nickname: Mapped[str] = mapped_column(String(60))
    region: Mapped[str | None] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    metrics: Mapped[list["PerformanceMetric"]] = relationship(back_populates="player")


class PatchVersion(Base):
    __tablename__ = "patch_versions"
    __table_args__ = (UniqueConstraint("game", "version_tag", name="uq_patch_game_tag"),)

    patch_id: Mapped[int] = mapped_column(primary_key=True)
    game: Mapped[str] = mapped_column(String(10))
    version_tag: Mapped[str] = mapped_column(String(20))
    released_at: Mapped[date] = mapped_column(Date)


class Match(Base):
    __tablename__ = "matches"

    match_id: Mapped[int] = mapped_column(primary_key=True)
    external_match_id: Mapped[str] = mapped_column(String(50), unique=True)
    game: Mapped[str] = mapped_column(String(10))
    played_at: Mapped[datetime] = mapped_column(DateTime)
    duration_sec: Mapped[int | None] = mapped_column(Integer)
    patch_id: Mapped[int] = mapped_column(ForeignKey("patch_versions.patch_id"))

    metrics: Mapped[list["PerformanceMetric"]] = relationship(back_populates="match")


class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"

    metric_id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.match_id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.player_id"))
    kills: Mapped[int | None] = mapped_column(Integer)
    deaths: Mapped[int | None] = mapped_column(Integer)
    assists: Mapped[int | None] = mapped_column(Integer)
    damage_dealt: Mapped[float | None] = mapped_column(Numeric(12, 2))
    kda: Mapped[float | None] = mapped_column(Numeric(6, 2))
    performance_score: Mapped[float | None] = mapped_column(Numeric(5, 4))
    win: Mapped[bool | None] = mapped_column(Boolean)

    match: Mapped[Match] = relationship(back_populates="metrics")
    player: Mapped[Player] = relationship(back_populates="metrics")


class ModelVersion(Base):
    __tablename__ = "model_versions"

    model_id: Mapped[int] = mapped_column(primary_key=True)
    # RNF-03: toda versión del modelo queda asociada al parche de sus datos.
    patch_id: Mapped[int] = mapped_column(ForeignKey("patch_versions.patch_id"))
    algorithm: Mapped[str] = mapped_column(String(30))
    accuracy: Mapped[float | None] = mapped_column(Numeric(5, 4))
    f1_score: Mapped[float | None] = mapped_column(Numeric(5, 4))
    auc_roc: Mapped[float | None] = mapped_column(Numeric(5, 4))
    trained_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    artifact_path: Mapped[str | None] = mapped_column(String(255))


class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.player_id"))
    match_id: Mapped[int | None] = mapped_column(ForeignKey("matches.match_id"))
    model_id: Mapped[int] = mapped_column(ForeignKey("model_versions.model_id"))
    win_probability: Mapped[float] = mapped_column(Numeric(5, 4))
    estimated_performance: Mapped[float | None] = mapped_column(Numeric(5, 4))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class DriftEvent(Base):
    __tablename__ = "drift_events"

    event_id: Mapped[int] = mapped_column(primary_key=True)
    patch_id: Mapped[int] = mapped_column(ForeignKey("patch_versions.patch_id"))
    model_id: Mapped[int] = mapped_column(ForeignKey("model_versions.model_id"))
    retrained_model_id: Mapped[int | None] = mapped_column(ForeignKey("model_versions.model_id"))
    detector: Mapped[str] = mapped_column(String(10))
    accuracy_before: Mapped[float | None] = mapped_column(Numeric(5, 4))
    accuracy_after: Mapped[float | None] = mapped_column(Numeric(5, 4))
    detected_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
