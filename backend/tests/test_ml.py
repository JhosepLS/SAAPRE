import numpy as np
import pytest

from app.ml.artifacts import load_model, save_model
from app.ml.drift.adwin_detector import ADWINDetector
from app.ml.drift.ddm_detector import DDMDetector
from app.ml.evaluation import (
    drift_detection_rate,
    false_alarm_rate,
    meets_quality_thresholds,
    recovery_ratio,
)
from app.ml.models.logistic_regression import LogisticRegressionModel
from app.ml.models.random_forest import RandomForestModel
from app.pipeline.preprocessing.preprocessor import compute_kda
from app.services.drift_monitor import DriftMonitor


def dataset(seed=0, n=600):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 4))
    y = (X[:, 0] + 0.5 * X[:, 1] + rng.normal(scale=0.5, size=n) > 0).astype(int)
    return X, y


@pytest.mark.parametrize("cls", [RandomForestModel, LogisticRegressionModel])
def test_modelos_entrenan_y_cumplen_umbrales(cls):
    X, y = dataset()
    model = cls(random_seed=7)
    model.train(X[:400], y[:400])
    metrics = model.evaluate(X[400:], y[400:])
    assert meets_quality_thresholds(metrics)


def test_entrenamiento_reproducible():
    X, y = dataset()
    a, b = RandomForestModel(random_seed=1), RandomForestModel(random_seed=1)
    a.train(X, y)
    b.train(X, y)
    assert np.allclose(a.predict_proba(X), b.predict_proba(X))


def test_kda_del_escenario_ilustrativo():
    assert compute_kda(9, 3, 11) == 6.67
    assert compute_kda(5, 0, 2) == 7.0


@pytest.mark.parametrize("cls", [ADWINDetector, DDMDetector])
def test_detectores_reportan_drift_ante_cambio(cls):
    rng = np.random.default_rng(0)
    detector = cls()
    for _ in range(500):
        detector.update(int(rng.random() < 0.10))  # modelo estable: ~10 % de error
    assert not detector.drift_detected
    detected = False
    for _ in range(500):
        detector.update(int(rng.random() < 0.60))  # tras el parche: ~60 % de error
        detected = detected or detector.drift_detected
    assert detected


def test_monitor_registra_resultados():
    monitor = DriftMonitor([ADWINDetector(), DDMDetector()])
    rng = np.random.default_rng(1)
    triggered = []
    for i in range(1000):
        err = rng.random() < (0.10 if i < 500 else 0.70)
        triggered += monitor.register_outcome(predicted=int(err), actual=0)
    assert triggered


def test_metricas_de_calidad_rq():
    assert drift_detection_rate({"14.19", "14.20"}, {"14.19", "14.20", "14.21", "14.22", "14.23"}) == 0.4
    assert recovery_ratio(0.78, 0.76) == pytest.approx(0.974, abs=1e-3)
    assert false_alarm_rate(1, 10) == 0.1 and false_alarm_rate(0, 0) == 0.0


def test_artefacto_con_integridad(tmp_path):
    X, y = dataset()
    model = LogisticRegressionModel()
    model.train(X, y)
    path, digest = save_model(model, tmp_path, "lol/xgb_p15.joblib")
    assert len(digest) == 64
    assert load_model(tmp_path, "lol/xgb_p15.joblib").predict(X[:5]).shape == (5,)
    path.write_bytes(path.read_bytes() + b"manipulado")
    with pytest.raises(ValueError):
        load_model(tmp_path, "lol/xgb_p15.joblib")


def test_artefacto_no_sale_del_directorio(tmp_path):
    with pytest.raises(ValueError):
        load_model(tmp_path, "../../etc/passwd")
