from pathlib import Path

import pytest

from snowcontrol.config.loader import ConfigError, load_config


def test_load_example_config() -> None:
    config_path = Path("examples/acme_account/desired.yaml")
    config = load_config(config_path)
    assert config.account_name == "ACME"
    assert len(config.warehouses) == 2
    assert config.warehouses[0].name == "WH_INGEST"


def test_invalid_config(tmp_path: Path) -> None:
    bad_path = tmp_path / "bad.yaml"
    bad_path.write_text("- just a list", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config(bad_path)
