# Roadmap

12 two-week sprints for a six-month program.

## Sprint 1
- Goals: establish repo scaffolding, CI, tooling.
- Deliverables: pyproject, CI pipeline, Makefile.
- Risks: dependency drift.
- DoD: `make verify` green.

## Sprint 2
- Goals: config schema + loader + examples.
- Deliverables: YAML schema, sample configs.
- Risks: schema complexity.
- DoD: validation tests pass.

## Sprint 3
- Goals: state backend + diff engine.
- Deliverables: JSON backend, diff logic.
- Risks: deterministic ordering.
- DoD: diff tests pass.

## Sprint 4
- Goals: planner + SQL rendering.
- Deliverables: action model, SQL output.
- Risks: SQL correctness.
- DoD: SQL snapshot tests.

## Sprint 5
- Goals: policy engine.
- Deliverables: rule framework + default pack.
- Risks: false positives.
- DoD: policy tests pass.

## Sprint 6
- Goals: FinOps analytics.
- Deliverables: ingest, report output.
- Risks: deterministic forecasts.
- DoD: report tests pass.

## Sprint 7
- Goals: CLI polish + demo.
- Deliverables: Typer commands, demo flow.
- Risks: UX regressions.
- DoD: CLI smoke tests.

## Sprint 8
- Goals: documentation + ADRs.
- Deliverables: docs site, ADRs.
- Risks: stale docs.
- DoD: mkdocs build passes.

## Sprint 9
- Goals: hardening + edge cases.
- Deliverables: defensive checks.
- Risks: overfitting.
- DoD: coverage maintained.

## Sprint 10
- Goals: performance optimizations.
- Deliverables: plan rendering improvements.
- Risks: complexity.
- DoD: benchmarks within tolerance.

## Sprint 11
- Goals: contributor workflows.
- Deliverables: contributing guide.
- Risks: onboarding friction.
- DoD: smooth local setup.

## Sprint 12
- Goals: release readiness.
- Deliverables: tagged release, changelog.
- Risks: feature creep.
- DoD: release checklist complete.
