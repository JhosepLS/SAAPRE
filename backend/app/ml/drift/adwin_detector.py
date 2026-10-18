from river.drift import ADWIN

from app.ml.drift.base import DriftDetector


class ADWINDetector(DriftDetector):
    name = "ADWIN"

    def __init__(self, delta: float = 0.002):
        self.delta = delta
        self.reset()

    def update(self, error: int) -> None:
        self._detector.update(error)

    @property
    def drift_detected(self) -> bool:
        return bool(self._detector.drift_detected)

    def reset(self) -> None:
        self._detector = ADWIN(delta=self.delta)
