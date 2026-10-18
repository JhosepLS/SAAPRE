"""Guardado y carga segura de modelos serializados (RF-06, RNF-03).

joblib usa pickle, que puede ejecutar código al cargar un archivo manipulado.
Por eso cada artefacto se guarda con su hash SHA-256 y solo se carga si:
  1) está dentro del directorio de modelos (sin salir con «..»), y
  2) su hash coincide con el registrado al guardarlo.
"""

import hashlib
from pathlib import Path
from typing import Any

import joblib


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _resolve_inside(models_dir: Path, name: str) -> Path:
    base = models_dir.resolve()
    target = (base / name).resolve()
    if base != target and base not in target.parents:
        raise ValueError("Ruta de artefacto fuera del directorio de modelos.")
    return target


def save_model(model: Any, models_dir: Path, name: str) -> tuple[Path, str]:
    target = _resolve_inside(models_dir, name)
    target.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, target)
    digest = _sha256(target)
    target.with_name(target.name + ".sha256").write_text(digest)
    return target, digest


def load_model(models_dir: Path, name: str) -> Any:
    target = _resolve_inside(models_dir, name)
    sidecar = target.with_name(target.name + ".sha256")
    if not target.is_file() or not sidecar.is_file():
        raise FileNotFoundError("Artefacto o suma de verificación inexistente.")
    if _sha256(target) != sidecar.read_text().strip():
        raise ValueError("La suma de verificación del artefacto no coincide; no se carga.")
    return joblib.load(target)
