"""CU-02, CU-03 y CU-04: análisis, evolución por parche y recomendaciones (RF-07, RF-08, RF-12, RF-13)."""

from fastapi import APIRouter, Path, Query

from app.api.v1.common import not_implemented
from app.schemas.analysis import AnalysisOut, PatchMetricOut, RecommendationOut
from app.schemas.common import Game

router = APIRouter(prefix="/players/{player_id}", tags=["análisis"])

PlayerId = Path(ge=1)


@router.get("/analysis", response_model=AnalysisOut)
def get_analysis(player_id: int = PlayerId, game: Game = Query()) -> AnalysisOut:
    raise not_implemented("Análisis de rendimiento (CU-02)")


@router.get("/evolution", response_model=list[PatchMetricOut])
def get_evolution(
    player_id: int = PlayerId,
    from_patch: int = Query(ge=1),
    to_patch: int = Query(ge=1),
) -> list[PatchMetricOut]:
    raise not_implemented("Evolución por parche (CU-03)")


@router.get("/recommendations", response_model=list[RecommendationOut])
def get_recommendations(player_id: int = PlayerId) -> list[RecommendationOut]:
    raise not_implemented("Recomendaciones (CU-04)")
