"""Métricas de calidad del modelo y umbrales mínimos (RQ-01 a RQ-05 y RQ-07)."""

from collections.abc import Sequence

from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

QUALITY_THRESHOLDS = {"accuracy": 0.75, "f1": 0.75, "auc_roc": 0.80}  # RQ-01..03
MIN_DRIFT_DETECTION_RATE = 0.80  # RQ-04
MIN_RECOVERY_RATIO = 0.80  # RQ-05
MAX_FALSE_ALARM_RATE = 0.20  # RQ-07 (umbral propuesto)


def compute_metrics(y_true: Sequence[int], y_pred: Sequence[int], y_score: Sequence[float]) -> dict[str, float]:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred)),
        "auc_roc": float(roc_auc_score(y_true, y_score)),
    }


def meets_quality_thresholds(metrics: dict[str, float]) -> bool:
    return all(metrics[name] >= minimum for name, minimum in QUALITY_THRESHOLDS.items())


def drift_detection_rate(detected_patches: set[str], documented_patches: set[str]) -> float:
    """Proporción de parches documentados en los que se detectó drift (RQ-04)."""
    if not documented_patches:
        raise ValueError("Se requiere al menos un parche documentado.")
    return len(detected_patches & documented_patches) / len(documented_patches)


def recovery_ratio(accuracy_before: float, accuracy_after: float) -> float:
    """Accuracy tras reentrenar dividida entre la previa al parche (RQ-05)."""
    if accuracy_before <= 0:
        raise ValueError("La accuracy previa debe ser positiva.")
    return accuracy_after / accuracy_before


def false_alarm_rate(alerts_without_patch: int, total_alerts: int) -> float:
    """Alertas sin cambio real de parche sobre el total de alertas (RQ-07)."""
    return 0.0 if total_alerts == 0 else alerts_without_patch / total_alerts
