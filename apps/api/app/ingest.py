from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from app.db import get_connection

TABLES = {
    "warehouses": (
        """
        CREATE TABLE IF NOT EXISTS warehouses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            size TEXT,
            credit_per_hour REAL
        )
        """,
        """
        INSERT INTO warehouses (name, size, credit_per_hour)
        VALUES (:name, :size, :credit_per_hour)
        """,
    ),
    "warehouse_metering": (
        """
        CREATE TABLE IF NOT EXISTS warehouse_metering (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            warehouse_name TEXT,
            start_time TEXT,
            end_time TEXT,
            credits_used REAL
        )
        """,
        """
        INSERT INTO warehouse_metering (warehouse_name, start_time, end_time, credits_used)
        VALUES (:warehouse_name, :start_time, :end_time, :credits_used)
        """,
    ),
    "query_history": (
        """
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id TEXT,
            warehouse_name TEXT,
            user_name TEXT,
            role_name TEXT,
            start_time TEXT,
            end_time TEXT,
            total_elapsed_ms INTEGER,
            bytes_scanned INTEGER,
            rows_produced INTEGER,
            query_text TEXT
        )
        """,
        """
        INSERT INTO query_history (
            query_id, warehouse_name, user_name, role_name,
            start_time, end_time, total_elapsed_ms, bytes_scanned,
            rows_produced, query_text
        )
        VALUES (
            :query_id, :warehouse_name, :user_name, :role_name,
            :start_time, :end_time, :total_elapsed_ms, :bytes_scanned,
            :rows_produced, :query_text
        )
        """,
    ),
    "role_grants": (
        """
        CREATE TABLE IF NOT EXISTS role_grants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT,
            grantee_name TEXT,
            grantee_type TEXT,
            privilege TEXT,
            granted_on TEXT
        )
        """,
        """
        INSERT INTO role_grants (role_name, grantee_name, grantee_type, privilege, granted_on)
        VALUES (:role_name, :grantee_name, :grantee_type, :privilege, :granted_on)
        """,
    ),
    "role_usage": (
        """
        CREATE TABLE IF NOT EXISTS role_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT,
            last_used_at TEXT
        )
        """,
        """
        INSERT INTO role_usage (role_name, last_used_at)
        VALUES (:role_name, :last_used_at)
        """,
    ),
    "object_access": (
        """
        CREATE TABLE IF NOT EXISTS object_access (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            object_name TEXT,
            object_type TEXT,
            role_name TEXT,
            access_count INTEGER
        )
        """,
        """
        INSERT INTO object_access (object_name, object_type, role_name, access_count)
        VALUES (:object_name, :object_type, :role_name, :access_count)
        """,
    ),
}

TYPE_CASTS = {
    "warehouses": {"credit_per_hour": float},
    "warehouse_metering": {
        "credits_used": float,
        "start_time": str,
        "end_time": str,
    },
    "query_history": {
        "total_elapsed_ms": int,
        "bytes_scanned": int,
        "rows_produced": int,
    },
    "role_usage": {"last_used_at": str},
    "object_access": {"access_count": int},
}


def _apply_casts(dataset: str, row: dict[str, str]) -> dict:
    casts = TYPE_CASTS.get(dataset, {})
    converted: dict = {}
    for key, value in row.items():
        converter = casts.get(key)
        converted[key] = converter(value) if converter else value
    return converted


def ingest_csvs(data_dir: Path) -> None:
    connection = get_connection()
    cursor = connection.cursor()
    for table_name, (ddl, insert_sql) in TABLES.items():
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(ddl)
        csv_path = data_dir / f"{table_name}.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing dataset: {csv_path}")
        with csv_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = [_apply_casts(table_name, row) for row in reader]
            if rows:
                cursor.executemany(insert_sql, rows)
    connection.commit()
    connection.close()


def ingest_demo_data() -> None:
    ingest_csvs(Path("data/demo"))


def touch_ingest_time() -> str:
    return datetime.utcnow().isoformat()
