from __future__ import annotations

from typing import Any

from snowcontrol.config.schema import DesiredConfig
from snowcontrol.core.models import ActionType, PlanAction

RESOURCE_MAP = {
    "warehouse": "warehouses",
    "database": "databases",
    "schema": "schemas",
    "role": "roles",
    "grant": "grants",
    "resource_monitor": "resource_monitors",
    "tag": "tags",
    "masking_policy": "masking_policies",
    "tag_attachment": "tag_attachments",
    "masking_attachment": "masking_attachments",
    "share": "shares",
}


def desired_to_state(desired: DesiredConfig) -> dict[str, dict[str, Any]]:
    return {
        "warehouse": {w.name: w.model_dump() for w in desired.warehouses},
        "database": {d.name: d.model_dump() for d in desired.databases},
        "schema": {f"{s.database}.{s.name}": s.model_dump() for s in desired.schemas},
        "role": {r.name: r.model_dump() for r in desired.roles},
        "grant": {
            f"{g.role}:{g.privilege}:{g.on_type}:{g.on_name}": g.model_dump()
            for g in desired.grants
        },
        "resource_monitor": {m.name: m.model_dump() for m in desired.resource_monitors},
        "tag": {t.name: t.model_dump() for t in desired.tags},
        "masking_policy": {m.name: m.model_dump() for m in desired.masking_policies},
        "tag_attachment": {
            f"{t.tag}:{t.object_type}:{t.object_name}": t.model_dump()
            for t in desired.tag_attachments
        },
        "masking_attachment": {
            f"{m.policy}:{m.object_type}:{m.object_name}": m.model_dump()
            for m in desired.masking_attachments
        },
        "share": {s.name: s.model_dump() for s in desired.shares},
    }


def diff_state(current: dict[str, Any], desired: DesiredConfig) -> list[PlanAction]:
    desired_state = desired_to_state(desired)
    current_resources: dict[str, dict[str, Any]] = current.get("resources", {})
    actions: list[PlanAction] = []
    create_action_map = {
        "grant": ActionType.GRANT,
        "tag_attachment": ActionType.ATTACH_TAG,
        "masking_attachment": ActionType.ATTACH_MASK,
    }
    drop_action_map = {
        "grant": ActionType.REVOKE,
        "tag_attachment": ActionType.DETACH_TAG,
        "masking_attachment": ActionType.DETACH_MASK,
    }
    for resource_type, desired_items in desired_state.items():
        current_items = current_resources.get(resource_type, {})
        for name, payload in desired_items.items():
            if name not in current_items:
                action_type = create_action_map.get(resource_type, ActionType.CREATE)
                actions.append(PlanAction(action_type, resource_type, name, payload))
            elif current_items[name] != payload:
                action_type = create_action_map.get(resource_type, ActionType.ALTER)
                actions.append(PlanAction(action_type, resource_type, name, payload))
        for name in current_items.keys() - desired_items.keys():
            action_type = drop_action_map.get(resource_type, ActionType.DROP)
            actions.append(PlanAction(action_type, resource_type, name, current_items[name]))
    return sorted(actions, key=lambda action: action.sort_key())
