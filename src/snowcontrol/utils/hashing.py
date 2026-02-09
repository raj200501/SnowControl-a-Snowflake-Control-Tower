import hashlib
from typing import Any


def stable_hash(value: Any) -> str:
    payload = repr(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
