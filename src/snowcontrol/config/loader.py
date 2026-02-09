from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from snowcontrol.config.schema import DesiredConfig


class ConfigError(RuntimeError):
    pass


def load_yaml(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except FileNotFoundError as exc:
        raise ConfigError(f"Config file not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"Expected a mapping at top-level in {path}")
    return data


def load_config(path: Path) -> DesiredConfig:
    payload = load_yaml(path)
    try:
        return DesiredConfig.model_validate(payload)
    except ValidationError as exc:
        raise ConfigError(str(exc)) from exc
