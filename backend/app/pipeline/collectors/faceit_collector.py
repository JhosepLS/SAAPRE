"""FaceitCollector: partidas de Counter-Strike 2 mediante la FACEIT API (RF-02)."""

from typing import Any

from app.pipeline.collectors.base import DataCollector


class FaceitCollector(DataCollector):
    base_url = "https://open.faceit.com/data/v4"
    auth_header = "Authorization"

    def fetch_matches(self, external_player_id: str, limit: int = 20) -> list[dict[str, Any]]:
        raise NotImplementedError("Pendiente: historial del jugador (game=cs2) y estadísticas por partida.")
