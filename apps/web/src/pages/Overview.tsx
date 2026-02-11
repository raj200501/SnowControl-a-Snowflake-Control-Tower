import { useEffect, useState } from "react";

import type { Overview, WarehouseMetering } from "@frostsight/shared/src/types";
import { api } from "../api/client";
import { KpiCard } from "../components/KpiCard";
import { LineChart } from "../components/LineChart";
import "./Pages.css";

export function OverviewPage() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [metering, setMetering] = useState<WarehouseMetering[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([api.overview(), api.metering()])
      .then(([overviewData, meteringData]) => {
        setOverview(overviewData);
        setMetering(meteringData);
      })
      .catch((err: Error) => setError(err.message));
  }, []);

  const chartPoints = metering
    .slice(-14)
    .map((row) => ({ label: row.start_time, value: row.credits_used }));

  return (
    <section className="page">
      <h2>Overview</h2>
      {error ? <div className="error">{error}</div> : null}
      <div className="kpi-grid">
        <KpiCard
          title="Credits / Day"
          value={overview ? overview.credits_today.toFixed(1) : "--"}
          trend="Last 24h burn"
        />
        <KpiCard
          title="p95 Latency"
          value={overview ? `${overview.p95_latency_today_ms.toFixed(0)} ms` : "--"}
          trend="Rolling p95"
        />
        <KpiCard
          title="Anomalies"
          value={overview ? `${overview.anomaly_count}` : "--"}
          trend="MAD-based detection"
        />
        <KpiCard
          title="Governance Issues"
          value={overview ? `${overview.governance_issue_count}` : "--"}
          trend="Lint findings"
        />
      </div>
      <div className="panel">
        <h3>Credit Burn Trend</h3>
        <LineChart points={chartPoints} />
      </div>
    </section>
  );
}
