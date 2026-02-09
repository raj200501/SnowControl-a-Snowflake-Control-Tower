from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ActionType(str, Enum):
    CREATE = "CREATE"
    ALTER = "ALTER"
    DROP = "DROP"
    GRANT = "GRANT"
    REVOKE = "REVOKE"
    ATTACH_TAG = "ATTACH_TAG"
    DETACH_TAG = "DETACH_TAG"
    ATTACH_MASK = "ATTACH_MASK"
    DETACH_MASK = "DETACH_MASK"


@dataclass(frozen=True)
class PlanAction:
    action: ActionType
    resource_type: str
    name: str
    details: dict[str, Any]

    def sort_key(self) -> tuple[str, str, str]:
        return (self.resource_type, self.name, self.action.value)
