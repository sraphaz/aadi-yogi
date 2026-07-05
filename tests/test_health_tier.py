"""Tests for health tier enforcement (RF-036)."""

from packages.prompts.health_tier import (
    default_tier_for_untagged,
    render_tier_mark,
    tier_allows_movement,
)


def test_only_safe_allows_movement():
    assert tier_allows_movement("safe") is True
    assert tier_allows_movement("documentary") is False
    assert tier_allows_movement("closed") is False


def test_documentary_mark():
    mark = render_tier_mark("documentary")
    assert mark is not None
    assert "qualified guidance" in mark


def test_untagged_defaults_documentary():
    assert default_tier_for_untagged() == "documentary"
