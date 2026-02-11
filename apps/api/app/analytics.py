from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from statistics import median


@dataclass(frozen=True)
class DailyCredits:
    day: date
    credits_used: float


@dataclass(frozen=True)
class WarehouseHotspot:
    warehouse_name: str
    credits_used: float


@dataclass(frozen=True)
class QueryLatencyPoint:
    day: date
    p95_ms: float


@dataclass(frozen=True)
class QueryRegression:
    warehouse_name: str
    p95_prev_ms: float
    p95_recent_ms: float
    delta_ms: float


@dataclass(frozen=True)
class QueryCostItem:
    query_id: str
    warehouse_name: str
    total_elapsed_ms: int
    bytes_scanned: int
    user_name: str
    query_text: str


@dataclass(frozen=True)
class Anomaly:
    day: date
    credits_used: float
    z_score: float


@dataclass(frozen=True)
class GovernanceFinding:
    finding_type: str
    severity: str
    description: str
    recommendation_sql: str


def calculate_daily_credits(rows: Iterable[dict]) -> list[DailyCredits]:
    totals: dict[date, float] = {}
    for row in rows:
        day = _parse_datetime(row["start_time"]).date()
        totals[day] = totals.get(day, 0.0) + float(row["credits_used"])
    return [DailyCredits(day=day, credits_used=credits) for day, credits in sorted(totals.items())]


def calculate_warehouse_hotspots(rows: Iterable[dict], top_n: int = 5) -> list[WarehouseHotspot]:
    totals: dict[str, float] = {}
    for row in rows:
        warehouse = row["warehouse_name"]
        totals[warehouse] = totals.get(warehouse, 0.0) + float(row["credits_used"])
    sorted_rows = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    return [
        WarehouseHotspot(warehouse_name=name, credits_used=credits)
        for name, credits in sorted_rows[:top_n]
    ]


def calculate_p95_latency_trend(rows: Iterable[dict]) -> list[QueryLatencyPoint]:
    day_buckets: dict[date, list[int]] = {}
    for row in rows:
        day = _parse_datetime(row["start_time"]).date()
        day_buckets.setdefault(day, []).append(int(row["total_elapsed_ms"]))
    trend: list[QueryLatencyPoint] = []
    for day, values in sorted(day_buckets.items()):
        trend.append(QueryLatencyPoint(day=day, p95_ms=_percentile(values, 95)))
    return trend


def find_query_regressions(rows: Iterable[dict]) -> list[QueryRegression]:
    cutoff = _recent_window(rows, days=14)
    previous_window = cutoff - timedelta(days=7)
    recent_window = cutoff
    buckets: dict[str, dict[str, list[int]]] = {}
    for row in rows:
        warehouse = row["warehouse_name"]
        start_time = _parse_datetime(row["start_time"])
        window_key = "recent" if start_time >= recent_window else "previous"
        if start_time < previous_window:
            continue
        buckets.setdefault(warehouse, {"previous": [], "recent": []})
        buckets[warehouse][window_key].append(int(row["total_elapsed_ms"]))
    regressions: list[QueryRegression] = []
    for warehouse, values in buckets.items():
        if not values["previous"] or not values["recent"]:
            continue
        prev_p95 = _percentile(values["previous"], 95)
        recent_p95 = _percentile(values["recent"], 95)
        delta = recent_p95 - prev_p95
        if delta > 250:
            regressions.append(
                QueryRegression(
                    warehouse_name=warehouse,
                    p95_prev_ms=prev_p95,
                    p95_recent_ms=recent_p95,
                    delta_ms=delta,
                )
            )
    return regressions


def top_expensive_queries(rows: Iterable[dict], limit: int = 10) -> list[QueryCostItem]:
    sorted_rows = sorted(rows, key=lambda row: int(row["total_elapsed_ms"]), reverse=True)
    top = sorted_rows[:limit]
    return [
        QueryCostItem(
            query_id=row["query_id"],
            warehouse_name=row["warehouse_name"],
            total_elapsed_ms=int(row["total_elapsed_ms"]),
            bytes_scanned=int(row["bytes_scanned"]),
            user_name=row["user_name"],
            query_text=row["query_text"],
        )
        for row in top
    ]


def detect_cost_anomalies(daily_credits: list[DailyCredits], window: int = 7) -> list[Anomaly]:
    anomalies: list[Anomaly] = []
    for idx in range(window, len(daily_credits)):
        history = [point.credits_used for point in daily_credits[idx - window : idx]]
        if not history:
            continue
        med = median(history)
        mad = median([abs(value - med) for value in history]) or 1.0
        current = daily_credits[idx]
        z_score = 0.6745 * (current.credits_used - med) / mad
        if z_score > 3.5:
            anomalies.append(
                Anomaly(
                    day=current.day,
                    credits_used=current.credits_used,
                    z_score=z_score,
                )
            )
    return anomalies


def governance_lint(
    role_grants: Iterable[dict],
    role_usage: Iterable[dict],
    object_access: Iterable[dict],
) -> list[GovernanceFinding]:
    findings: list[GovernanceFinding] = []
    for grant in role_grants:
        if grant["privilege"] == "ALL PRIVILEGES" or grant["granted_on"] == "ACCOUNT":
            findings.append(
                GovernanceFinding(
                    finding_type="RISKY_GRANT",
                    severity="high",
                    description=(
                        f"Role {grant['role_name']} has elevated privilege on "
                        f"{grant['granted_on']}."
                    ),
                    recommendation_sql=(
                        f"REVOKE {grant['privilege']} ON {grant['granted_on']} FROM ROLE "
                        f"{grant['role_name']};"
                    ),
                )
            )
    cutoff = datetime.utcnow() - timedelta(days=30)
    for usage in role_usage:
        last_used = _parse_datetime(usage["last_used_at"])
        if last_used < cutoff:
            findings.append(
                GovernanceFinding(
                    finding_type="UNUSED_ROLE",
                    severity="medium",
                    description=f"Role {usage['role_name']} has not been used in 30+ days.",
                    recommendation_sql=f"DROP ROLE IF EXISTS {usage['role_name']};",
                )
            )
    for access in object_access:
        if int(access["access_count"]) > 150:
            findings.append(
                GovernanceFinding(
                    finding_type="BROAD_ACCESS",
                    severity="low",
                    description=(
                        f"Role {access['role_name']} has high access volume on "
                        f"{access['object_name']}."
                    ),
                    recommendation_sql=(
                        f"REVOKE ALL ON {access['object_type']} {access['object_name']} "
                        f"FROM ROLE {access['role_name']};"
                    ),
                )
            )
    return findings


def _parse_datetime(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


def _percentile(values: list[int], percentile: int) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    k = (len(sorted_values) - 1) * percentile / 100
    f = int(k)
    c = min(f + 1, len(sorted_values) - 1)
    if f == c:
        return float(sorted_values[int(k)])
    d0 = sorted_values[f] * (c - k)
    d1 = sorted_values[c] * (k - f)
    return float(d0 + d1)


def _recent_window(rows: Iterable[dict], days: int) -> datetime:
    timestamps = [
        _parse_datetime(row["start_time"]) for row in rows if row.get("start_time")
    ]
    if not timestamps:
        return datetime.utcnow()
    latest = max(timestamps)
    return latest - timedelta(days=days)
