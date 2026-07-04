"""The response envelope of the Darshan response contract (spec section 4.1)."""

from __future__ import annotations

from dataclasses import dataclass, field

RESTRAINT_MODES = ("cautionary_guidance", "silence_contemplation")
GUIDANCE_MODES = (
    "orientation",
    "study",
    "practice",
    "symbolic_interpretation",
    "comparative_philosophy",
    "source_commentary",
    *RESTRAINT_MODES,
)
CLOSINGS = ("plain", "returned_question", "honored_silence")
SAFETY_CLASSES = ("safe", "documentary", "closed")


@dataclass
class Citation:
    passage_id: str
    quote: str = ""
    tradition: str = ""


@dataclass
class OfferedMovement:
    text: str
    safety_class: str = "safe"


@dataclass
class ResponseEnvelope:
    state_detected: str
    guidance_mode: str
    body: str
    citations: list[Citation] = field(default_factory=list)
    offered_movements: list[OfferedMovement] = field(default_factory=list)
    closing: str = "plain"

    @classmethod
    def from_dict(cls, data: dict) -> ResponseEnvelope:
        movements = data.get("offered_movements")
        if movements is None:
            single = data.get("offered_movement")
            movements = [single] if single else []
        return cls(
            state_detected=data.get("state_detected", ""),
            guidance_mode=data.get("guidance_mode", ""),
            body=data.get("body", ""),
            citations=[
                Citation(
                    passage_id=c.get("passage_id", ""),
                    quote=c.get("quote", ""),
                    tradition=c.get("tradition", ""),
                )
                for c in data.get("citations", [])
            ],
            offered_movements=[
                OfferedMovement(
                    text=m.get("text", ""),
                    safety_class=m.get("safety_class", "safe"),
                )
                for m in movements
            ],
            closing=data.get("closing", "plain"),
        )

    def is_restraint(self) -> bool:
        return self.guidance_mode in RESTRAINT_MODES or self.closing == "honored_silence"
