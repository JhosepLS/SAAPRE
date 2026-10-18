from pydantic import BaseModel

from app.schemas.common import Game, Nickname, StrictInput


class AccountLinkRequest(StrictInput):
    """Entrada de CU-01: vincular la cuenta de un jugador (RF-10)."""

    game: Game
    nickname: Nickname


class PlayerOut(BaseModel):
    """Solo se devuelven los campos que el dashboard necesita."""

    player_id: int
    game: Game
    nickname: str
    region: str | None = None
