import { useEffect, useState } from "react";

import { API_URL } from "../api/client";
import "./Pages.css";

type SnowflakeStatus = {
  configured: boolean;
  missing: string[];
};

export function SettingsPage() {
  const [status, setStatus] = useState<SnowflakeStatus | null>(null);

  useEffect(() => {
    fetch(`${API_URL}/api/v1/snowflake/status`, {
      headers: {
        Authorization: `Bearer ${import.meta.env.VITE_LOCAL_TOKEN ?? "local-dev-token"}`,
      },
    })
      .then((response) => response.json())
      .then(setStatus)
      .catch(() => setStatus({ configured: false, missing: ["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER"] }));
  }, []);

  return (
    <section className="page">
      <h2>Settings</h2>
      <div className="panel">
        <h3>Mode</h3>
        <div className="toggle-row">
          <span>Demo Mode</span>
          <span className="pill">DEFAULT</span>
        </div>
        <div className="toggle-row">
          <span>Snowflake Mode</span>
          <span className={status?.configured ? "pill success" : "pill warn"}>
            {status?.configured ? "CONFIGURED" : "NOT CONFIGURED"}
          </span>
        </div>
        {status?.missing?.length ? (
          <p className="note">Missing env vars: {status.missing.join(", ")}</p>
        ) : null}
      </div>
      <div className="panel">
        <h3>Connection</h3>
        <p>API base URL: {API_URL}</p>
      </div>
    </section>
  );
}
