from app.ml.models.base import MLModel


class XGBoostModel(MLModel):
    algorithm = "XGBoost"

    def _build_estimator(self):
        from xgboost import XGBClassifier  # importación diferida: dependencia pesada

        return XGBClassifier(n_estimators=200, random_state=self.random_seed, eval_metric="logloss")
