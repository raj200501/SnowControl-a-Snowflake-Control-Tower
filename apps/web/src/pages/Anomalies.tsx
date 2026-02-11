import { useEffect, useState } from "react";

import type { Anomaly } from "@frostsight/shared/src/types";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import "./Pages.css";

export function AnomaliesPage() {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [selected, setSelected] = useState<Anomaly | null>(null);

  useEffect(() => {
    api.anomalies().then(setAnomalies).catch(() => setAnomalies([]));
  }, []);

  return (
    <section className="page">
      <h2>Anomalies</h2>
      <div className="panel">
        <DataTable
          columns={[
            { header: "Day", render: (row) => row.day },
            { header: "Credits", render: (row) => row.credits_used.toFixed(2) },
            { header: "Z-Score", render: (row) => row.z_score.toFixed(2) },
          ]}
          data={anomalies}
        />
      </div>
      <div className="panel">
        <h3>Explain</h3>
        <div className="explain-box">
          {selected ? (
            <>
              <p>Spike on {selected.day}</p>
              <p>Credits used: {selected.credits_used.toFixed(2)}</p>
              <p>Deviation score: {selected.z_score.toFixed(2)}</p>
            </>
          ) : (
            <p>Select a row to see why it was flagged.</p>
          )}
        </div>
        <div className="cta-row">
          {anomalies.slice(0, 3).map((row) => (
            <button key={row.day} type="button" onClick={() => setSelected(row)}>
              Explain {row.day}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
