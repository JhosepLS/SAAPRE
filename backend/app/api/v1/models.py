"""CU-05 Consultar estado del modelo y parche vigente (RF-09, RF-14)."""

from fastapi import APIRouter, Query

from app.api.v1.common import not_implemented
from app.schemas.common import Game
from app.schemas.model_status import ModelStatusOut

router = APIRouter(prefix="/models", tags=["modelos"])


@router.get("/status", response_model=ModelStatusOut)
def get_model_status(game: Game = Query()) -> ModelStatusOut:
    raise not_implemented("Estado del modelo (CU-05)")
