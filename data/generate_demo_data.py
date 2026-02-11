from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUTPUT_DIR = Path("data/demo")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_DATE = datetime(2024, 1, 1)
DAYS = 30

WAREHOUSES = [
    ("WH_CORE", "LARGE", 8.0),
    ("WH_ANALYTICS", "MEDIUM", 4.0),
    ("WH_INGEST", "SMALL", 2.0),
    ("WH_SCIENCE", "XLARGE", 16.0),
    ("WH_FINOPS", "SMALL", 2.0),
]

ROLES = ["SYSADMIN", "ANALYST", "DATA_ENGINEER", "SECURITY", "FINOPS", "TEMP_ROLE"]
USERS = ["ava", "ben", "chloe", "diego", "ellen", "frank"]

QUERY_TEMPLATES = [
    "select count(*) from sales where order_date >= '{date}'",
    "select * from sessions where user_id = '{user}' limit 100",
    "select region, sum(revenue) from revenue group by 1",
    "create temporary table stage_{day} as select * from raw_events",
    "select * from inventory where updated_at >= '{date}'",
]


@dataclass
class WarehouseMeteringRow:
    warehouse_name: str
    start_time: datetime
    end_time: datetime
    credits_used: float


def write_csv(filename: str, fieldnames: list[str], rows: list[dict]) -> None:
    with (OUTPUT_DIR / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_warehouses() -> None:
    rows = [
        {"name": name, "size": size, "credit_per_hour": credit}
        for name, size, credit in WAREHOUSES
    ]
    write_csv("warehouses.csv", ["name", "size", "credit_per_hour"], rows)


def generate_warehouse_metering() -> None:
    rows: list[dict] = []
    for day in range(DAYS):
        day_start = BASE_DATE + timedelta(days=day)
        for name, _, credit_per_hour in WAREHOUSES:
            hours = random.randint(8, 20)
            credits_used = round(hours * credit_per_hour * random.uniform(0.7, 1.1), 2)
            rows.append(
                {
                    "warehouse_name": name,
                    "start_time": day_start.isoformat(),
                    "end_time": (day_start + timedelta(hours=hours)).isoformat(),
                    "credits_used": credits_used,
                }
            )
    write_csv(
        "warehouse_metering.csv",
        ["warehouse_name", "start_time", "end_time", "credits_used"],
        rows,
    )


def generate_query_history() -> None:
    rows: list[dict] = []
    for day in range(DAYS):
        day_start = BASE_DATE + timedelta(days=day)
        for idx in range(60):
            warehouse = random.choice(WAREHOUSES)[0]
            role = random.choice(ROLES)
            user = random.choice(USERS)
            start_time = day_start + timedelta(minutes=random.randint(0, 1430))
            duration = random.randint(50, 4500)
            bytes_scanned = random.randint(10_000, 9_000_000)
            rows_produced = random.randint(10, 5000)
            query_text = random.choice(QUERY_TEMPLATES).format(
                date=day_start.date(), user=user, day=day
            )
            rows.append(
                {
                    "query_id": f"Q{day:02d}-{idx:03d}",
                    "warehouse_name": warehouse,
                    "user_name": user,
                    "role_name": role,
                    "start_time": start_time.isoformat(),
                    "end_time": (start_time + timedelta(milliseconds=duration)).isoformat(),
                    "total_elapsed_ms": duration,
                    "bytes_scanned": bytes_scanned,
                    "rows_produced": rows_produced,
                    "query_text": query_text,
                }
            )
    write_csv(
        "query_history.csv",
        [
            "query_id",
            "warehouse_name",
            "user_name",
            "role_name",
            "start_time",
            "end_time",
            "total_elapsed_ms",
            "bytes_scanned",
            "rows_produced",
            "query_text",
        ],
        rows,
    )


def generate_role_grants() -> None:
    rows = [
        {
            "role_name": "SYSADMIN",
            "grantee_name": "SECURITY",
            "grantee_type": "ROLE",
            "privilege": "ALL PRIVILEGES",
            "granted_on": "ACCOUNT",
        },
        {
            "role_name": "DATA_ENGINEER",
            "grantee_name": "ANALYST",
            "grantee_type": "ROLE",
            "privilege": "USAGE",
            "granted_on": "WAREHOUSE",
        },
        {
            "role_name": "TEMP_ROLE",
            "grantee_name": "ava",
            "grantee_type": "USER",
            "privilege": "USAGE",
            "granted_on": "DATABASE",
        },
        {
            "role_name": "ANALYST",
            "grantee_name": "ben",
            "grantee_type": "USER",
            "privilege": "USAGE",
            "granted_on": "DATABASE",
        },
        {
            "role_name": "FINOPS",
            "grantee_name": "ellen",
            "grantee_type": "USER",
            "privilege": "MONITOR",
            "granted_on": "WAREHOUSE",
        },
    ]
    write_csv(
        "role_grants.csv",
        ["role_name", "grantee_name", "grantee_type", "privilege", "granted_on"],
        rows,
    )


def generate_role_usage() -> None:
    rows = [
        {"role_name": "SYSADMIN", "last_used_at": (BASE_DATE + timedelta(days=2)).isoformat()},
        {"role_name": "ANALYST", "last_used_at": (BASE_DATE + timedelta(days=5)).isoformat()},
        {"role_name": "DATA_ENGINEER", "last_used_at": (BASE_DATE + timedelta(days=7)).isoformat()},
        {"role_name": "SECURITY", "last_used_at": (BASE_DATE + timedelta(days=1)).isoformat()},
        {"role_name": "FINOPS", "last_used_at": (BASE_DATE + timedelta(days=3)).isoformat()},
        {"role_name": "TEMP_ROLE", "last_used_at": (BASE_DATE - timedelta(days=40)).isoformat()},
    ]
    write_csv("role_usage.csv", ["role_name", "last_used_at"], rows)


def generate_object_access() -> None:
    objects = [
        ("CUSTOMERS", "TABLE"),
        ("ORDERS", "TABLE"),
        ("PAYMENTS", "TABLE"),
        ("PIPELINE", "STAGE"),
        ("RAW_EVENTS", "VIEW"),
    ]
    rows: list[dict] = []
    for object_name, object_type in objects:
        for role in ROLES:
            rows.append(
                {
                    "object_name": object_name,
                    "object_type": object_type,
                    "role_name": role,
                    "access_count": random.randint(0, 200),
                }
            )
    write_csv(
        "object_access.csv",
        ["object_name", "object_type", "role_name", "access_count"],
        rows,
    )


def main() -> None:
    generate_warehouses()
    generate_warehouse_metering()
    generate_query_history()
    generate_role_grants()
    generate_role_usage()
    generate_object_access()


if __name__ == "__main__":
    main()
