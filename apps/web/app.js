const API_URL = "http://localhost:8000";
const TOKEN = "local-dev-token";

const content = document.getElementById("content");
const pageTitle = document.getElementById("page-title");

async function request(path) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { Authorization: `Bearer ${TOKEN}` },
  });
  if (!response.ok) {
    throw new Error("Request failed");
  }
  return response.json();
}

function setActive(button) {
  document.querySelectorAll("nav button").forEach((btn) => btn.classList.remove("active"));
  button.classList.add("active");
}

function renderOverview(data) {
  content.innerHTML = `
    <div class="kpi-grid">
      <div class="kpi"><h3>${data.credits_today.toFixed(1)}</h3><p>Credits / Day</p></div>
      <div class="kpi"><h3>${data.p95_latency_today_ms.toFixed(0)} ms</h3><p>p95 Latency</p></div>
      <div class="kpi"><h3>${data.anomaly_count}</h3><p>Anomalies</p></div>
      <div class="kpi"><h3>${data.governance_issue_count}</h3><p>Governance</p></div>
    </div>
  `;
}

function renderTable(rows, headers) {
  const head = headers.map((header) => `<th>${header}</th>`).join("");
  const body = rows
    .map((row) => `<tr>${headers.map((key) => `<td>${row[key]}</td>`).join("")}</tr>`)
    .join("");
  return `<table class="table"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
}

async function loadPage(page) {
  if (page === "overview") {
    pageTitle.textContent = "Overview";
    const overview = await request("/api/v1/overview");
    renderOverview(overview);
    return;
  }
  if (page === "cost") {
    pageTitle.textContent = "Cost Explorer";
    const metering = await request("/api/v1/warehouse-metering?limit=10");
    content.innerHTML = `<div class="panel">${renderTable(metering, ["warehouse_name", "credits_used", "start_time"])}</div>`;
    return;
  }
  if (page === "queries") {
    pageTitle.textContent = "Query Explorer";
    const queries = await request("/api/v1/queries?limit=10");
    content.innerHTML = `<div class="panel">${renderTable(queries, ["query_id", "warehouse_name", "total_elapsed_ms"])}</div>`;
    return;
  }
  if (page === "anomalies") {
    pageTitle.textContent = "Anomalies";
    const anomalies = await request("/api/v1/anomalies");
    content.innerHTML = `<div class="panel">${renderTable(anomalies, ["day", "credits_used", "z_score"])}</div>`;
    return;
  }
  if (page === "governance") {
    pageTitle.textContent = "Governance";
    const findings = await request("/api/v1/governance/findings");
    const sql = findings
      .map((finding) => `<div class="code">${finding.recommendation_sql}</div>`)
      .join("");
    content.innerHTML = `<div class="panel">${renderTable(findings, ["finding_type", "severity", "description"])}</div><div class="panel">${sql}</div>`;
    return;
  }
  if (page === "settings") {
    pageTitle.textContent = "Settings";
    const status = await request("/api/v1/snowflake/status");
    content.innerHTML = `<div class="panel">Snowflake configured: ${status.configured}</div>`;
  }
}

window.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("nav button").forEach((button) => {
    button.addEventListener("click", () => {
      setActive(button);
      loadPage(button.dataset.page);
    });
  });
  loadPage("overview");
});
