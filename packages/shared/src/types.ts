export type Warehouse = {
  id: number;
  name: string;
  size: string;
  credit_per_hour: number;
};

export type WarehouseMetering = {
  id: number;
  warehouse_name: string;
  start_time: string;
  end_time: string;
  credits_used: number;
};

export type QueryHistory = {
  id: number;
  query_id: string;
  warehouse_name: string;
  user_name: string;
  role_name: string;
  start_time: string;
  end_time: string;
  total_elapsed_ms: number;
  bytes_scanned: number;
  rows_produced: number;
  query_text: string;
};

export type Overview = {
  credits_today: number;
  p95_latency_today_ms: number;
  anomaly_count: number;
  governance_issue_count: number;
};

export type QueryInsight = {
  latency_trend: { day: string; p95_ms: number }[];
  regressions: {
    warehouse_name: string;
    p95_prev_ms: number;
    p95_recent_ms: number;
    delta_ms: number;
  }[];
  top_expensive: {
    query_id: string;
    warehouse_name: string;
    total_elapsed_ms: number;
    bytes_scanned: number;
    user_name: string;
    query_text: string;
  }[];
};

export type Anomaly = {
  day: string;
  credits_used: number;
  z_score: number;
};

export type GovernanceFinding = {
  finding_type: string;
  severity: string;
  description: string;
  recommendation_sql: string;
};
