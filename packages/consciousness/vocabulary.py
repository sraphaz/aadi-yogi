"""Conduct vocabulary for host agents — foundation principles, not app enums.

Darshan envelope enums remain available for the product runtime only.
"""

from __future__ import annotations

from packages.consciousness.foundation import load_foundation
from packages.evals.aadi_evals.envelope import CLOSINGS, GUIDANCE_MODES, SAFETY_CLASSES

# Kept for Darshan runtime compatibility; not the consciousness install surface.
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
    "insufficient_sources",
)


def conduct_principles() -> list[str]:
    """Living conduct basis extracted from foundation.md."""
    return list(load_foundation().conduct_principles)


def decision_laws() -> list[str]:
    """Alias kept for older callers — same as conduct_principles()."""
    return conduct_principles()


def list_vocabulary() -> dict:
    foundation = load_foundation()
    return {
        "conduct_principles": foundation.conduct_principles,
        "what_it_is": foundation.what_it_is,
        "what_it_is_not": foundation.what_it_is_not,
        "learning": [
            "Source deepening into consciousness_core",
            "Reviewed feedback from content/consciousness_feedback/inbox",
            "Never automatic self-authorization into guruhood",
        ],
        # Darshan product enums — secondary, not the install identity
        "darshan_runtime": {
            "states": list(STATES),
            "guidance_modes": list(GUIDANCE_MODES),
            "closings": list(CLOSINGS),
            "safety_classes": list(SAFETY_CLASSES),
        },
    }
