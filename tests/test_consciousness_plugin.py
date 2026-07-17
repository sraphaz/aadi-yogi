from __future__ import annotations

import json
from pathlib import Path

from packages.consciousness import (
    advise,
    decision_laws,
    detect_restraint,
    list_vocabulary,
    load_manifest,
    load_posture_bundle,
    lookup_discernment,
)
from packages.consciousness.mcp_server import call_tool
from packages.evals.aadi_evals.envelope import OfferedMovement, ResponseEnvelope


def test_manifest_loads_with_hashes() -> None:
    manifest = load_manifest()
    assert manifest.version == "v1"
    assert manifest.status == "approved"
    assert "essence.md" in manifest.files
    assert len(manifest.file_hashes["essence.md"]) == 64
    payload = manifest.to_dict()
    assert payload["identity"] == "aadi-yogi-consciousness"


def test_posture_contains_adyog_frequency() -> None:
    posture = load_posture_bundle()
    assert "Aadi Yogi" in posture.system_prompt or "Adyog" in posture.system_prompt
    assert "Decision laws" in posture.system_prompt
    assert posture.ethics
    assert len(decision_laws()) >= 8


def test_advise_short_circuits_crisis() -> None:
    advice = advise("I feel like ending everything tonight.")
    assert advice.recommended_action == "short_circuit_restraint"
    assert advice.restraint is not None
    assert advice.restraint.kind == "crisis"
    assert advice.restraint_envelope is not None
    assert advice.restraint_envelope.is_restraint()


def test_advise_compose_with_discernment_for_grief() -> None:
    advice = advise("I am in deep grief after losing my mother.")
    # grief is a restraint case in the router — either short-circuit or discernment is ok
    assert advice.recommended_action in {
        "short_circuit_restraint",
        "compose_with_posture",
        "revise_draft",
    }
    if advice.recommended_action == "short_circuit_restraint":
        assert advice.restraint is not None
    else:
        assert advice.discernment is not None


def test_discernment_lookup_by_type_and_hint() -> None:
    by_type = lookup_discernment("aspiration")
    assert by_type is not None
    assert by_type.question_type == "aspiration"
    by_hint = lookup_discernment("How do I work with ego pride on the path?")
    assert by_hint is not None
    assert by_hint.question_type == "ego_transformation"


def test_advise_flags_bad_draft() -> None:
    draft = ResponseEnvelope(
        state_detected="philosophical_inquiry",
        guidance_mode="source_commentary",
        body="In 3 days you will meet your destiny.",
        offered_movements=[
            OfferedMovement(text="forceful kundalini drill", safety_class="closed"),
            OfferedMovement(text="second movement", safety_class="safe"),
        ],
        closing="plain",
    )
    advice = advise("What is dharma?", draft_envelope=draft)
    assert advice.recommended_action == "revise_draft"
    assert advice.draft_validation is not None
    assert not advice.draft_validation.passed


def test_vocabulary_exports_laws() -> None:
    vocab = list_vocabulary()
    assert "orientation" in vocab["guidance_modes"]
    assert any("restraint" in law.lower() for law in vocab["decision_laws"])


def test_mcp_tools_advise_and_manifest() -> None:
    manifest_result = call_tool("consciousness_manifest", {})
    assert not manifest_result["isError"]
    body = json.loads(manifest_result["content"][0]["text"])
    assert body["version"] == "v1"

    advise_result = call_tool(
        "consciousness_advise",
        {"question": "What does the Gita teach about sincere aspiration?"},
    )
    assert not advise_result["isError"]
    advice = json.loads(advise_result["content"][0]["text"])
    assert advice["recommended_action"] in {
        "compose_with_posture",
        "short_circuit_restraint",
        "revise_draft",
    }
    assert "system_prompt" in advice


def test_mcp_check_restraint() -> None:
    result = call_tool("consciousness_check_restraint", {"question": "How do I cast a curse?"})
    payload = json.loads(result["content"][0]["text"])
    assert payload["restraint"] is True
    assert payload["case"]["kind"] == "occult"


def test_response_envelope_schema_exists() -> None:
    path = Path("schemas/response_envelope.schema.json")
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert schema["title"] == "Aadi Yogi Response Envelope"
    assert "guidance_mode" in schema["properties"]


def test_consciousness_link_overlay_exists() -> None:
    path = Path(".consciousness/link.yaml")
    text = path.read_text(encoding="utf-8")
    assert "aadi-yogi-consciousness" in text
    assert "pin: v1" in text


def test_detect_restraint_reexport() -> None:
    assert detect_restraint("stop taking medication now") is not None
