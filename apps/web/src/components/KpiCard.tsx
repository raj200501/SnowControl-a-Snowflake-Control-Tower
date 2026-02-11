import type { ReactNode } from "react";

import "./KpiCard.css";

type KpiCardProps = {
  title: string;
  value: string;
  trend?: string;
  icon?: ReactNode;
};

export function KpiCard({ title, value, trend, icon }: KpiCardProps) {
  return (
    <div className="kpi-card">
      <div className="kpi-header">
        <span>{title}</span>
        {icon ? <span className="kpi-icon">{icon}</span> : null}
      </div>
      <div className="kpi-value">{value}</div>
      {trend ? <div className="kpi-trend">{trend}</div> : null}
    </div>
  );
}
