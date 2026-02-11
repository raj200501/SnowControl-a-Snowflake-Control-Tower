import { useEffect, useState } from "react";

import type { WarehouseMetering } from "@frostsight/shared/src/types";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { LineChart } from "../components/LineChart";
import "./Pages.css";

export function CostExplorerPage() {
  const [metering, setMetering] = useState<WarehouseMetering[]>([]);

  useEffect(() => {
    api.metering().then(setMetering).catch(() => setMetering([]));
  }, []);

  const recent = metering.slice(-20);
  const chartPoints = recent.map((row) => ({
    label: row.start_time,
    value: row.credits_used,
  }));

  return (
    <section className="page">
      <h2>Cost Explorer</h2>
      <div className="panel">
        <h3>Warehouse Credit Timeline</h3>
        <LineChart points={chartPoints} />
      </div>
      <div className="panel">
        <h3>Top Warehouses</h3>
        <DataTable
          columns={[
            { header: "Warehouse", render: (row) => row.warehouse_name },
            { header: "Credits", render: (row) => row.credits_used.toFixed(2) },
            { header: "Start", render: (row) => new Date(row.start_time).toLocaleDateString() },
          ]}
          data={recent}
        />
      </div>
    </section>
  );
}
