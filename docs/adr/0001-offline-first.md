# ADR 0001: Offline-first Control Plane

## Status
Accepted

## Context
SnowControl must operate without Snowflake credentials. This requirement supports CI and
ensures deterministic behavior for planning and policy evaluation.

## Decision
Store desired state in YAML, compute diffs locally, and persist canonical state in JSON.
Snowflake connectivity is optional behind an interface.

## Consequences
- No network calls in tests.
- SQL rendering is deterministic and idempotent.
