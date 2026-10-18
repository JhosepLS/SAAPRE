"""DriftDetector: contrato de los detectores de concept drift (RF-05)."""

from abc import ABC, abstractmethod


class DriftDetector(ABC):
    name: str

    @abstractmethod
    def update(self, error: int) -> None:
        """Recibe el error de una predicción: 1 si falló, 0 si acertó."""

    @property
    @abstractmethod
    def drift_detected(self) -> bool: ...

    @abstractmethod
    def reset(self) -> None: ...
