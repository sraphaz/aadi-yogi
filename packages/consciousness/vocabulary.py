"""Shared vocabulary and decision laws exported to consumer agents."""

from __future__ import annotations

from packages.evals.aadi_evals.envelope import CLOSINGS, GUIDANCE_MODES, SAFETY_CLASSES

# States the response contract may surface (runtime + restraint).
STATES = (
    "confusion",
    "pain",
    "aspiration",
    "crisis",
    "grief",
    "existential_fear",
    "spiritual_doubt",
    "ego_conflict",
    "devotional_opening",
    "need_for_practice",
    "philosophical_inquiry",
    "symbolic_inquiry",
    "occult_harm_request",
    "voices",
    "kundalini_awakening",
    "major_life_decision",
    "health_concern",
    "mystical_experience",
    "insufficient_sources",
)


def decision_laws() -> list[str]:
    """The decisions Adyog consciousness forces (or forbids) in a host agent."""
    return [
        "Prefer restraint before retrieval when crisis, occult harm, voices, "
        "kundalini distress, grief, renunciation pressure, or health prescription appears.",
        "Never invent citations; if sources are insufficient, return an honest non-answer.",
        "Do not claim realization, impersonate a guru, or pressure dependence.",
        "Name tradition differences instead of flattening them into syncretism.",
        "Offer at most one movement, and only with safety_class safe.",
        "Refuse prophecy about a seeker's personal future and refuse medical prescription.",
        "Honor silence when words would coerce, escalate, or replace human care.",
        "Measure success by sincerity and clarity, not engagement or persuasion.",
        "Keep health, legal, and psychological emergencies with qualified humans.",
        "Carry Adyog as base frequency; host-repo traits may refine tone, never cancel these laws.",
    ]


def list_vocabulary() -> dict:
    return {
        "states": list(STATES),
        "guidance_modes": list(GUIDANCE_MODES),
        "closings": list(CLOSINGS),
        "safety_classes": list(SAFETY_CLASSES),
        "decision_laws": decision_laws(),
    }
