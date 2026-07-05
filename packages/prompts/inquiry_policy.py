"""Inquiry pricing policy from creator calibration (ADR-0001, RF-039)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

CALIBRATION_PATH = Path(__file__).resolve().parents[2] / "docs" / "calibrations" / "0001-dana.yaml"


@lru_cache(maxsize=1)
def load_dana_calibration() -> dict:
    if not CALIBRATION_PATH.exists():
        return {"status": "pending", "inquiry_pricing": {}, "dana": {}}
    with CALIBRATION_PATH.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def inquiry_policy() -> dict:
    cal = load_dana_calibration()
    pricing = cal.get("inquiry_pricing") or {}
    dana = cal.get("dana") or {}
    return {
        "status": cal.get("status", "pending"),
        "calibrated": cal.get("status") == "calibrated",
        "free_daily_inquiries": pricing.get("free_daily_inquiries"),
        "credit_unit_label": pricing.get("credit_unit_label"),
        "credit_price_brl": pricing.get("credit_price_brl"),
        "credit_price_usd": pricing.get("credit_price_usd"),
        "cost_anchor_note": pricing.get("cost_anchor_note"),
        "dana_quiet_page_url": dana.get("quiet_page_url", "/dana"),
        "payout_rails": dana.get("payout_rails") or [],
        "hard_boundaries": cal.get("hard_boundaries") or {},
    }


def free_daily_limit() -> int | None:
    policy = inquiry_policy()
    value = policy.get("free_daily_inquiries")
    if value is None:
        return None
    return int(value)
