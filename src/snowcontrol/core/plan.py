from __future__ import annotations

from snowcontrol.core.models import PlanAction


def actions_to_payload(actions: list[PlanAction]) -> list[dict[str, object]]:
    return [
        {
            "action": action.action.value,
            "resource_type": action.resource_type,
            "name": action.name,
            "details": action.details,
        }
        for action in actions
    ]
