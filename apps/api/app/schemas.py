from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class WarehouseOut(BaseModel):
    id: int
    name: str
    size: str
    credit_per_hour: float


class WarehouseMeteringOut(BaseModel):
    id: int
    warehouse_name: str
    start_time: datetime
    end_time: datetime
    credits_used: float


class QueryHistoryOut(BaseModel):
    id: int
    query_id: str
    warehouse_name: str
    user_name: str
    role_name: str
    start_time: datetime
    end_time: datetime
    total_elapsed_ms: int
    bytes_scanned: int
    rows_produced: int
    query_text: str


class DailyCreditsOut(BaseModel):
    day: date
    credits_used: float


class WarehouseHotspotOut(BaseModel):
    warehouse_name: str
    credits_used: float


class QueryLatencyPointOut(BaseModel):
    day: date
    p95_ms: float


class QueryRegressionOut(BaseModel):
    warehouse_name: str
    p95_prev_ms: float
    p95_recent_ms: float
    delta_ms: float


class QueryCostItemOut(BaseModel):
    query_id: str
    warehouse_name: str
    total_elapsed_ms: int
    bytes_scanned: int
    user_name: str
    query_text: str


class AnomalyOut(BaseModel):
    day: date
    credits_used: float
    z_score: float = Field(..., description="MAD-based z-score")


class GovernanceFindingOut(BaseModel):
    finding_type: str
    severity: str
    description: str
    recommendation_sql: str


class OverviewOut(BaseModel):
    credits_today: float
    p95_latency_today_ms: float
    anomaly_count: int
    governance_issue_count: int


class QueryInsightsOut(BaseModel):
    latency_trend: list[QueryLatencyPointOut]
    regressions: list[QueryRegressionOut]
    top_expensive: list[QueryCostItemOut]
