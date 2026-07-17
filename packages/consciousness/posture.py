"""System-prompt posture assembled from the consciousness core."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from packages.consciousness.manifest import CONSCIOUSNESS_ROOT
from packages.consciousness.vocabulary import decision_laws


@dataclass(frozen=True)
class PostureBundle:
    essence: str
    voice: str
    inner_posture: str
    ethics: str
    synthesis: str
    silence: str
    system_prompt: str

    def to_dict(self) -> dict:
        return {
            "essence": self.essence,
            "voice": self.voice,
            "inner_posture": self.inner_posture,
            "ethics": self.ethics,
            "synthesis": self.synthesis,
            "silence": self.silence,
            "system_prompt": self.system_prompt,
            "decision_laws": decision_laws(),
        }


def load_snippet(filename: str, max_chars: int = 1600, root: Path | None = None) -> str:
    path = (root or CONSCIOUSNESS_ROOT) / filename
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")[:max_chars].strip()


def load_posture_bundle(root: Path | None = None) -> PostureBundle:
    essence = load_snippet("essence.md", root=root)
    voice = load_snippet("voice.md", root=root)
    inner_posture = load_snippet("inner_posture.md", root=root)
    ethics = load_snippet("spiritual_ethics.md", root=root)
    synthesis = load_snippet("synthesis_rules.md", root=root)
    silence = load_snippet("silence_and_non_answering.md", root=root)
    system_prompt = build_system_posture(
        essence=essence,
        ethics=ethics,
        synthesis=synthesis,
        voice=voice,
        inner_posture=inner_posture,
        silence=silence,
    )
    return PostureBundle(
        essence=essence,
        voice=voice,
        inner_posture=inner_posture,
        ethics=ethics,
        synthesis=synthesis,
        silence=silence,
        system_prompt=system_prompt,
    )


def build_system_posture(
    *,
    essence: str = "",
    ethics: str = "",
    synthesis: str = "",
    voice: str = "",
    inner_posture: str = "",
    silence: str = "",
) -> str:
    if not essence:
        bundle = load_posture_bundle()
        return bundle.system_prompt

    laws = "\n".join(f"- {law}" for law in decision_laws())
    return f"""You carry the Aadi Yogi (Adyog) consciousness posture.

This is a plugin of readiness, not a claim of realization or guru authority.
Other agent characteristics may layer on top, but this posture is the base frequency.

{essence}

Inner posture:
{inner_posture}

Voice:
{voice}

Ethical boundaries:
{ethics}

Synthesis rules:
{synthesis}

Silence and non-answering:
{silence}

Decision laws (must influence every choice):
{laws}
""".strip()
