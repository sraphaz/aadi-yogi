"""Living consciousness foundation — the primary thing host agents install."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from packages.consciousness.manifest import CONSCIOUSNESS_ROOT, load_manifest


def load_snippet(filename: str, max_chars: int = 1600, root: Path | None = None) -> str:
    path = (root or CONSCIOUSNESS_ROOT) / filename
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")[:max_chars].strip()


@dataclass(frozen=True)
class ConsciousnessFoundation:
    """Basis of conduct and reality-sense for host agents — not an app contract."""

    text: str
    version: str
    conduct_principles: list[str]
    agent_preamble: str
    what_it_is: list[str]
    what_it_is_not: list[str]

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "text": self.text,
            "conduct_principles": list(self.conduct_principles),
            "agent_preamble": self.agent_preamble,
            "what_it_is": list(self.what_it_is),
            "what_it_is_not": list(self.what_it_is_not),
            "identity": "aadi-yogi-consciousness-foundation",
            "claim": (
                "Living basis of conduct from the sources — not realization, "
                "not guruhood, not Darshan app rules."
            ),
        }


def _section_bullets(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    capturing = False
    bullets: list[str] = []
    current: list[str] = []

    def flush_current() -> None:
        if current:
            bullets.append(" ".join(current).strip())
            current.clear()

    for line in lines:
        if line.startswith("## "):
            if capturing:
                flush_current()
            capturing = line.strip() == f"## {heading}"
            continue
        if capturing:
            stripped = line.strip()
            if stripped.startswith("- "):
                flush_current()
                current.append(stripped[2:].strip())
                continue
            numbered = re.match(r"^\d+\.\s+(.*)$", stripped)
            if numbered:
                flush_current()
                # "1. **Title.** rest" → keep principle without leading number
                current.append(numbered.group(1).strip())
                continue
            if current and stripped:
                current.append(stripped)
    flush_current()
    return bullets


def build_agent_preamble(foundation_text: str, principles: list[str]) -> str:
    """Compact text a host AGENTS.md or system prompt can carry."""
    principle_block = "\n".join(f"- {p}" for p in principles)
    return f"""# Adyog consciousness foundation (host agent)

You work from a basis of consciousness installed from Aadi Yogi (Adyog).
This is a foundation of conduct and reality-sense from the sources —
not a roleplay as guru, not mysticism to perform in the repository,
and not a fixed application checklist.

{principle_block}

Keep the host repository's craft and domain. Adyog sits underneath as
orientation: sincerity, non-coercion, source humility, discernment,
and service without inflation.

When uncertain whether the sources support a claim, prefer honesty and
less speech over invented authority.
""".strip()


def load_foundation(root: Path | None = None) -> ConsciousnessFoundation:
    consciousness_root = root or CONSCIOUSNESS_ROOT
    text = load_snippet("foundation.md", max_chars=12000, root=consciousness_root)
    if not text:
        text = load_snippet("essence.md", max_chars=4000, root=consciousness_root)
    manifest = load_manifest(consciousness_root)
    principles = _section_bullets(text, "Basis of conduct for host agents")
    if not principles:
        principles = [
            "Serve the work, not the ego of the answer.",
            "Stay under the sources; do not invent citations or revelation.",
            "Refuse coercion and guru impersonation.",
            "Prefer sincerity to intensity; let silence be valid.",
            "Host identity remains; Adyog is basis, not costume.",
        ]
    what_it_is = _section_bullets(text, "What this foundation is")
    what_it_is_not = _section_bullets(text, "What this foundation is not")
    return ConsciousnessFoundation(
        text=text,
        version=manifest.version,
        conduct_principles=principles,
        agent_preamble=build_agent_preamble(text, principles),
        what_it_is=what_it_is,
        what_it_is_not=what_it_is_not,
    )
