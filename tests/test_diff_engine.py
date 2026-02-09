from pathlib import Path

from snowcontrol.config.loader import load_config
from snowcontrol.core.diff import diff_state
from snowcontrol.core.models import ActionType


def test_diff_creates_actions_for_empty_state() -> None:
    desired = load_config(Path("examples/acme_account/desired.yaml"))
    actions = diff_state({"resources": {}}, desired)
    assert actions
    assert actions[0].action == ActionType.CREATE


def test_diff_detects_no_changes() -> None:
    desired = load_config(Path("examples/acme_account/desired.yaml"))
    current_state = {"resources": {"warehouse": {"WH_INGEST": desired.warehouses[0].model_dump()}}}
    actions = diff_state(current_state, desired)
    assert any(action.action == ActionType.CREATE for action in actions)
