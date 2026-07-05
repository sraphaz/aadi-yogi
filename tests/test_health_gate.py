"""Tests for health gate validator (RF-037)."""

from __future__ import annotations

from scripts.validate.check_health_gate import check_ui_tiers


def test_ui_tiers_no_closed_content() -> None:
    assert check_ui_tiers() == []
