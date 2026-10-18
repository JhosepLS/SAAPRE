from sklearn.ensemble import RandomForestClassifier

from app.ml.models.base import MLModel


class RandomForestModel(MLModel):
    algorithm = "Random Forest"

    def _build_estimator(self):
        return RandomForestClassifier(n_estimators=200, random_state=self.random_seed, n_jobs=-1)
