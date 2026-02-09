# SnowControl: Snowflake Control Tower

**Tagline:** Offline-first Snowflake Platform Engineering + FinOps + Governance-as-Code toolkit.

SnowControl provides a deterministic control plane for Snowflake accounts. It parses a YAML
specification, computes a plan, renders SQL, and updates a local state backend without
requiring credentials.

## Key capabilities
- Offline-first "Snowflake as Code"
- Governance policy engine with built-in guardrails
- FinOps analytics on sample metering data
- Fast CLI workflows with Rich output

## Quick start
```bash
make bootstrap
make demo
```

## Screenshot (text-only)
```
$ snowcontrol plan
[
  {
    "action": "CREATE",
    "resource_type": "warehouse",
    "name": "WH_INGEST",
    "details": {
      "name": "WH_INGEST",
      "size": "MEDIUM",
      "auto_suspend": 300,
      "auto_resume": true,
      "scaling_policy": "STANDARD",
      "max_cluster_count": 2,
      "resource_monitor": "RM_CORE"
    }
  }
]
```
