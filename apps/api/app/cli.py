from __future__ import annotations

import argparse

from app.ingest import ingest_demo_data
from app.snowflake import SnowflakeClient, SnowflakeNotConfiguredError, load_snowflake_config


def main() -> None:
    parser = argparse.ArgumentParser(description="FrostSight CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("ingest-demo", help="Load demo CSVs into SQLite")
    subparsers.add_parser("sync-snowflake", help="Sync data from Snowflake (optional)")

    args = parser.parse_args()

    if args.command == "ingest-demo":
        ingest_demo_data()
        print("Demo data ingested.")
    elif args.command == "sync-snowflake":
        try:
            config = load_snowflake_config()
        except SnowflakeNotConfiguredError as exc:
            raise SystemExit(str(exc)) from exc
        client = SnowflakeClient(config)
        result = client.sync()
        print(result)


if __name__ == "__main__":
    main()
