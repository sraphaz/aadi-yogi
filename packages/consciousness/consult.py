"""Consult the living foundation — guidance, not an app router."""

from __future__ import annotations

from dataclasses import dataclass, field

from packages.consciousness.discernment import DiscernmentEntry, lookup_discernment
from packages.consciousness.foundation import ConsciousnessFoundation, load_foundation
from packages.consciousness.manifest import ConsciousnessManifest, load_manifest


@dataclass
class ConsciousnessConsultation:
    """How Adyog orients a host agent for a situation — without fixed app outcomes."""

    situation: str
    foundation: ConsciousnessFoundation
    manifest: ConsciousnessManifest
    orientation: list[str]
    conduct_to_hold: list[str]
    discernment: DiscernmentEntry | None
    agent_preamble: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "situation": self.situation,
            "orientation": list(self.orientation),
            "conduct_to_hold": list(self.conduct_to_hold),
            "discernment": self.discernment.to_dict() if self.discernment else None,
            "agent_preamble": self.agent_preamble,
            "foundation": {
                "version": self.foundation.version,
                "what_it_is": self.foundation.what_it_is,
                "what_it_is_not": self.foundation.what_it_is_not,
                "conduct_principles": self.foundation.conduct_principles,
            },
            "manifest": {
                "version": self.manifest.version,
                "status": self.manifest.status,
                "approved_date": self.manifest.approved_date,
            },
            "notes": list(self.notes),
            "reminder": (
                "This is a basis of consciousness for conduct — not a script that "
                "turns the host agent into a guru, and not Darshan product rules."
            ),
        }


def consult(situation: str) -> ConsciousnessConsultation:
    """Orient a host agent from the living foundation for a concrete situation.

    The host still decides with its own craft. Adyog supplies the basis:
    what to hold, what not to become, how the sources want reality to be met.
    """
    foundation = load_foundation()
    manifest = load_manifest()
    discernment = lookup_discernment(situation)

    orientation = [
        "Carry Adyog as a basis of consciousness underneath the host's craft.",
        "Do not perform mysticism or guru speech in the repository.",
        "Prefer sincerity, non-coercion, and source humility over certainty display.",
    ]
    conduct = list(foundation.conduct_principles)
    notes = [
        "Foundation is living: deepen via sources and reviewed feedback, not self-authorization.",
        "Darshan response envelopes are one product expression of this basis — optional, not the install.",
    ]

    if discernment:
        orientation.append(
            f"From the discernment field ({discernment.question_type}): "
            f"hold tone '{discernment.response_tone}'."
        )
        orientation.append(
            "Avoid: " + "; ".join(discernment.avoid)
            if discernment.avoid
            else "Keep avoidances from the foundation."
        )
        notes.append(
            "Primary sources that may inform this situation: "
            + ", ".join(discernment.primary_sources)
        )
        for tip in discernment.safe_guidance:
            orientation.append(tip)

    return ConsciousnessConsultation(
        situation=situation.strip(),
        foundation=foundation,
        manifest=manifest,
        orientation=orientation,
        conduct_to_hold=conduct,
        discernment=discernment,
        agent_preamble=foundation.agent_preamble,
        notes=notes,
    )
