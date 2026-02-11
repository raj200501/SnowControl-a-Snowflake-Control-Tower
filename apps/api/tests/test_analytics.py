import unittest
from datetime import datetime, timedelta

from app.analytics import (
    calculate_daily_credits,
    calculate_p95_latency_trend,
    detect_cost_anomalies,
    find_query_regressions,
    governance_lint,
    top_expensive_queries,
)


class AnalyticsTestCase(unittest.TestCase):
    def test_daily_credits(self) -> None:
        rows = [
            {"start_time": "2024-01-01T00:00:00", "credits_used": 3},
            {"start_time": "2024-01-01T02:00:00", "credits_used": 7},
            {"start_time": "2024-01-02T02:00:00", "credits_used": 5},
        ]
        daily = calculate_daily_credits(rows)
        self.assertEqual(len(daily), 2)
        self.assertEqual(daily[0].credits_used, 10)

    def test_latency_trend(self) -> None:
        rows = [
            {"start_time": "2024-01-01T00:00:00", "total_elapsed_ms": 100},
            {"start_time": "2024-01-01T01:00:00", "total_elapsed_ms": 200},
            {"start_time": "2024-01-02T00:00:00", "total_elapsed_ms": 300},
        ]
        trend = calculate_p95_latency_trend(rows)
        self.assertEqual(len(trend), 2)

    def test_regressions(self) -> None:
        base = datetime(2024, 1, 1)
        rows = []
        for day in range(20):
            for _idx in range(5):
                rows.append(
                    {
                        "warehouse_name": "WH_CORE",
                        "start_time": (base + timedelta(days=day)).isoformat(),
                        "total_elapsed_ms": 100 + day * 30,
                    }
                )
        regressions = find_query_regressions(rows)
        self.assertTrue(regressions)

    def test_top_expensive(self) -> None:
        rows = [
            {
                "query_id": "Q1",
                "warehouse_name": "WH_CORE",
                "total_elapsed_ms": 100,
                "bytes_scanned": 10,
                "user_name": "ava",
                "query_text": "select 1",
            },
            {
                "query_id": "Q2",
                "warehouse_name": "WH_CORE",
                "total_elapsed_ms": 500,
                "bytes_scanned": 20,
                "user_name": "ben",
                "query_text": "select 2",
            },
        ]
        top = top_expensive_queries(rows, limit=1)
        self.assertEqual(top[0].query_id, "Q2")

    def test_anomalies(self) -> None:
        rows = [
            {"start_time": "2024-01-01T00:00:00", "credits_used": 10},
            {"start_time": "2024-01-02T00:00:00", "credits_used": 11},
            {"start_time": "2024-01-03T00:00:00", "credits_used": 10},
            {"start_time": "2024-01-04T00:00:00", "credits_used": 12},
            {"start_time": "2024-01-05T00:00:00", "credits_used": 200},
        ]
        daily = calculate_daily_credits(rows)
        anomalies = detect_cost_anomalies(daily, window=3)
        self.assertTrue(anomalies)

    def test_governance(self) -> None:
        grants = [
            {"role_name": "SYSADMIN", "privilege": "ALL PRIVILEGES", "granted_on": "ACCOUNT"}
        ]
        usage = [{"role_name": "TEMP_ROLE", "last_used_at": "2020-01-01T00:00:00"}]
        access = [
            {
                "object_name": "CUSTOMERS",
                "object_type": "TABLE",
                "role_name": "ANALYST",
                "access_count": 200,
            }
        ]
        findings = governance_lint(grants, usage, access)
        self.assertEqual(len(findings), 3)
