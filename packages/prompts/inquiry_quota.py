"""Server-side free inquiry measure (ADR-0001) — complements device-local counter."""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

from packages.prompts.inquiry_policy import free_daily_limit

DEFAULT_STORE = Path(".tmp_inquiry_quota.json")


def quota_store_path() -> Path:
    return Path(os.environ.get("DARSHAN_INQUIRY_QUOTA_STORE", DEFAULT_STORE))


def _today() -> str:
    return date.today().isoformat()


def _load_store() -> dict:
    path = quota_store_path()
    if not path.exists():
        return {"date": _today(), "devices": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"date": _today(), "devices": {}}
    if data.get("date") != _today():
        return {"date": _today(), "devices": {}}
    devices = data.get("devices")
    if not isinstance(devices, dict):
        return {"date": _today(), "devices": {}}
    return {"date": _today(), "devices": devices}


def _save_store(store: dict) -> None:
    path = quota_store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(store, indent=2), encoding="utf-8")


def device_usage(device_id: str | None) -> int:
    if not device_id:
        return 0
    store = _load_store()
    return int(store["devices"].get(device_id, 0))


def remaining_free_inquiries(device_id: str | None) -> int | None:
    limit = free_daily_limit()
    if limit is None:
        return None
    return max(0, limit - device_usage(device_id))


def can_use_free_inquiry(device_id: str | None) -> bool:
    limit = free_daily_limit()
    if limit is None:
        return True
    return device_usage(device_id) < limit


def record_free_inquiry(device_id: str | None) -> int:
    if not device_id:
        return 0
    store = _load_store()
    count = int(store["devices"].get(device_id, 0)) + 1
    store["devices"][device_id] = count
    _save_store(store)
    return count
