# SnowControl: Snowflake Control Tower

**Tagline:** Offline-first Snowflake Platform Engineering + FinOps + Governance-as-Code toolkit.

SnowControl is a deterministic control plane for Snowflake. Define account resources in YAML,
compute a plan, render Snowflake SQL, and update a local state backend — all without credentials.

## Why SnowControl?
- **Platform engineering**: manage warehouses, databases, schemas, roles, tags, masking policies, and shares.
- **Governance-as-code**: enforce guardrails with policy packs.
- **FinOps**: run cost analytics on offline sample data.
- **Offline-first**: no Snowflake credentials needed for CI or local demos.

## Quickstart (under 5 minutes)
```bash
make bootstrap
make demo
```

## CLI overview
```bash
snowcontrol init
snowcontrol validate
snowcontrol plan
snowcontrol render
snowcontrol apply
snowcontrol finops report
```

## Demo output (text-only screenshot)
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

## Project structure
```
src/snowcontrol/    # core logic
examples/           # sample YAML configs
finops/             # offline analytics
out/                # report outputs
```

## Limitations
SnowControl is not a full Snowflake emulator. It is a deterministic control plane + SQL generator
that focuses on safe planning, policy enforcement, and local state tracking.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT. See [LICENSE](LICENSE).
