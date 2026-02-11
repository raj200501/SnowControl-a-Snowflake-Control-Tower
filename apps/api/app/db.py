from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path("data/demo/frostsight_demo.db")


def get_db_path() -> Path:
    return Path(os.getenv("FROSTSIGHT_DB_PATH", DEFAULT_DB_PATH))


def get_connection() -> sqlite3.Connection:
    path = get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection
