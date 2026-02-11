import { useEffect, useState } from "react";

import type { GovernanceFinding } from "@frostsight/shared/src/types";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import "./Pages.css";

export function GovernancePage() {
  const [findings, setFindings] = useState<GovernanceFinding[]>([]);

  useEffect(() => {
    api.governance().then(setFindings).catch(() => setFindings([]));
  }, []);

  return (
    <section className="page">
      <h2>Governance</h2>
      <div className="panel">
        <h3>Lint Rules</h3>
        <DataTable
          columns={[
            { header: "Type", render: (row) => row.finding_type },
            { header: "Severity", render: (row) => row.severity },
            { header: "Description", render: (row) => row.description },
          ]}
          data={findings}
        />
      </div>
      <div className="panel">
        <h3>Recommended SQL</h3>
        <ul className="sql-list">
          {findings.map((finding) => (
            <li key={finding.recommendation_sql}>
              <code>{finding.recommendation_sql}</code>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
