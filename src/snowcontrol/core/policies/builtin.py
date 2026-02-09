from __future__ import annotations

from snowcontrol.config.schema import DesiredConfig
from snowcontrol.core.models import PlanAction
from snowcontrol.core.policies.rules import Policy, PolicyResult


def _warehouse_auto_suspend(desired: DesiredConfig, _: list[PlanAction]) -> list[PolicyResult]:
    results: list[PolicyResult] = []
    for warehouse in desired.warehouses:
        if warehouse.auto_suspend > 300:
            results.append(
                PolicyResult(
                    policy_id="WAREHOUSE_AUTO_SUSPEND",
                    severity="HIGH",
                    message=f"Warehouse {warehouse.name} auto_suspend exceeds 300s",
                )
            )
    return results


def _no_public_grants(desired: DesiredConfig, _: list[PlanAction]) -> list[PolicyResult]:
    results: list[PolicyResult] = []
    for grant in desired.grants:
        if grant.role.upper() == "PUBLIC":
            allowed = grant.privilege.upper() == "USAGE" and grant.on_name.upper() == "UTILS"
            if not allowed:
                results.append(
                    PolicyResult(
                        policy_id="NO_PUBLIC_GRANTS",
                        severity="HIGH",
                        message=(
                            "PUBLIC grants must be limited to USAGE on UTILS database"
                        ),
                    )
                )
    return results


def _pii_masking(desired: DesiredConfig, _: list[PlanAction]) -> list[PolicyResult]:
    results: list[PolicyResult] = []
    pii_objects = {
        (attachment.object_type, attachment.object_name)
        for attachment in desired.tag_attachments
        if attachment.tag.upper() == "PII"
    }
    masked_objects = {
        (attachment.object_type, attachment.object_name)
        for attachment in desired.masking_attachments
    }
    for obj in sorted(pii_objects - masked_objects):
        results.append(
            PolicyResult(
                policy_id="PII_MASKING",
                severity="MEDIUM",
                message=f"PII tagged object {obj[0]} {obj[1]} missing masking policy",
            )
        )
    return results


def _resource_monitor_for_large(desired: DesiredConfig, _: list[PlanAction]) -> list[PolicyResult]:
    results: list[PolicyResult] = []
    large_sizes = {"LARGE", "XLARGE", "XXLARGE"}
    for warehouse in desired.warehouses:
        if warehouse.size in large_sizes and not warehouse.resource_monitor:
            results.append(
                PolicyResult(
                    policy_id="WAREHOUSE_RESOURCE_MONITOR",
                    severity="MEDIUM",
                    message=f"Warehouse {warehouse.name} lacks resource monitor",
                )
            )
    return results


def _shares_secure_views(desired: DesiredConfig, _: list[PlanAction]) -> list[PolicyResult]:
    results: list[PolicyResult] = []
    for share in desired.shares:
        if not share.secure_views:
            results.append(
                PolicyResult(
                    policy_id="SHARES_SECURE_VIEWS",
                    severity="HIGH",
                    message=f"Share {share.name} must expose secure views only",
                )
            )
        for view in share.secure_views:
            if not view.upper().startswith("SECURE_"):
                results.append(
                    PolicyResult(
                        policy_id="SHARES_SECURE_VIEWS",
                        severity="HIGH",
                        message=f"Share {share.name} view {view} is not secure",
                    )
                )
    return results


BUILTIN_POLICIES = [
    Policy(
        policy_id="WAREHOUSE_AUTO_SUSPEND",
        description="Warehouses must auto suspend within 300 seconds",
        severity="HIGH",
        evaluator=_warehouse_auto_suspend,
    ),
    Policy(
        policy_id="NO_PUBLIC_GRANTS",
        description="No grants to PUBLIC except UTILS usage",
        severity="HIGH",
        evaluator=_no_public_grants,
    ),
    Policy(
        policy_id="PII_MASKING",
        description="PII-tagged columns must have masking policies",
        severity="MEDIUM",
        evaluator=_pii_masking,
    ),
    Policy(
        policy_id="WAREHOUSE_RESOURCE_MONITOR",
        description="Resource monitors required for large warehouses",
        severity="MEDIUM",
        evaluator=_resource_monitor_for_large,
    ),
    Policy(
        policy_id="SHARES_SECURE_VIEWS",
        description="Shares may only expose secure views",
        severity="HIGH",
        evaluator=_shares_secure_views,
    ),
]
