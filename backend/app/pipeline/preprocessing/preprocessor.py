"""Preprocessor: limpieza, normalización y variables predictoras (RF-03)."""


def compute_kda(kills: int, deaths: int, assists: int) -> float:
    """KDA = (kills + assists) / deaths; con 0 muertes se divide entre 1."""
    return round((kills + assists) / max(deaths, 1), 2)


class Preprocessor:
    def clean(self, raw_matches):
        raise NotImplementedError

    def normalize(self, frame):
        raise NotImplementedError

    def build_features(self, frame):
        raise NotImplementedError
