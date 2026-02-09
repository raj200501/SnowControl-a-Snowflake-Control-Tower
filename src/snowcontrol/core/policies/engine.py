from __future__ import annotations

from pathlib import Path

import yaml

from snowcontrol.config.schema import DesiredConfig
from snowcontrol.core.models import PlanAction
from snowcontrol.core.policies.rules import Policy, PolicyResult


class PolicyConfigError(RuntimeError):
    pass


def load_policy_config(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except FileNotFoundError as exc:
        raise PolicyConfigError(f"Policy config not found: {path}") from exc
    if not isinstance(data, dict):
        raise PolicyConfigError("Policy config must be a mapping")
    return data


def evaluate_policies(
    desired: DesiredConfig,
    plan: list[PlanAction],
    policies: list[Policy],
    config: dict,
) -> list[PolicyResult]:
    results: list[PolicyResult] = []
    policy_settings = config.get("policies", {})
    for policy in policies:
        settings = policy_settings.get(policy.policy_id, {})
        if settings.get("enabled", True) is False:
            continue
        policy_results = policy.evaluator(desired, plan)
        allowlist = set(settings.get("allowlist", []))
        for result in policy_results:
            if result.message in allowlist:
                continue
            severity = settings.get("severity", result.severity)
            results.append(
                PolicyResult(
                    policy_id=result.policy_id,
                    severity=severity,
                    message=result.message,
                )
            )
    return results
