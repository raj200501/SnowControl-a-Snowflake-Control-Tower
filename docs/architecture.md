# Architecture

## Component diagram
```mermaid
flowchart LR
  CLI[CLI (Typer + Rich)] --> Config[Config Loader]
  CLI --> Diff[Diff Engine]
  Diff --> Plan[Plan Actions]
  Plan --> SQL[SQL Renderer]
  Plan --> State[Local State Backend]
  CLI --> Policies[Policy Engine]
  CLI --> FinOps[FinOps Report]
  Policies --> Config
  FinOps --> Data[Offline Metering Data]
```

## Plan/apply data flow
1. Load YAML config.
2. Read local state (JSON).
3. Compute diff actions.
4. Render SQL plan.
5. Apply updates to local state.

## Policy evaluation flow
1. Load policy config.
2. Evaluate built-in rules against desired config and plan.
3. Emit human-friendly results with severity overrides.
