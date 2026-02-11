#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH=apps/api python -m unittest discover -s apps/api/tests -p "test_*.py"
