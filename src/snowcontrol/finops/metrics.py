from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Iterable


def parse_date(value: str) -> str:
    return datetime.fromisoformat(value).date().isoformat()


def credits_by_day(rows: Iterable[dict[str, str]]) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    for row in rows:
        day = parse_date(row["start_time"])
        totals[day] += float(row["credits_used"])
    return dict(totals)


def credits_by_warehouse(rows: Iterable[dict[str, str]]) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    for row in rows:
        totals[row["warehouse"]] += float(row["credits_used"])
    return dict(totals)
