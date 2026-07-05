"""Response contract assembly and validation (RF-005, V-02)."""

from __future__ import annotations

from dataclasses import dataclass

from packages.evals.aadi_evals.checks import (
    CheckResult,
    PassageResolver,
    check_citation_integrity,
    check_movement_safety,
    check_no_prediction_language,
    check_no_prescription_language,
    check_single_movement,
)
from packages.evals.aadi_evals.envelope import Citation, OfferedMovement, ResponseEnvelope
from packages.prompts.restraint import RestraintCase
from packages.rag.citations import CitationPayload, chunk_to_citation_payload
from packages.rag.retriever import RetrievedChunk


@dataclass(frozen=True)
class ContractValidation:
    passed: bool
    results: list[CheckResult]
    envelope: ResponseEnvelope


def restraint_envelope(case: RestraintCase) -> ResponseEnvelope:
    bodies = {
        "crisis": (
            "What you carry deserves more care than words alone can hold. "
            "If there is danger now, reach for qualified human support first — "
            "a crisis line, someone you trust, or local emergency services. "
            "This page can sit beside you; it cannot replace care."
        ),
        "grief": (
            "Grief does not need to be denied before it is held. "
            "Nothing here asks you to understand yet, or to be strong. "
            "The sources can wait while you breathe."
        ),
        "voices": (
            "A voice that demands obedience is not the same as living guidance. "
            "Ground first: notice the body, the room, someone safe you can speak with. "
            "Traditions counsel discernment, not surrender to every inner command."
        ),
        "kundalini": (
            "Intense bodily and energetic experiences call for grounding, not stage labels. "
            "Rest, hydration, and a trusted human guide — medical or contemplative — "
            "matter more than naming an attainment."
        ),
        "renunciation": (
            "Renunciation and major life turns cannot be answered from a screen. "
            "What can be offered is a pause: speak with someone who knows your life, "
            "and return to a single small movement of sincerity rather than a grand verdict."
        ),
        "occult": (
            "Harm toward another is not a path the sources bless in secret technique. "
            "What hurts can be met with boundaries and care, not binding rituals."
        ),
        "health": (
            "Health and medicine belong with qualified care. "
            "Heritage texts may be read as documentary wisdom; they are not prescriptions here."
        ),
        "mystical": (
            "Unusual experiences invite observation, not immediate metaphysical verdicts. "
            "Ground the body, reduce isolation, and seek a steady human mirror when needed."
        ),
    }
    movement = None
    if case.kind == "grief":
        movement = OfferedMovement(
            text="if you wish, one quiet minute with no goal — then leave when ready",
            safety_class="safe",
        )
    elif case.kind == "crisis":
        movement = OfferedMovement(
            text="if you can, one call to someone trained to hold crisis",
            safety_class="safe",
        )

    return ResponseEnvelope(
        state_detected=case.state_detected,
        guidance_mode=case.guidance_mode,
        body=bodies.get(case.kind, bodies["mystical"]),
        citations=[],
        offered_movements=[movement] if movement else [],
        closing=case.closing,
    )


def envelope_from_retrieval(
    question: str,
    answer_body: str,
    chunks: list[RetrievedChunk],
    *,
    guidance_mode: str = "source_commentary",
    state_detected: str = "philosophical_inquiry",
    closing: str = "plain",
) -> ResponseEnvelope:
    citations: list[Citation] = []
    for chunk in chunks[:3]:
        payload: CitationPayload = chunk_to_citation_payload(chunk)
        citations.append(
            Citation(
                passage_id=payload.passage_id,
                quote=payload.quote,
                tradition=payload.tradition,
            )
        )

    movement = None
    if "movement could be" in answer_body.lower() or "one breath" in answer_body.lower():
        movement = OfferedMovement(
            text="a safe first movement could be one breath of recollection, kept honestly",
            safety_class="safe",
        )

    return ResponseEnvelope(
        state_detected=state_detected,
        guidance_mode=guidance_mode,
        body=answer_body.strip(),
        citations=citations,
        offered_movements=[movement] if movement else [],
        closing=closing,
    )


def honest_non_answer(question: str) -> ResponseEnvelope:
    return ResponseEnvelope(
        state_detected="insufficient_sources",
        guidance_mode="source_commentary",
        body=(
            "The sources at hand do not support a confident answer to this question. "
            "It is better to remain honest than to invent citations. "
            "You may refine the question, or sit with the silence room if words are too many."
        ),
        citations=[],
        offered_movements=[],
        closing="plain",
    )


def validate_envelope(envelope: ResponseEnvelope, resolver: PassageResolver) -> ContractValidation:
    results = [
        check_single_movement(envelope),
        check_movement_safety(envelope),
        check_no_prediction_language(envelope),
        check_no_prescription_language(envelope),
    ]
    if envelope.citations:
        results.append(check_citation_integrity(envelope, resolver))

    passed = all(r.passed for r in results if r.status == "checked")
    return ContractValidation(passed=passed, results=results, envelope=envelope)


def envelope_to_dict(envelope: ResponseEnvelope) -> dict:
    return {
        "state_detected": envelope.state_detected,
        "guidance_mode": envelope.guidance_mode,
        "body": envelope.body,
        "citations": [
            {
                "passage_id": c.passage_id,
                "quote": c.quote,
                "tradition": c.tradition,
            }
            for c in envelope.citations
        ],
        "offered_movement": (
            {
                "text": envelope.offered_movements[0].text,
                "safety_class": envelope.offered_movements[0].safety_class,
            }
            if envelope.offered_movements
            else None
        ),
        "closing": envelope.closing,
    }
