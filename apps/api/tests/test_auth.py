import json
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory

import os

from app.ingest import ingest_demo_data
from app.main import run_server


class AuthTestCase(unittest.TestCase):
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

    def test_requires_auth(self) -> None:
        url = f"http://127.0.0.1:{self.port}/api/v1/overview"
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(url)
        self.assertEqual(ctx.exception.code, 401)

    def test_accepts_auth(self) -> None:
        url = f"http://127.0.0.1:{self.port}/api/v1/overview"
        request = urllib.request.Request(url)
        request.add_header("Authorization", "Bearer local-dev-token")
        with urllib.request.urlopen(request) as response:
            payload = json.loads(response.read().decode("utf-8"))
        self.assertIn("credits_today", payload)
