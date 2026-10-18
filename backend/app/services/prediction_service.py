"""PredictionService: genera predicciones con el modelo activo (RF-11)."""


class PredictionService:
    def predict(self, player_id: int):
        raise NotImplementedError

    def load_active_model(self) -> None:
        raise NotImplementedError
