# ADR 0003: Local State Backend

## Status
Accepted

## Context
We need deterministic plan/apply without Snowflake credentials.

## Decision
Use a JSON state file with a version field for future migrations.

## Consequences
- Simple, local persistence.
- Future backend options (SQLite) can be added behind the same interface.
