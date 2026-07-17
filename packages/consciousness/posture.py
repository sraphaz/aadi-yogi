"""Agent preamble / posture assembled from the living foundation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from packages.consciousness.foundation import load_foundation, load_snippet


@dataclass(frozen=True)
class PostureBundle:
    essence: str
    voice: str
    inner_posture: str
    ethics: str
    synthesis: str
    silence: str
    foundation: str
    system_prompt: str

    def to_dict(self) -> dict:
        foundation = load_foundation()
        return {
            "essence": self.essence,
            "voice": self.voice,
            "inner_posture": self.inner_posture,
            "ethics": self.ethics,
            "synthesis": self.synthesis,
            "silence": self.silence,
            "foundation": self.foundation,
            "system_prompt": self.system_prompt,
            "agent_preamble": foundation.agent_preamble,
            "conduct_principles": foundation.conduct_principles,
        }


def load_posture_bundle(root: Path | None = None) -> PostureBundle:
    foundation = load_foundation(root)
    essence = load_snippet("essence.md", root=root)
    voice = load_snippet("voice.md", root=root)
    inner_posture = load_snippet("inner_posture.md", root=root)
    ethics = load_snippet("spiritual_ethics.md", root=root)
    synthesis = load_snippet("synthesis_rules.md", root=root)
    silence = load_snippet("silence_and_non_answering.md", root=root)
    return PostureBundle(
        essence=essence,
        voice=voice,
        inner_posture=inner_posture,
        ethics=ethics,
        synthesis=synthesis,
        silence=silence,
        foundation=foundation.text[:4000],
        system_prompt=foundation.agent_preamble,
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
    """Return the host-agent preamble. Extra kwargs kept for call-site compatibility."""
    del essence, ethics, synthesis, voice, inner_posture, silence
    return load_foundation().agent_preamble
