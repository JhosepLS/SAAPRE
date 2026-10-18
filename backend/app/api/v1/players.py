"""CU-01 Vincular cuenta de jugador (RF-10)."""

from fastapi import APIRouter

from app.api.v1.common import not_implemented
from app.schemas.player import AccountLinkRequest, PlayerOut

router = APIRouter(prefix="/players", tags=["jugadores"])


@router.post("", response_model=PlayerOut, status_code=201)
def link_account(payload: AccountLinkRequest) -> PlayerOut:
    raise not_implemented("Vincular cuenta (CU-01)")
