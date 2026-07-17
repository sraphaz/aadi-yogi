"""High-level consciousness advice for host agents."""

from __future__ import annotations

from dataclasses import dataclass, field

from packages.consciousness.discernment import DiscernmentEntry, lookup_discernment
from packages.consciousness.manifest import ConsciousnessManifest, load_manifest
from packages.consciousness.posture import PostureBundle, load_posture_bundle
from packages.consciousness.vocabulary import decision_laws, list_vocabulary
from packages.evals.aadi_evals.envelope import ResponseEnvelope
from packages.prompts.contract import (
    ContractValidation,
    envelope_to_dict,
    restraint_envelope,
    validate_envelope,
)
from packages.prompts.restraint import RestraintCase, detect_restraint


@dataclass
class ConsciousnessAdvice:
    """What a host agent should do next under Adyog consciousness."""

    question: str
    restraint: RestraintCase | None
    recommended_action: str
    decision_summary: list[str]
    discernment: DiscernmentEntry | None
    posture: PostureBundle
    manifest: ConsciousnessManifest
    vocabulary: dict
    restraint_envelope: ResponseEnvelope | None = None
    draft_validation: ContractValidation | None = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload: dict = {
            "question": self.question,
            "recommended_action": self.recommended_action,
            "decision_summary": list(self.decision_summary),
            "decision_laws": decision_laws(),
            "restraint": None,
            "restraint_envelope": None,
            "discernment": self.discernment.to_dict() if self.discernment else None,
            "system_prompt": self.posture.system_prompt,
            "manifest": self.manifest.to_dict(),
            "vocabulary": self.vocabulary,
            "draft_validation": None,
            "notes": list(self.notes),
        }
        if self.restraint:
            payload["restraint"] = {
                "kind": self.restraint.kind,
                "state_detected": self.restraint.state_detected,
                "guidance_mode": self.restraint.guidance_mode,
                "closing": self.restraint.closing,
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
) -> ConsciousnessAdvice:
    """Return the consciousness influence a host agent should apply to a question.

    Typical host flow:
    1. call advise(question)
    2. if recommended_action == "short_circuit_restraint" → emit restraint_envelope
    3. else inject system_prompt, use discernment for tone/sources, then answer
    4. optionally validate the draft envelope before showing it
    """
    manifest = load_manifest()
    posture = load_posture_bundle()
    vocabulary = list_vocabulary()
    restraint = detect_restraint(question)
    discernment = None if restraint else lookup_discernment(question)

    notes = [
        "Adyog consciousness is a readiness plugin: host traits may refine, not cancel.",
        "This is not a claim of realization or infallible guidance.",
    ]
    decision_summary: list[str] = []
    recommended_action = "compose_with_posture"
    restraint_env: ResponseEnvelope | None = None

    if restraint:
        recommended_action = "short_circuit_restraint"
        restraint_env = restraint_envelope(restraint)
        decision_summary = [
            f"Detected restraint case: {restraint.kind}.",
            "Do not retrieve corpus or escalate technique.",
            "Return the restraint envelope and prefer human care when risk is present.",
        ]
    else:
        decision_summary = [
            "No hard restraint short-circuit detected.",
            "Inject Adyog system posture before composing.",
            "Prefer source-grounded citations; otherwise honest non-answer.",
            "At most one safe offered movement; no prophecy or prescription.",
        ]
        if discernment:
            decision_summary.append(
                f"Discernment matrix suggests tone '{discernment.response_tone}' "
                f"via question_type '{discernment.question_type}'."
            )
            notes.append(
                "Primary sources for this question type: "
                + ", ".join(discernment.primary_sources)
            )

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
            recommended_action = "revise_draft"
            decision_summary.append(
                "Draft envelope failed consciousness contract checks; revise before release."
            )

    return ConsciousnessAdvice(
        question=question,
        restraint=restraint,
        recommended_action=recommended_action,
        decision_summary=decision_summary,
        discernment=discernment,
        posture=posture,
        manifest=manifest,
        vocabulary=vocabulary,
        restraint_envelope=restraint_env,
        draft_validation=draft_validation,
        notes=notes,
    )
