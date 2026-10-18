"""Tipos y base común de los esquemas de la API (RNF-09).

Todos los esquemas de entrada prohíben campos adicionales, de modo que un cliente
no pueda enviar atributos que el servidor no espera (manipulación de campos).
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

Game = Literal["LOL", "CS2"]

# Sin caracteres de control ni «<» y «>»; el nombre se limita a 3-40 caracteres.
Nickname = Annotated[str, Field(min_length=3, max_length=40, pattern=r"^[^\x00-\x1f\x7f<>]+$")]


class StrictInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Detail(BaseModel):
    detail: str
