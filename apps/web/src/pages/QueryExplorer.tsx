import { useEffect, useMemo, useState } from "react";

import type { QueryHistory, QueryInsight } from "@frostsight/shared/src/types";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { LineChart } from "../components/LineChart";
import "./Pages.css";

export function QueryExplorerPage() {
  const [queries, setQueries] = useState<QueryHistory[]>([]);
  const [insights, setInsights] = useState<QueryInsight | null>(null);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    api.queries().then(setQueries).catch(() => setQueries([]));
    api.queryInsights().then(setInsights).catch(() => setInsights(null));
  }, []);

  const filtered = useMemo(() => {
    if (!filter) {
      return queries;
    }
    return queries.filter((query) => query.warehouse_name.includes(filter));
  }, [queries, filter]);

  const latencyPoints =
    insights?.latency_trend.map((point) => ({
      label: point.day,
      value: point.p95_ms,
    })) ?? [];

  return (
    <section className="page">
      <h2>Query Explorer</h2>
      <div className="panel">
        <h3>Regression View (p95 latency)</h3>
        <LineChart points={latencyPoints} />
      </div>
      <div className="panel">
        <div className="filter-row">
          <label htmlFor="warehouse">Filter warehouse</label>
          <input
            id="warehouse"
            value={filter}
            onChange={(event) => setFilter(event.target.value)}
            placeholder="WH_CORE"
          />
        </div>
        <DataTable
          columns={[
            { header: "Query", render: (row) => row.query_id },
            { header: "Warehouse", render: (row) => row.warehouse_name },
            { header: "User", render: (row) => row.user_name },
            { header: "Elapsed (ms)", render: (row) => row.total_elapsed_ms },
          ]}
          data={filtered}
        />
      </div>
      <div className="panel">
        <h3>Top Expensive Queries</h3>
        <DataTable
          columns={[
            { header: "Query", render: (row) => row.query_id },
            { header: "Warehouse", render: (row) => row.warehouse_name },
            { header: "Elapsed (ms)", render: (row) => row.total_elapsed_ms },
          ]}
          data={insights?.top_expensive ?? []}
        />
      </div>
    </section>
  );
}
