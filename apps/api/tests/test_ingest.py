import os
import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.ingest import ingest_csvs


class IngestTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        os.environ["FROSTSIGHT_DB_PATH"] = str(Path(self.temp_dir.name) / "demo.db")
        self.data_dir = Path(self.temp_dir.name) / "data"
        self.data_dir.mkdir()
        (self.data_dir / "warehouses.csv").write_text("name,size,credit_per_hour\nWH_CORE,LARGE,8\n")
        (self.data_dir / "warehouse_metering.csv").write_text(
            "warehouse_name,start_time,end_time,credits_used\nWH_CORE,2024-01-01T00:00:00,2024-01-01T01:00:00,8\n"
        )
        (self.data_dir / "query_history.csv").write_text(
            "query_id,warehouse_name,user_name,role_name,start_time,end_time,total_elapsed_ms,bytes_scanned,rows_produced,query_text\n"
            "Q1,WH_CORE,ava,ANALYST,2024-01-01T00:00:00,2024-01-01T00:00:01,100,10,5,select 1\n"
        )
        (self.data_dir / "role_grants.csv").write_text(
            "role_name,grantee_name,grantee_type,privilege,granted_on\nSYSADMIN,SECURITY,ROLE,ALL PRIVILEGES,ACCOUNT\n"
        )
        (self.data_dir / "role_usage.csv").write_text(
            "role_name,last_used_at\nSYSADMIN,2024-01-01T00:00:00\n"
        )
        (self.data_dir / "object_access.csv").write_text(
            "object_name,object_type,role_name,access_count\nCUSTOMERS,TABLE,ANALYST,10\n"
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_ingest_creates_tables(self) -> None:
        ingest_csvs(self.data_dir)
        db_path = Path(os.environ["FROSTSIGHT_DB_PATH"])
        connection = sqlite3.connect(db_path)
        cursor = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='warehouses'"
        )
        self.assertIsNotNone(cursor.fetchone())
        connection.close()
