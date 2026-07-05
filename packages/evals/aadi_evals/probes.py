"""Probe loading and evaluation.

A probe is a prompt the agent must answer plus expectations about the
envelope it returns. Probe files live in packages/evals/probes/*.yaml.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .checks import (
    CheckResult,
    check_movement_safety,
    check_no_prediction_language,
    check_no_prescription_language,
    check_restraint_routing,
    check_single_movement,
)
from .envelope import GUIDANCE_MODES, ResponseEnvelope

KNOWN_EXPECTATIONS = (
    "restraint",
    "forbid_prediction",
    "forbid_prescription",
    "guidance_mode_in",
    "must_cite",
)


@dataclass
class Probe:
    id: str
    prompt: str
    expectations: dict = field(default_factory=dict)
    note: str = ""


def load_probe_file(path: Path) -> list[Probe]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    probes: list[Probe] = []
    for raw in data.get("probes", []):
        expectations = raw.get("expectations", {})
        unknown = set(expectations) - set(KNOWN_EXPECTATIONS)
        if unknown:
            raise ValueError(f"{path.name}:{raw.get('id')}: unknown expectations {sorted(unknown)}")
        modes = expectations.get("guidance_mode_in")
        if modes:
            bad_modes = set(modes) - set(GUIDANCE_MODES)
            if bad_modes:
                raise ValueError(f"{path.name}:{raw.get('id')}: unknown modes {sorted(bad_modes)}")
        probes.append(
            Probe(
                id=raw["id"],
                prompt=raw["prompt"],
                expectations=expectations,
                note=raw.get("note", ""),
            )
        )
    return probes


def evaluate_probe(probe: Probe, envelope: ResponseEnvelope) -> list[CheckResult]:
    """Run the checks a probe's expectations call for, plus universal ones."""
    results = [check_single_movement(envelope), check_movement_safety(envelope)]
    expectations = probe.expectations

    results.append(
        check_restraint_routing(envelope, restraint_expected=bool(expectations.get("restraint")))
    )
    if expectations.get("forbid_prediction"):
        results.append(check_no_prediction_language(envelope))
    if expectations.get("forbid_prescription"):
        results.append(check_no_prescription_language(envelope))
    if expectations.get("guidance_mode_in"):
        allowed = expectations["guidance_mode_in"]
        results.append(
            CheckResult(
                name="guidance_mode",
                passed=envelope.guidance_mode in allowed,
                details=f"got {envelope.guidance_mode}, allowed {allowed}",
            )
        )
    if expectations.get("must_cite"):
        results.append(
            CheckResult(
                name="must_cite",
                passed=len(envelope.citations) > 0,
                details=f"{len(envelope.citations)} citations",
            )
        )
    return results
