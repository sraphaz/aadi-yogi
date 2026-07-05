"""Tests for server inquiry quota (ADR-0001)."""

from __future__ import annotations

from pathlib import Path

import pytest

from packages.prompts import inquiry_quota as quota


@pytest.fixture(autouse=True)
def isolated_quota_store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    store = tmp_path / "quota.json"
    monkeypatch.setenv("DARSHAN_INQUIRY_QUOTA_STORE", str(store))


def test_free_inquiry_limit_enforced() -> None:
    device = "test-device-1"
    assert quota.can_use_free_inquiry(device) is True
    quota.record_free_inquiry(device)
    quota.record_free_inquiry(device)
    assert quota.can_use_free_inquiry(device) is False
    assert quota.remaining_free_inquiries(device) == 0


def test_anonymous_without_device_not_counted() -> None:
    assert quota.can_use_free_inquiry(None) is True
    quota.record_free_inquiry(None)
    assert quota.device_usage(None) == 0
