from sklearn.linear_model import LogisticRegression

from app.ml.models.base import MLModel


class LogisticRegressionModel(MLModel):
    algorithm = "Regresión Logística"

    def _build_estimator(self):
        return LogisticRegression(max_iter=1000, random_state=self.random_seed)
