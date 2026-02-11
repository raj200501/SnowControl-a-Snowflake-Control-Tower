import json
import os
import threading
import time
import unittest
import urllib.request
from http.server import HTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory

from app.ingest import ingest_demo_data
from app.main import run_server


class HealthEndpointTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = TemporaryDirectory()
        os.environ["FROSTSIGHT_DB_PATH"] = str(Path(cls.temp_dir.name) / "demo.db")
        ingest_demo_data()
        cls.server: HTTPServer = run_server("127.0.0.1", 0)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.thread.join(timeout=2)
        cls.temp_dir.cleanup()

    def test_health(self) -> None:
        url = f"http://127.0.0.1:{self.port}/api/v1/health"
        with urllib.request.urlopen(url) as response:
            payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(payload["status"], "ok")
