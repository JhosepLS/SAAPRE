from river.drift.binary import DDM

from app.ml.drift.base import DriftDetector


class DDMDetector(DriftDetector):
    name = "DDM"

    def __init__(self, warm_start: int = 30):
        self.warm_start = warm_start
        self.reset()

    def update(self, error: int) -> None:
        self._detector.update(bool(error))

    @property
    def drift_detected(self) -> bool:
        return bool(self._detector.drift_detected)

    def reset(self) -> None:
        self._detector = DDM(warm_start=self.warm_start)
