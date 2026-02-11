from __future__ import annotations

import json
import os
from datetime import date, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from app.analytics import (
    calculate_daily_credits,
    calculate_p95_latency_trend,
    detect_cost_anomalies,
    find_query_regressions,
    governance_lint,
    top_expensive_queries,
)
from app.db import get_connection, get_db_path
from app.ingest import ingest_demo_data
from app.snowflake import snowflake_status

DEFAULT_TOKEN = "local-dev-token"


def _require_auth(headers) -> bool:
    token = os.getenv("LOCAL_DEV_TOKEN", DEFAULT_TOKEN)
    auth = headers.get("Authorization", "")
    return auth == f"Bearer {token}"


def _serialize_value(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def _serialize_dict(data: dict) -> dict:
    return {key: _serialize_value(value) for key, value in data.items()}


def _serialize_list(items: list[dict]) -> list[dict]:
    return [_serialize_dict(item) for item in items]


def _json_response(handler: BaseHTTPRequestHandler, payload: object, status: int = 200) -> None:
    data = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def _query_param(query: dict[str, list[str]], key: str, default: int) -> int:
    try:
        return int(query.get(key, [str(default)])[0])
    except ValueError:
        return default


def _fetch_all(query: str, params: tuple = ()) -> list[dict]:
    conn = get_connection()
    cursor = conn.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


class FrostSightHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/v1/health":
            _json_response(self, {"status": "ok"})
            return
        if not _require_auth(self.headers):
            _json_response(self, {"detail": "unauthorized"}, status=HTTPStatus.UNAUTHORIZED)
            return
        query = parse_qs(parsed.query)
        if parsed.path == "/api/v1/overview":
            metering = _fetch_all("SELECT * FROM warehouse_metering")
            daily = calculate_daily_credits(metering)
            queries = _fetch_all("SELECT * FROM query_history LIMIT 500")
            latency = calculate_p95_latency_trend(queries)
            anomalies = detect_cost_anomalies(daily)
            governance = governance_lint(
                _fetch_all("SELECT * FROM role_grants"),
                _fetch_all("SELECT * FROM role_usage"),
                _fetch_all("SELECT * FROM object_access"),
            )
            payload = {
                "credits_today": daily[-1].credits_used if daily else 0.0,
                "p95_latency_today_ms": latency[-1].p95_ms if latency else 0.0,
                "anomaly_count": len(anomalies),
                "governance_issue_count": len(governance),
            }
            _json_response(self, payload)
            return
        if parsed.path == "/api/v1/warehouses":
            limit = _query_param(query, "limit", 50)
            offset = _query_param(query, "offset", 0)
            rows = _fetch_all(
                "SELECT * FROM warehouses LIMIT ? OFFSET ?",
                (limit, offset),
            )
            _json_response(self, _serialize_list(rows))
            return
        if parsed.path == "/api/v1/warehouse-metering":
            limit = _query_param(query, "limit", 200)
            offset = _query_param(query, "offset", 0)
            rows = _fetch_all(
                "SELECT * FROM warehouse_metering LIMIT ? OFFSET ?",
                (limit, offset),
            )
            _json_response(self, _serialize_list(rows))
            return
        if parsed.path == "/api/v1/queries":
            limit = _query_param(query, "limit", 100)
            offset = _query_param(query, "offset", 0)
            rows = _fetch_all(
                "SELECT * FROM query_history LIMIT ? OFFSET ?",
                (limit, offset),
            )
            _json_response(self, _serialize_list(rows))
            return
        if parsed.path == "/api/v1/queries/insights":
            query_rows = _fetch_all("SELECT * FROM query_history LIMIT 500")
            payload = {
                "latency_trend": [item.__dict__ for item in calculate_p95_latency_trend(query_rows)],
                "regressions": [item.__dict__ for item in find_query_regressions(query_rows)],
                "top_expensive": [item.__dict__ for item in top_expensive_queries(query_rows)],
            }
            _json_response(self, _serialize_dict(payload))
            return
        if parsed.path == "/api/v1/anomalies":
            limit = _query_param(query, "limit", 50)
            offset = _query_param(query, "offset", 0)
            metering = _fetch_all("SELECT * FROM warehouse_metering")
            daily = calculate_daily_credits(metering)
            anomalies = detect_cost_anomalies(daily)
            payload = [_serialize_dict(item.__dict__) for item in anomalies[offset : offset + limit]]
            _json_response(self, payload)
            return
        if parsed.path == "/api/v1/governance/findings":
            limit = _query_param(query, "limit", 100)
            offset = _query_param(query, "offset", 0)
            findings = governance_lint(
                _fetch_all("SELECT * FROM role_grants"),
                _fetch_all("SELECT * FROM role_usage"),
                _fetch_all("SELECT * FROM object_access"),
            )
            payload = [_serialize_dict(item.__dict__) for item in findings[offset : offset + limit]]
            _json_response(self, payload)
            return
        if parsed.path == "/api/v1/snowflake/status":
            _json_response(self, snowflake_status())
            return
        _json_response(self, {"detail": "not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if not _require_auth(self.headers):
            _json_response(self, {"detail": "unauthorized"}, status=HTTPStatus.UNAUTHORIZED)
            return
        if parsed.path == "/api/v1/ingest/demo":
            ingest_demo_data()
            _json_response(self, {"status": "demo_ingested", "db": str(get_db_path())})
            return
        _json_response(self, {"detail": "not found"}, status=HTTPStatus.NOT_FOUND)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> HTTPServer:
    server = HTTPServer((host, port), FrostSightHandler)
    return server


if __name__ == "__main__":
    ingest_demo_data()
    httpd = run_server()
    print("FrostSight API running on http://0.0.0.0:8000")
    httpd.serve_forever()
