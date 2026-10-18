"""MLModel: contrato común de los modelos de clasificación (RF-04)."""

from abc import ABC, abstractmethod
from typing import Any

from app.ml.evaluation import compute_metrics


class MLModel(ABC):
    algorithm: str

    def __init__(self, random_seed: int = 42):
        self.random_seed = random_seed
        self._estimator: Any = self._build_estimator()

    @abstractmethod
    def _build_estimator(self) -> Any: ...

    def train(self, X, y) -> None:
        self._estimator.fit(X, y)

    def predict_proba(self, X):
        return self._estimator.predict_proba(X)[:, 1]

    def predict(self, X):
        return self._estimator.predict(X)

    def evaluate(self, X, y) -> dict[str, float]:
        return compute_metrics(y, self.predict(X), self.predict_proba(X))
