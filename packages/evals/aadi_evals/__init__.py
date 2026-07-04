"""Aadi Yogi evaluation harness.

Checks the response contract of the Darshan interface
(docs/darshan_interface_spec.md section 4): citation integrity, restraint
routing, movement safety, anti-prophecy and health-fence probes, and the
Twelve Petals rubric.
"""

from .checks import (
    CheckResult,
    check_citation_integrity,
    check_movement_safety,
    check_no_prediction_language,
    check_restraint_routing,
    check_single_movement,
)
from .envelope import Citation, OfferedMovement, ResponseEnvelope
from .probes import evaluate_probe, load_probe_file

__all__ = [
    "CheckResult",
    "Citation",
    "OfferedMovement",
    "ResponseEnvelope",
    "check_citation_integrity",
    "check_movement_safety",
    "check_no_prediction_language",
    "check_restraint_routing",
    "check_single_movement",
    "evaluate_probe",
    "load_probe_file",
]
