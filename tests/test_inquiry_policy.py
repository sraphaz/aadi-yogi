"""Tests for inquiry policy loader (ADR-0001)."""

from packages.prompts.inquiry_policy import free_daily_limit, inquiry_policy, load_dana_calibration


def test_calibration_loaded() -> None:
    cal = load_dana_calibration()
    assert cal.get("status") == "calibrated"


def test_inquiry_policy_has_free_measure() -> None:
    policy = inquiry_policy()
    assert policy["calibrated"] is True
    assert policy["free_daily_inquiries"] == 2
    assert policy["credit_price_brl"] == 1.0


def test_free_daily_limit() -> None:
    assert free_daily_limit() == 2
