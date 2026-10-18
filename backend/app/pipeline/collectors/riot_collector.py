"""RiotCollector: partidas de League of Legends mediante la Riot Games API (RF-01)."""

from typing import Any

from app.pipeline.collectors.base import DataCollector


class RiotCollector(DataCollector):
    base_url = "https://americas.api.riotgames.com"
    auth_header = "X-Riot-Token"

    def fetch_matches(self, external_player_id: str, limit: int = 20) -> list[dict[str, Any]]:
        raise NotImplementedError("Pendiente: lista de partidas por puuid y detalle de cada una.")
