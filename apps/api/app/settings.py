from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    mode: str
    local_dev_token: str



def get_settings() -> Settings:
    return Settings(
        mode=os.getenv("FROSTSIGHT_MODE", "demo"),
        local_dev_token=os.getenv("LOCAL_DEV_TOKEN", "local-dev-token"),
    )
