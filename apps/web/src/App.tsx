import { NavLink, Route, Routes } from "react-router-dom";

import { AnomaliesPage } from "./pages/Anomalies";
import { CostExplorerPage } from "./pages/CostExplorer";
import { GovernancePage } from "./pages/Governance";
import { OverviewPage } from "./pages/Overview";
import { QueryExplorerPage } from "./pages/QueryExplorer";
import { SettingsPage } from "./pages/Settings";
import "./styles/App.css";

export function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span>FrostSight</span>
          <p>Cost + Performance + Governance</p>
        </div>
        <nav>
          <NavLink to="/" end>
            Overview
          </NavLink>
          <NavLink to="/cost">Cost Explorer</NavLink>
          <NavLink to="/queries">Query Explorer</NavLink>
          <NavLink to="/anomalies">Anomalies</NavLink>
          <NavLink to="/governance">Governance</NavLink>
          <NavLink to="/settings">Settings</NavLink>
        </nav>
      </aside>
      <main>
        <header className="topbar">
          <div>
            <h1>FrostSight Control Plane</h1>
            <p>Snowflake leadership dashboard (demo mode)</p>
          </div>
        </header>
        <Routes>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/cost" element={<CostExplorerPage />} />
          <Route path="/queries" element={<QueryExplorerPage />} />
          <Route path="/anomalies" element={<AnomaliesPage />} />
          <Route path="/governance" element={<GovernancePage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
    </div>
  );
}
