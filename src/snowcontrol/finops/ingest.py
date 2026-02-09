from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def filter_rows(rows: Iterable[dict[str, str]], **criteria: str) -> list[dict[str, str]]:
    filtered = []
    for row in rows:
        if all(row.get(key) == value for key, value in criteria.items()):
            filtered.append(row)
    return filtered
