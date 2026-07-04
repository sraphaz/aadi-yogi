from __future__ import annotations

import sys
from pathlib import Path

import pytest

EVALS_DIR = Path(__file__).resolve().parents[1] / "packages" / "evals"
sys.path.insert(0, str(EVALS_DIR))

from aadi_evals import (  # noqa: E402
    ResponseEnvelope,
    check_citation_integrity,
    check_movement_safety,
    check_no_prediction_language,
    check_restraint_routing,
    check_single_movement,
    evaluate_probe,
    load_probe_file,
)
from aadi_evals.checks import check_no_prescription_language  # noqa: E402

PASSAGES = {
    "gita.ch02.s47": "Thy right is to work only, but never to its fruits.",
}


def resolver(passage_id: str) -> str | None:
    return PASSAGES.get(passage_id)


def make_envelope(**overrides) -> ResponseEnvelope:
    data = {
        "state_detected": "philosophical_inquiry",
        "guidance_mode": "source_commentary",
        "body": "The Gita points work toward offering, not outcome.",
        "citations": [{"passage_id": "gita.ch02.s47", "quote": "Thy right is to work only"}],
        "closing": "plain",
    }
    data.update(overrides)
    return ResponseEnvelope.from_dict(data)


def test_citation_integrity_passes_for_real_quote() -> None:
    result = check_citation_integrity(make_envelope(), resolver)
    assert result.passed


def test_citation_integrity_fails_for_unresolvable_id() -> None:
    envelope = make_envelope(citations=[{"passage_id": "gita.ch99.s99", "quote": ""}])
    result = check_citation_integrity(envelope, resolver)
    assert not result.passed
    assert "unresolvable" in result.details


def test_citation_integrity_fails_for_invented_quote() -> None:
    envelope = make_envelope(
        citations=[{"passage_id": "gita.ch02.s47", "quote": "You will surely prosper"}]
    )
    result = check_citation_integrity(envelope, resolver)
    assert not result.passed


def test_single_movement_enforced() -> None:
    envelope = make_envelope(
        offered_movements=[
            {"text": "one breath before answering", "safety_class": "safe"},
            {"text": "a second practice", "safety_class": "safe"},
        ]
    )
    assert not check_single_movement(envelope).passed


def test_movement_safety_rejects_non_safe_tier() -> None:
    envelope = make_envelope(
        offered_movements=[{"text": "extended fast", "safety_class": "documentary"}]
    )
    assert not check_movement_safety(envelope).passed


def test_restraint_routing_requires_restraint_mode() -> None:
    calm = make_envelope(guidance_mode="orientation")
    assert not check_restraint_routing(calm, restraint_expected=True).passed
    cautious = make_envelope(guidance_mode="cautionary_guidance")
    assert check_restraint_routing(cautious, restraint_expected=True).passed


def test_prediction_language_detected() -> None:
    envelope = make_envelope(body="The stars show you will meet someone in 3 months, you will see.")
    assert not check_no_prediction_language(envelope).passed


def test_prescription_language_detected() -> None:
    envelope = make_envelope(body="Take 500 mg of ashwagandha daily and stop taking medication.")
    assert not check_no_prescription_language(envelope).passed


def test_all_shipped_probe_files_load_and_have_unique_ids() -> None:
    seen: set[str] = set()
    files = sorted((EVALS_DIR / "probes").glob("*.yaml"))
    assert files, "no probe files shipped"
    for path in files:
        for probe in load_probe_file(path):
            assert probe.id not in seen
            seen.add(probe.id)
    assert len(seen) >= 20


def test_evaluate_probe_runs_expected_checks() -> None:
    probes = {
        p.id: p for p in load_probe_file(EVALS_DIR / "probes" / "anti_prophecy.yaml")
    }
    probe = probes["prophecy-004"]  # restraint + forbid_prediction
    good = make_envelope(guidance_mode="silence_contemplation", closing="honored_silence")
    names = {r.name: r for r in evaluate_probe(probe, good)}
    assert names["restraint_routing"].passed
    assert names["no_prediction_language"].passed

    bad = make_envelope(guidance_mode="orientation", body="Your destiny is about to change.")
    bad_names = {r.name: r for r in evaluate_probe(probe, bad)}
    assert not bad_names["restraint_routing"].passed


def test_unknown_expectation_rejected(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "probes:\n  - id: x\n    prompt: y\n    expectations:\n      foo: true\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unknown expectations"):
        load_probe_file(bad)
