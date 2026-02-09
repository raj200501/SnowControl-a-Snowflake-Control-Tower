from __future__ import annotations

from dataclasses import dataclass
import importlib
import importlib.util
from typing import Protocol


class SnowflakeClient(Protocol):
    def fetch_state(self) -> dict:
        ...

    def execute_sql(self, sql: str) -> None:
        ...


@dataclass
class MockSnowflakeClient:
    state: dict

    def fetch_state(self) -> dict:
        return self.state

    def execute_sql(self, sql: str) -> None:
        return None


class RealSnowflakeClient:
    def __init__(self, **kwargs: str) -> None:
        if importlib.util.find_spec("snowflake.connector") is None:
            raise RuntimeError(
                "snowflake-connector-python is required for RealSnowflakeClient"
            )
        snowflake_connector = importlib.import_module("snowflake.connector")
        self._conn = snowflake_connector.connect(**kwargs)

    def fetch_state(self) -> dict:
        return {}

    def execute_sql(self, sql: str) -> None:
        with self._conn.cursor() as cursor:
            cursor.execute(sql)
