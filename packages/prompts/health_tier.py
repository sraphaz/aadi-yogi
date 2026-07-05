"""Health content tier helpers (RF-036)."""

from __future__ import annotations

TIERS = ("safe", "documentary", "closed")

DOCUMENTARY_MARK = (
    "practiced traditionally under qualified guidance; "
    "Darshan does not instruct this."
)


def tier_allows_movement(tier: str) -> bool:
    return tier == "safe"


def render_tier_mark(tier: str) -> str | None:
    if tier == "documentary":
        return DOCUMENTARY_MARK
    if tier == "closed":
        return "closed by design — routes to qualified care"
    return None


def default_tier_for_untagged() -> str:
    return "documentary"
