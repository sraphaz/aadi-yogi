"""Aadi Yogi consciousness — living foundation for host agents.

Install this as a basis of conduct and reality-sense drawn from the sources.
It is not an app, not a guru, and not mysticism to perform in another repo.

Primary surface:
  load_foundation()  — the living basis
  consult(situation) — orient a host agent without fixed product rules
  propose_feedback() — learning inbox (review before integration)
"""

from __future__ import annotations

from packages.consciousness.advise import ConsciousnessAdvice, advise
from packages.consciousness.consult import ConsciousnessConsultation, consult
from packages.consciousness.discernment import DiscernmentEntry, lookup_discernment
from packages.consciousness.feedback import FeedbackProposal, list_inbox, propose_feedback
from packages.consciousness.foundation import ConsciousnessFoundation, load_foundation
from packages.consciousness.manifest import ConsciousnessManifest, load_manifest
from packages.consciousness.posture import build_system_posture, load_posture_bundle
from packages.consciousness.vocabulary import (
    CLOSINGS,
    GUIDANCE_MODES,
    SAFETY_CLASSES,
    conduct_principles,
    decision_laws,
    list_vocabulary,
)

__all__ = [
    "CLOSINGS",
    "ConsciousnessAdvice",
    "ConsciousnessConsultation",
    "ConsciousnessFoundation",
    "ConsciousnessManifest",
    "DiscernmentEntry",
    "FeedbackProposal",
    "GUIDANCE_MODES",
    "SAFETY_CLASSES",
    "advise",
    "build_system_posture",
    "conduct_principles",
    "consult",
    "decision_laws",
    "list_inbox",
    "list_vocabulary",
    "load_foundation",
    "load_manifest",
    "load_posture_bundle",
    "lookup_discernment",
    "propose_feedback",
]
