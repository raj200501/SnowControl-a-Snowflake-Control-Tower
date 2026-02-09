from pathlib import Path

from snowcontrol.config.loader import load_config
from snowcontrol.core.diff import diff_state
from snowcontrol.core.policies.builtin import BUILTIN_POLICIES
from snowcontrol.core.policies.engine import evaluate_policies


def test_policy_violations_detected() -> None:
    desired = load_config(Path("examples/acme_account/desired.yaml"))
    desired.warehouses[0].auto_suspend = 600
    plan = diff_state({"resources": {}}, desired)
    results = evaluate_policies(desired, plan, BUILTIN_POLICIES, {"policies": {}})
    assert any(result.policy_id == "WAREHOUSE_AUTO_SUSPEND" for result in results)
