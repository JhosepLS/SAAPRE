from pydantic import BaseModel, Field

from app.schemas.common import Game, StrictInput


class AnalysisOut(BaseModel):
    player_id: int
    patch_version: str
    kda: float
    winrate: float = Field(ge=0, le=1)
    performance_score: float = Field(ge=0, le=1)
    win_probability: float = Field(ge=0, le=1)


class PatchMetricOut(BaseModel):
    patch_version: str
    kda: float
    winrate: float
    performance_score: float


class RecommendationOut(BaseModel):
    rec_type: str
    description: str
    patch_version: str


class AdminCollectRequest(StrictInput):
    game: Game
    player_id: int = Field(ge=1)


class AdminRetrainRequest(StrictInput):
    game: Game
    patch_version: str = Field(min_length=1, max_length=20, pattern=r"^[0-9]+(\.[0-9]+)*$")
