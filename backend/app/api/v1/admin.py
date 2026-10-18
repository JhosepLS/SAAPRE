"""Endpoints administrativos: exigen autenticación (RNF-09). Cubren CU-06, CU-10 y CU-12."""

from fastapi import APIRouter, Depends

from app.api.v1.common import not_implemented
from app.core.security import require_admin
from app.schemas.analysis import AdminCollectRequest, AdminRetrainRequest

router = APIRouter(prefix="/admin", tags=["administración"], dependencies=[Depends(require_admin)])


@router.post("/collect", status_code=202)
def collect(payload: AdminCollectRequest) -> dict[str, str]:
    raise not_implemented("Recolección de partidas (CU-06)")


@router.post("/retrain", status_code=202)
def retrain(payload: AdminRetrainRequest) -> dict[str, str]:
    raise not_implemented("Reentrenamiento (CU-10)")
