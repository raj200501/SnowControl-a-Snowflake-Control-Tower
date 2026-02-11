from __future__ import annotations

import os


def snowflake_status() -> dict:
    required = ["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER"]
    missing = [name for name in required if not os.getenv(name)]
    return {"configured": not missing, "missing": missing}
