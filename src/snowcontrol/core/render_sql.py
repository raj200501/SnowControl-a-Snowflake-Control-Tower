from __future__ import annotations

from snowcontrol.core.models import ActionType, PlanAction


def render_action(action: PlanAction) -> str:
    name = action.name
    details = action.details
    if action.resource_type == "warehouse":
        if action.action in {ActionType.CREATE, ActionType.ALTER}:
            return (
                "{verb} WAREHOUSE {name} WITH WAREHOUSE_SIZE = {size} "
                "AUTO_SUSPEND = {auto_suspend} AUTO_RESUME = {auto_resume} "
                "SCALING_POLICY = {scaling_policy} MAX_CLUSTER_COUNT = {max_cluster_count};"
            ).format(
                verb=action.action.value,
                name=details["name"],
                size=details["size"],
                auto_suspend=details["auto_suspend"],
                auto_resume="TRUE" if details["auto_resume"] else "FALSE",
                scaling_policy=details["scaling_policy"],
                max_cluster_count=details["max_cluster_count"],
            )
        return f"DROP WAREHOUSE {name};"
    if action.resource_type == "database":
        return (
            f"{action.action.value} DATABASE {name};"
            if action.action != ActionType.DROP
            else f"DROP DATABASE {name};"
        )
    if action.resource_type == "schema":
        db, schema = name.split(".", 1)
        if action.action == ActionType.DROP:
            return f"DROP SCHEMA {db}.{schema};"
        return f"{action.action.value} SCHEMA {db}.{schema};"
    if action.resource_type == "role":
        if action.action == ActionType.DROP:
            return f"DROP ROLE {name};"
        return f"{action.action.value} ROLE {name};"
    if action.resource_type == "grant":
        if action.action == ActionType.REVOKE:
            return (
                "REVOKE {privilege} ON {on_type} {on_name} FROM ROLE {role};"
            ).format(**details)
        return (
            "GRANT {privilege} ON {on_type} {on_name} TO ROLE {role};"
        ).format(**details)
    if action.resource_type == "resource_monitor":
        if action.action == ActionType.DROP:
            return f"DROP RESOURCE MONITOR {name};"
        return (
            "{verb} RESOURCE MONITOR {name} WITH CREDIT_QUOTA = {credit_quota} "
            "FREQUENCY = {frequency};"
        ).format(
            verb=action.action.value,
            name=name,
            credit_quota=details["credit_quota"],
            frequency=details["frequency"],
        )
    if action.resource_type == "tag":
        if action.action == ActionType.DROP:
            return f"DROP TAG {name};"
        return f"{action.action.value} TAG {name};"
    if action.resource_type == "masking_policy":
        if action.action == ActionType.DROP:
            return f"DROP MASKING POLICY {name};"
        return (
            "{verb} MASKING POLICY {name} AS (val string) RETURN {expression};"
        ).format(verb=action.action.value, name=name, expression=details["expression"])
    if action.resource_type == "tag_attachment":
        if action.action == ActionType.DETACH_TAG:
            return (
                "UNSET TAG {tag} ON {object_type} {object_name};"
            ).format(**details)
        return (
            "SET TAG {tag} = '{value}' ON {object_type} {object_name};"
        ).format(**details)
    if action.resource_type == "masking_attachment":
        if action.action == ActionType.DETACH_MASK:
            return (
                "UNSET MASKING POLICY {policy} ON {object_type} {object_name};"
            ).format(**details)
        return (
            "SET MASKING POLICY {policy} ON {object_type} {object_name};"
        ).format(**details)
    if action.resource_type == "share":
        if action.action == ActionType.DROP:
            return f"DROP SHARE {name};"
        accounts = ", ".join(details["accounts"])
        views = ", ".join(details["secure_views"])
        return (
            f"{action.action.value} SHARE {name} WITH ACCOUNTS = ({accounts}) "
            f"SECURE_VIEWS = ({views});"
        )
    raise ValueError(f"Unsupported resource type: {action.resource_type}")


def render_plan(actions: list[PlanAction]) -> str:
    if not actions:
        return "-- No changes.\n"
    return "\n".join(render_action(action) for action in actions) + "\n"
