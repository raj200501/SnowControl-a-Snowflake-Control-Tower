# Architecture Decisions

## ADR-001: FastAPI + SQLite for the demo backend
We chose FastAPI for its automatic OpenAPI docs and strong typing, plus SQLite for deterministic local persistence with zero credentials. This keeps CI green and demo mode self-contained.

## ADR-002: Synthetic ACCOUNT_USAGE-like CSVs
Demo mode uses locally generated CSVs committed under `data/demo/` to avoid any network dependency. A generator script ensures the dataset is reproducible.

## ADR-003: Simple analytics primitives
Cost anomalies use rolling median + MAD z-score and regressions use p95 trend deltas. These techniques are robust, easy to explain, and fast to execute.

## ADR-004: React + Vite frontend
Vite provides fast local dev and a stable build pipeline. We keep charting lightweight with SVG components to avoid heavy dependencies.
