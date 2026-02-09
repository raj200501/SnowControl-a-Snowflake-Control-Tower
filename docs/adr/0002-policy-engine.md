# ADR 0002: Policy Engine

## Status
Accepted

## Context
SnowControl needs governance guardrails that can be configured per account.

## Decision
Implement a policy framework with built-in rules and a YAML configuration file to enable,
disable, and adjust severity.

## Consequences
- Policies run against desired config and plan.
- Results are human-readable with Rich formatting in the CLI.
