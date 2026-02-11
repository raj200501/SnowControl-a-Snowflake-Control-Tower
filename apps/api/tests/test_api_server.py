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


class APIServerTestCase(unittest.TestCase):
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

    def _get(self, path: str, auth: bool = True) -> dict:
        url = f"http://127.0.0.1:{self.port}{path}"
        request = urllib.request.Request(url)
        if auth:
            request.add_header("Authorization", "Bearer local-dev-token")
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))

    def test_health(self) -> None:
        data = self._get("/api/v1/health", auth=False)
        self.assertEqual(data["status"], "ok")

    def test_overview(self) -> None:
        data = self._get("/api/v1/overview")
        self.assertIn("credits_today", data)
        self.assertIn("p95_latency_today_ms", data)

    def test_queries(self) -> None:
        data = self._get("/api/v1/queries?limit=5")
        self.assertEqual(len(data), 5)

    def test_anomalies(self) -> None:
        data = self._get("/api/v1/anomalies")
        self.assertIsInstance(data, list)

    def test_governance(self) -> None:
        data = self._get("/api/v1/governance/findings")
        self.assertIsInstance(data, list)
