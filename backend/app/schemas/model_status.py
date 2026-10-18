from pydantic import BaseModel

from app.schemas.common import Game


class ModelStatusOut(BaseModel):
    game: Game
    algorithm: str
    patch_version: str
    accuracy: float
    f1_score: float
    auc_roc: float
    drift_status: str  # monitoring | warning | drift_detected
