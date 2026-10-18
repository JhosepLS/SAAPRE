"""Recommendation: objeto de valor; se calcula en cada consulta y no se persiste (RF-12)."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Recommendation:
    rec_type: str
    description: str
    patch_id: int

    def to_dict(self) -> dict:
        return asdict(self)


def build_recommendations(prediction, recent_metrics) -> list[Recommendation]:
    raise NotImplementedError
