import type {
  Anomaly,
  GovernanceFinding,
  Overview,
  QueryHistory,
  QueryInsight,
  Warehouse,
  WarehouseMetering,
} from "@frostsight/shared/src/types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const TOKEN = import.meta.env.VITE_LOCAL_TOKEN ?? "local-dev-token";

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      Authorization: `Bearer ${TOKEN}`,
    },
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || "Request failed");
  }
  return response.json() as Promise<T>;
}

export const api = {
  overview: () => request<Overview>("/api/v1/overview"),
  warehouses: () => request<Warehouse[]>("/api/v1/warehouses?limit=100"),
  metering: () => request<WarehouseMetering[]>("/api/v1/warehouse-metering"),
  queries: () => request<QueryHistory[]>("/api/v1/queries?limit=50"),
  queryInsights: () => request<QueryInsight>("/api/v1/queries/insights"),
  anomalies: () => request<Anomaly[]>("/api/v1/anomalies"),
  governance: () => request<GovernanceFinding[]>("/api/v1/governance/findings"),
};

export { API_URL, TOKEN };
