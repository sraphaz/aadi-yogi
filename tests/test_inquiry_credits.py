"""Tests for inquiry credit ledger scaffold (ADR-0001 / Fase 09)."""

from __future__ import annotations

from pathlib import Path

import pytest

from packages.prompts import inquiry_credits as credits


@pytest.fixture(autouse=True)
def isolated_credits_store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    store = tmp_path / "credits.json"
    monkeypatch.setenv("DARSHAN_INQUIRY_CREDITS_STORE", str(store))
    monkeypatch.delenv("DARSHAN_ALLOW_DEV_CREDIT_GRANT", raising=False)


def test_grant_and_debit() -> None:
    device = "credit-device-1"
    assert credits.credit_balance(device) == 0
    assert credits.grant_credits(device, 2) == 2
    assert credits.can_use_credit(device) is True
    assert credits.debit_credit(device) == 1
    assert credits.debit_credit(device) == 0
    assert credits.can_use_credit(device) is False


def test_debit_without_balance_raises() -> None:
    with pytest.raises(ValueError, match="insufficient_credits"):
        credits.debit_credit("empty-device")


def test_dev_grant_gate() -> None:
    assert credits.dev_grant_allowed() is False
