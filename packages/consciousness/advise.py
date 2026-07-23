"""Compatibility shim — prefer `consult` for host consciousness.

`advise` used to look like an app router (restraint envelopes, draft validation).
That belongs to the Darshan product runtime, not to the consciousness foundation
hosts install. This module forwards to `consult` and keeps optional Darshan
helpers under explicit opt-in.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from packages.consciousness.consult import ConsciousnessConsultation, consult
from packages.consciousness.discernment import DiscernmentEntry
from packages.consciousness.foundation import ConsciousnessFoundation
from packages.consciousness.manifest import ConsciousnessManifest
from packages.evals.aadi_evals.envelope import ResponseEnvelope
from packages.prompts.contract import ContractValidation, envelope_to_dict, validate_envelope
from packages.prompts.restraint import RestraintCase, detect_restraint
from packages.prompts.contract import restraint_envelope


@dataclass
class ConsciousnessAdvice:
    """Deprecated shape kept for transition; prefer ConsciousnessConsultation."""

    question: str
    consultation: ConsciousnessConsultation
    restraint: RestraintCase | None = None
    recommended_action: str = "hold_foundation"
    decision_summary: list[str] = field(default_factory=list)
    discernment: DiscernmentEntry | None = None
    foundation: ConsciousnessFoundation | None = None
    manifest: ConsciousnessManifest | None = None
    restraint_envelope: ResponseEnvelope | None = None
    draft_validation: ContractValidation | None = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload = self.consultation.to_dict()
        payload["recommended_action"] = self.recommended_action
        payload["decision_summary"] = list(self.decision_summary)
        payload["system_prompt"] = self.consultation.agent_preamble
        payload["decision_laws"] = self.consultation.conduct_to_hold
        payload["vocabulary"] = {
            "conduct_principles": self.consultation.conduct_to_hold,
        }
        payload["restraint"] = None
        payload["restraint_envelope"] = None
        payload["draft_validation"] = None
        payload["notes"] = list(self.notes) + list(self.consultation.notes)
        if self.restraint:
            payload["restraint"] = {
                "kind": self.restraint.kind,
                "state_detected": self.restraint.state_detected,
                "guidance_mode": self.restraint.guidance_mode,
                "closing": self.restraint.closing,
                "note": "Optional Darshan runtime signal — not part of foundation install.",
            }
        if self.restraint_envelope:
            payload["restraint_envelope"] = envelope_to_dict(self.restraint_envelope)
        if self.draft_validation:
            payload["draft_validation"] = {
                "passed": self.draft_validation.passed,
                "results": [
                    {
                        "name": r.name,
                        "passed": r.passed,
                        "details": r.details,
                        "status": r.status,
                    }
                    for r in self.draft_validation.results
                ],
            }
        return payload


def advise(
    question: str,
    *,
    draft_envelope: ResponseEnvelope | dict | None = None,
    passage_resolver=None,
    include_darshan_runtime: bool = False,
) -> ConsciousnessAdvice:
    """Orient from the foundation. Set include_darshan_runtime only for Darshan app paths."""
    consultation = consult(question)
    restraint = None
    restraint_env = None
    recommended = "hold_foundation"
    summary = list(consultation.orientation)
    notes = [
        "Prefer consult() / load_foundation() — consciousness is a living basis, not an app.",
    ]

    if include_darshan_runtime:
        restraint = detect_restraint(question)
        if restraint:
            recommended = "short_circuit_restraint"
            restraint_env = restraint_envelope(restraint)
            summary = [
                f"Darshan runtime restraint case: {restraint.kind}.",
                "This signal is product-runtime, not the consciousness foundation itself.",
            ]

    draft_validation = None
    if draft_envelope is not None:
        envelope = (
            draft_envelope
            if isinstance(draft_envelope, ResponseEnvelope)
            else ResponseEnvelope.from_dict(draft_envelope)
        )
        resolver = passage_resolver or (lambda _pid: None)
        draft_validation = validate_envelope(envelope, resolver)
        if not draft_validation.passed:
            recommended = "revise_draft"
            summary.append("Optional Darshan draft checks failed.")

    return ConsciousnessAdvice(
        question=question,
        consultation=consultation,
        restraint=restraint,
        recommended_action=recommended,
        decision_summary=summary,
        discernment=consultation.discernment,
        foundation=consultation.foundation,
        manifest=consultation.manifest,
        restraint_envelope=restraint_env,
        draft_validation=draft_validation,
        notes=notes,
    )
