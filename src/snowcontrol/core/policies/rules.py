from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from snowcontrol.config.schema import DesiredConfig
from snowcontrol.core.models import PlanAction


@dataclass(frozen=True)
class PolicyResult:
    policy_id: str
    severity: str
    message: str


@dataclass(frozen=True)
class Policy:
    policy_id: str
    description: str
    severity: str
    evaluator: Callable[[DesiredConfig, list[PlanAction]], list[PolicyResult]]
