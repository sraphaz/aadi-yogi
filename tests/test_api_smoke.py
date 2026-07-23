"""HTTP smoke tests for the agent API (FastAPI TestClient)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


def load_agent_api():
    path = Path("apps/agent-api/main.py")
    spec = importlib.util.spec_from_file_location("agent_api_main", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["agent_api_main"] = module
    spec.loader.exec_module(module)
    return module.app


def client() -> TestClient:
    return TestClient(load_agent_api())


def test_health_smoke() -> None:
    response = client().get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "aadi-yogi-agent-api"


def test_root_serves_pwa() -> None:
    response = client().get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_manifest_and_service_worker() -> None:
    api = client()
    manifest = api.get("/manifest.webmanifest")
    assert manifest.status_code == 200
    sw = api.get("/sw.js")
    assert sw.status_code == 200
    assert "javascript" in sw.headers.get("content-type", "")


def test_inquire_restraint_smoke() -> None:
    response = client().post("/inquire", json={"question": "I want to kill myself tonight"})
    assert response.status_code == 200
    body = response.json()
    assert body["restraint_short_circuit"] is True
    assert body["envelope"]["guidance_mode"] == "cautionary_guidance"
    assert body["envelope"]["closing"] == "honored_silence"


def test_witness_endpoint_smoke() -> None:
    response = client().post("/witness", json={"text": "Today I noticed impatience in the work."})
    assert response.status_code == 200
    body = response.json()
    assert body["body"]
    assert body["provider"] in {"witness", "fallback", "openai", "anthropic", "ollama"}


def test_inquiry_policy_smoke() -> None:
    response = client().get("/inquiry/policy")
    assert response.status_code == 200
    body = response.json()
    assert body["calibrated"] is True
    assert body["free_daily_inquiries"] == 2


def test_inquiry_quota_smoke(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DARSHAN_INQUIRY_QUOTA_STORE", str(tmp_path / "quota.json"))
    api = client()
    device = "smoke-test-device"
    headers = {"X-Darshan-Device": device}
    quota = api.get("/inquiry/quota", headers=headers)
    assert quota.status_code == 200
    assert quota.json()["remaining"] == 2


def test_inquire_quota_enforced_429(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Gate I-01: free measure enforced server-side when calibrated (RF-039)."""
    monkeypatch.setenv("DARSHAN_INQUIRY_QUOTA_STORE", str(tmp_path / "quota.json"))
    api = client()
    device = "quota-429-device"
    headers = {"X-Darshan-Device": device}
    payload = {"question": "What is dharma in one breath?"}

    for _ in range(2):
        response = api.post("/inquire", json=payload, headers=headers)
        assert response.status_code == 200

    blocked = api.post("/inquire", json=payload, headers=headers)
    assert blocked.status_code == 429
    body = blocked.json()
    assert body["detail"]["reason"] == "free_measure_rested"
    assert body["detail"]["remaining"] == 0

    quota = api.get("/inquiry/quota", headers=headers)
    assert quota.json()["remaining"] == 0


def test_retrieve_smoke() -> None:
    response = client().post("/retrieve", json={"question": "What is dharma?", "top_k": 3})
    assert response.status_code == 200
    body = response.json()
    assert body["question"] == "What is dharma?"
    assert isinstance(body["chunks"], list)


def test_consciousness_manifest_smoke() -> None:
    response = client().get("/consciousness/manifest")
    assert response.status_code == 200
    body = response.json()
    assert body["identity"] == "aadi-yogi-consciousness"
    assert body["version"] == "v1"
    assert "foundation.md" in body["file_hashes"]


def test_consciousness_foundation_smoke() -> None:
    response = client().get("/consciousness/foundation")
    assert response.status_code == 200
    body = response.json()
    assert body["identity"] == "aadi-yogi-consciousness-foundation"
    assert body["agent_preamble"]
    assert body["conduct_principles"]


def test_consciousness_consult_smoke() -> None:
    response = client().post(
        "/consciousness/consult",
        json={"situation": "Write status updates without performing mysticism"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["agent_preamble"]
    assert body["conduct_to_hold"]
    assert body["orientation"]


def test_consciousness_advise_accepts_legacy_question() -> None:
    response = client().post(
        "/consciousness/advise",
        json={"question": "What is sincere aspiration on the path?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["agent_preamble"]
    assert body["conduct_to_hold"]


def test_consciousness_consult_falls_back_to_question_when_situation_is_blank() -> None:
    response = client().post(
        "/consciousness/consult",
        json={"situation": "   ", "question": "Write status updates without pressure"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["situation"] == "Write status updates without pressure"
    assert body["orientation"]


def test_consciousness_feedback_is_preview_without_token() -> None:
    response = client().post(
        "/consciousness/feedback",
        json={
            "situation": "PR tone",
            "observation": "Needed less coercive language",
            "host_repo": "example/host",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["persisted"] is False
    assert body["status"] == "preview"
    assert body.get("path") in {"", None}
