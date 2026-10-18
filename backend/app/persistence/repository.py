"""DataRepository: único punto de acceso a los datos (interfaz IDataAccess)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import ModelVersion, PatchVersion, Player


class DataRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_player(self, external_id: str, game: str) -> Player | None:
        stmt = select(Player).where(Player.external_id == external_id, Player.game == game)
        return self.session.scalars(stmt).first()

    def add_player(self, player: Player) -> Player:
        self.session.add(player)
        self.session.flush()
        return player

    def get_active_model(self, game: str) -> ModelVersion | None:
        stmt = (
            select(ModelVersion)
            .join(PatchVersion, ModelVersion.patch_id == PatchVersion.patch_id)
            .where(PatchVersion.game == game, ModelVersion.is_active.is_(True))
            .order_by(ModelVersion.trained_at.desc())
        )
        return self.session.scalars(stmt).first()

    # Pendientes (se implementan junto con el pipeline y el motor de predicción)
    def save_matches(self, matches) -> None:
        raise NotImplementedError

    def get_matches_by_patch(self, player_id: int, patch_id: int):
        raise NotImplementedError

    def save_prediction(self, prediction) -> None:
        raise NotImplementedError

    def save_drift_event(self, event) -> None:
        raise NotImplementedError
