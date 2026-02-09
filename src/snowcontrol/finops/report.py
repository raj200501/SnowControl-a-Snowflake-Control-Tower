from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from rich.table import Table

from snowcontrol.finops.anomalies import z_score_flags
from snowcontrol.finops.ingest import load_csv
from snowcontrol.finops.metrics import credits_by_day, credits_by_warehouse
from snowcontrol.utils.console import console


def moving_average(values: list[float], window: int = 3) -> float:
    if not values:
        return 0.0
    if len(values) < window:
        return sum(values) / len(values)
    return sum(values[-window:]) / window


def generate_report(metering_path: Path, out_dir: Path) -> dict[str, Any]:
    rows = load_csv(metering_path)
    by_day = credits_by_day(rows)
    by_warehouse = credits_by_warehouse(rows)
    flagged = z_score_flags(by_day)
    forecast = moving_average(list(by_day.values()))

    out_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "top_warehouses": sorted(by_warehouse.items(), key=lambda x: x[1], reverse=True),
        "cost_by_day": by_day,
        "anomalies": flagged,
        "forecast_next_day_credits": forecast,
    }
    with (out_dir / "finops_report.json").open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)

    md_lines = ["# FinOps Report", "", "## Top Warehouses"]
    for warehouse, credits in report["top_warehouses"]:
        md_lines.append(f"- {warehouse}: {credits:.2f} credits")
    md_lines.append("\n## Anomalies")
    if flagged:
        md_lines.extend([f"- {day}" for day in flagged])
    else:
        md_lines.append("- None")
    md_lines.append("\n## Forecast")
    md_lines.append(f"Next day credits (SMA): {forecast:.2f}")
    with (out_dir / "finops_report.md").open("w", encoding="utf-8") as handle:
        handle.write("\n".join(md_lines) + "\n")

    table = Table(title="Top Warehouses by Credits")
    table.add_column("Warehouse")
    table.add_column("Credits", justify="right")
    for warehouse, credits in report["top_warehouses"]:
        table.add_row(warehouse, f"{credits:.2f}")
    console.print(table)
    return report
