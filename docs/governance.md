# Governance

SnowControl ships with a default policy pack focused on cost and security guardrails.

## Built-in policies
1. Warehouses must have auto_suspend <= 300 seconds.
2. No grants to PUBLIC except USAGE on database UTILS.
3. PII-tagged columns must have a masking policy attached.
4. Resource monitors required for any warehouse >= LARGE.
5. Shares may only expose secure views.

## Configuration
Policies are configured in a single YAML file:

```yaml
policies:
  WAREHOUSE_AUTO_SUSPEND:
    enabled: true
    severity: HIGH
```
