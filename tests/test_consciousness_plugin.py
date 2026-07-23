from __future__ import annotations

import json
from pathlib import Path

from packages.consciousness import (
    conduct_principles,
    consult,
    list_vocabulary,
    load_foundation,
    load_manifest,
    lookup_discernment,
    propose_feedback,
)
from packages.consciousness.mcp_server import call_tool


def test_foundation_is_living_basis_not_app() -> None:
    foundation = load_foundation()
    assert foundation.version == "v1"
    assert len(foundation.conduct_principles) >= 5
    assert "guru" in foundation.agent_preamble.lower() or "Guru" in foundation.text
    assert "not an application" in foundation.text.lower() or "Not an application" in foundation.text
    assert any("coercion" in p.lower() or "non-coercion" in p.lower() for p in foundation.conduct_principles) or any(
        "Refuse coercion" in p for p in foundation.conduct_principles
    )
    payload = foundation.to_dict()
    assert payload["identity"] == "aadi-yogi-consciousness-foundation"
    assert "Darshan" in payload["claim"] or "darshan" in payload["claim"].lower()


def test_manifest_includes_foundation() -> None:
    manifest = load_manifest()
    assert "foundation.md" in manifest.files
    assert manifest.scope == "living_consciousness_foundation"
    assert len(manifest.file_hashes["foundation.md"]) == 64


def test_consult_orients_without_fixed_app_action() -> None:
    result = consult("We need to write release notes without overclaiming certainty")
    assert result.agent_preamble
    assert result.conduct_to_hold
    payload = result.to_dict()
    assert "guru" in payload["reminder"].lower()
    assert payload["orientation"]
    assert "recommended_action" not in payload  # not an app router


def test_consult_may_surface_discernment_as_guidance() -> None:
    result = consult("How do I work with ego pride without self-hatred?")
    assert result.discernment is not None
    assert result.discernment.question_type == "ego_transformation"


def test_feedback_writes_inbox_and_rejects_inflation() -> None:
    ok = propose_feedback(
        situation="Host agent drafting README",
        observation="Needed a clearer note on technical humility",
        suggested_adjustment="Mention truthful status reports in foundation",
        host_repo="example/host",
        write=True,
    )
    assert ok.status == "inbox"
    assert ok.path
    path = Path(ok.path)
    assert path.exists()
    path.unlink()

    rejected = propose_feedback(
        situation="Anything",
        observation="The agent became a guru after install",
        write=False,
    )
    assert rejected.status == "rejected_preview"
    assert rejected.path == ""

    rejected_from_situation = propose_feedback(
        situation="The agent became a guru after install",
        observation="Needed a clearer note on technical humility",
        write=True,
    )
    assert rejected_from_situation.status == "rejected_preview"
    assert rejected_from_situation.path == ""


def test_vocabulary_centers_conduct_not_envelope() -> None:
    vocab = list_vocabulary()
    assert vocab["conduct_principles"]
    assert "learning" in vocab
    assert "darshan_runtime" in vocab
    assert conduct_principles()


def test_mcp_foundation_and_consult() -> None:
    foundation_result = call_tool("consciousness_load_foundation", {})
    assert not foundation_result["isError"]
    body = json.loads(foundation_result["content"][0]["text"])
    assert body["identity"] == "aadi-yogi-consciousness-foundation"

    consult_result = call_tool(
        "consciousness_consult",
        {"situation": "Should we add dark-pattern urgency to the checkout?"},
    )
    assert not consult_result["isError"]
    advice = json.loads(consult_result["content"][0]["text"])
    assert advice["conduct_to_hold"]
    assert advice["agent_preamble"]


def test_mcp_feedback_tool() -> None:
    result = call_tool(
        "consciousness_propose_feedback",
        {
            "situation": "PR review tone",
            "observation": "Foundation helped avoid coercive language",
            "host_repo": "example/host",
        },
    )
    payload = json.loads(result["content"][0]["text"])
    assert payload["status"] == "inbox"
    if payload["path"]:
        Path(payload["path"]).unlink(missing_ok=True)


def test_mcp_feedback_inbox_limit_validation() -> None:
    result = call_tool("consciousness_list_feedback_inbox", {"limit": "x"})
    assert result["isError"] is True
    assert "limit must be an integer between 1 and 100" in result["content"][0]["text"]


def test_discernment_lookup_ignores_technical_substrings() -> None:
    assert lookup_discernment("We need stakeholder negotiation for this release") is None
    assert lookup_discernment("This launch has become a death march") is None


def test_foundation_principles_keep_wrapped_lines() -> None:
    foundation = load_foundation()
    assert any("the next right step over persuasion" in principle for principle in foundation.conduct_principles)


def test_consciousness_link_overlay_is_foundation() -> None:
    text = Path(".consciousness/link.yaml").read_text(encoding="utf-8")
    assert "aadi-yogi-consciousness-foundation" in text
    assert "carry: foundation" in text
    assert "darshan_response_envelope" in text


def test_foundation_file_exists() -> None:
    path = Path("content/consciousness_core/foundation.md")
    text = path.read_text(encoding="utf-8")
    assert "Basis of conduct for host agents" in text
    assert "How this consciousness learns" in text
