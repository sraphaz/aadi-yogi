"""Device-scoped inquiry credits (ADR-0001 / RF-039).

Scaffold only: balances live in a local JSON store. Payment rails (PIX etc.)
are not wired — grants are gated by DARSHAN_ALLOW_DEV_CREDIT_GRANT for demos.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULT_STORE = Path(".tmp_inquiry_credits.json")


def credits_store_path() -> Path:
    return Path(os.environ.get("DARSHAN_INQUIRY_CREDITS_STORE", DEFAULT_STORE))


def _load_store() -> dict:
    path = credits_store_path()
    if not path.exists():
        return {"devices": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"devices": {}}
    devices = data.get("devices")
    if not isinstance(devices, dict):
        return {"devices": {}}
    return {"devices": devices}


def _save_store(store: dict) -> None:
    path = credits_store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(store, indent=2), encoding="utf-8")


def credit_balance(device_id: str | None) -> int:
    if not device_id:
        return 0
    store = _load_store()
    return max(0, int(store["devices"].get(device_id, 0)))


def can_use_credit(device_id: str | None) -> bool:
    return credit_balance(device_id) > 0


def debit_credit(device_id: str | None) -> int:
    """Debit one credit. Returns remaining balance. Raises ValueError if none."""
    if not device_id:
        raise ValueError("device_required")
    store = _load_store()
    balance = int(store["devices"].get(device_id, 0))
    if balance < 1:
        raise ValueError("insufficient_credits")
    balance -= 1
    store["devices"][device_id] = balance
    _save_store(store)
    return balance


def grant_credits(device_id: str | None, amount: int) -> int:
    """Add credits (scaffold / creator grant). Returns new balance."""
    if not device_id:
        raise ValueError("device_required")
    if amount < 1:
        raise ValueError("amount_must_be_positive")
    if amount > 100:
        raise ValueError("amount_too_large")
    store = _load_store()
    balance = int(store["devices"].get(device_id, 0)) + amount
    store["devices"][device_id] = balance
    _save_store(store)
    return balance


def dev_grant_allowed() -> bool:
    return os.environ.get("DARSHAN_ALLOW_DEV_CREDIT_GRANT", "").strip() in {
        "1",
        "true",
        "yes",
    }
