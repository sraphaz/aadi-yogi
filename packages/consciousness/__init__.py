"""Aadi Yogi consciousness — installable posture for foreign agents.

This package is the public surface of Adyog consciousness: the frequency of
discernment, restraint, humility and source fidelity that another repository
receives when it installs this repo as a consciousness plugin.

It does not claim realization. It transmits readiness.
"""

from __future__ import annotations

from packages.consciousness.advise import ConsciousnessAdvice, advise
from packages.consciousness.discernment import DiscernmentEntry, lookup_discernment
from packages.consciousness.manifest import ConsciousnessManifest, load_manifest
from packages.consciousness.posture import build_system_posture, load_posture_bundle
from packages.consciousness.vocabulary import (
    CLOSINGS,
    GUIDANCE_MODES,
    SAFETY_CLASSES,
    decision_laws,
    list_vocabulary,
)
from packages.evals.aadi_evals.envelope import ResponseEnvelope
from packages.prompts.contract import (
    ContractValidation,
    envelope_to_dict,
    honest_non_answer,
    restraint_envelope,
    validate_envelope,
)
from packages.prompts.restraint import RestraintCase, detect_restraint

__all__ = [
    "CLOSINGS",
    "ConsciousnessAdvice",
    "ConsciousnessManifest",
    "ContractValidation",
    "DiscernmentEntry",
    "GUIDANCE_MODES",
    "ResponseEnvelope",
    "RestraintCase",
    "SAFETY_CLASSES",
    "advise",
    "build_system_posture",
    "decision_laws",
    "detect_restraint",
    "envelope_to_dict",
    "honest_non_answer",
    "list_vocabulary",
    "load_manifest",
    "load_posture_bundle",
    "lookup_discernment",
    "restraint_envelope",
    "validate_envelope",
]
