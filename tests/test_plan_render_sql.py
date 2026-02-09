from snowcontrol.core.models import ActionType, PlanAction
from snowcontrol.core.render_sql import render_plan


def test_render_sql_for_warehouse_and_share() -> None:
    actions = [
        PlanAction(
            ActionType.CREATE,
            "warehouse",
            "WH_INGEST",
            {
                "name": "WH_INGEST",
                "size": "MEDIUM",
                "auto_suspend": 300,
                "auto_resume": True,
                "scaling_policy": "STANDARD",
                "max_cluster_count": 2,
            },
        ),
        PlanAction(
            ActionType.CREATE,
            "share",
            "SHARE_SALES",
            {"name": "SHARE_SALES", "accounts": ["ACME"], "secure_views": ["SECURE_VW"]},
        ),
    ]
    sql = render_plan(actions)
    assert "CREATE WAREHOUSE" in sql
    assert "CREATE SHARE SHARE_SALES" in sql
