"""DriftMonitor: evalúa el error de las predicciones y activa el reentrenamiento (RF-05, RF-09)."""

from app.ml.drift.base import DriftDetector


class DriftMonitor:
    def __init__(self, detectors: list[DriftDetector]):
        self.detectors = detectors

    def register_outcome(self, predicted: int, actual: int) -> list[str]:
        """Registra un resultado real y devuelve los detectores que reportan drift."""
        error = int(predicted != actual)
        triggered = []
        for detector in self.detectors:
            detector.update(error)
            if detector.drift_detected:
                triggered.append(detector.name)
        return triggered

    def reset(self) -> None:
        for detector in self.detectors:
            detector.reset()
