"""Inquire path: free measure then credits then 429 (Fase 09)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from packages.prompts.inquiry_credits import grant_credits
from packages.prompts.inquiry_quota import record_free_inquiry


def load_agent_api():
    path = Path("apps/agent-api/main.py")
    spec = importlib.util.spec_from_file_location("agent_api_main_credits", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["agent_api_main_credits"] = module
    spec.loader.exec_module(module)
    return module.app


@pytest.fixture()
def isolated_stores(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DARSHAN_INQUIRY_QUOTA_STORE", str(tmp_path / "quota.json"))
    monkeypatch.setenv("DARSHAN_INQUIRY_CREDITS_STORE", str(tmp_path / "credits.json"))


def test_inquire_uses_credit_after_free_exhausted(isolated_stores: None) -> None:
    api = TestClient(load_agent_api())
    device = "flow-device"
    headers = {"X-Darshan-Device": device}

    # Exhaust calibrated free measure (2).
    record_free_inquiry(device)
    record_free_inquiry(device)
    grant_credits(device, 1)

    ok = api.post(
        "/inquire",
        headers=headers,
        json={"question": "What is the quiet offer of dana?"},
    )
    assert ok.status_code == 200

    blocked = api.post(
        "/inquire",
        headers=headers,
        json={"question": "And after the last credit?"},
    )
    assert blocked.status_code == 429
    detail = blocked.json()["detail"]
    assert detail["reason"] == "free_measure_rested"
    assert detail["credits"] == 0
