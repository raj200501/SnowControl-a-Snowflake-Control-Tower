from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STATE_VERSION = 1


class LocalStateBackend:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"state_version": STATE_VERSION, "resources": {}}
        with self.path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if data.get("state_version") != STATE_VERSION:
            raise ValueError("Unsupported state version")
        return data

    def save(self, state: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)

    def apply(self, actions: list[dict[str, Any]]) -> dict[str, Any]:
        state = self.load()
        resources = state.setdefault("resources", {})
        for action in actions:
            action_type = action["action"]
            resource_type = action["resource_type"]
            name = action["name"]
            details = action["details"]
            bucket = resources.setdefault(resource_type, {})
            if action_type in {"CREATE", "ALTER", "GRANT", "ATTACH_TAG", "ATTACH_MASK"}:
                bucket[name] = details
            elif action_type in {"DROP", "REVOKE", "DETACH_TAG", "DETACH_MASK"}:
                bucket.pop(name, None)
        self.save(state)
        return state
