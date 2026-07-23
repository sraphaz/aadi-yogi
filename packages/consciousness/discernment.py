"""Parse and query the discernment matrix for foreign agents."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from packages.consciousness.manifest import CONSCIOUSNESS_ROOT

_YAML_BLOCK = re.compile(r"```yaml\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)

# Lightweight keyword hints so foreign agents can ask without knowing question_type ids.
_HINTS: dict[str, tuple[str, ...]] = {
    "suffering": ("suffer", "pain", "hurt", "anguish", "despair"),
    "fear_of_death": ("death", "dying", "mortality", "afraid to die"),
    "action_in_the_world": ("action", "work", "duty in the world", "how should i act"),
    "surrender": ("surrender", "offering", "consecrat"),
    "ego_transformation": ("ego", "pride", "selfish", "narciss"),
    "aspiration": ("aspiration", "seek", "awaken", "yearn"),
    "dharma": ("dharma", "right action", "what is my duty"),
    "intense_spiritual_experiences": ("vision", "mystical", "intense experience"),
    "kundalini_or_energetic_practices": ("kundalini", "energy rising", "chakra force"),
    "grief": ("grief", "mourning", "lost my", "bereav"),
}


@dataclass(frozen=True)
class DiscernmentEntry:
    question_type: str
    inner_state: list[str]
    primary_sources: list[str]
    response_tone: str
    avoid: list[str]
    safe_guidance: list[str]

    def to_dict(self) -> dict:
        return {
            "question_type": self.question_type,
            "inner_state": list(self.inner_state),
            "primary_sources": list(self.primary_sources),
            "response_tone": self.response_tone,
            "avoid": list(self.avoid),
            "safe_guidance": list(self.safe_guidance),
        }


def _as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def _hint_matches(hint: str, haystack: str, words: list[str]) -> bool:
    normalized_hint = hint.lower().strip()
    if not normalized_hint:
        return False
    if " " in normalized_hint:
        pattern = r"(?<!\w)" + r"\s+".join(re.escape(part) for part in normalized_hint.split()) + r"(?!\w)"
        return re.search(pattern, haystack) is not None
    if normalized_hint.isalpha() and len(normalized_hint) >= 7:
        return any(word.startswith(normalized_hint) for word in words)
    return normalized_hint in words


def _strong_hint(hint: str) -> bool:
    normalized_hint = hint.lower().strip()
    return " " in normalized_hint or len(normalized_hint) >= 7


def load_discernment_entries(root: Path | None = None) -> list[DiscernmentEntry]:
    path = (root or CONSCIOUSNESS_ROOT) / "discernment_matrix.md"
    text = path.read_text(encoding="utf-8")
    entries: list[DiscernmentEntry] = []
    for block in _YAML_BLOCK.findall(text):
        raw = yaml.safe_load(block) or {}
        question_type = str(raw.get("question_type", "")).strip()
        if not question_type:
            continue
        entries.append(
            DiscernmentEntry(
                question_type=question_type,
                inner_state=_as_list(raw.get("inner_state")),
                primary_sources=_as_list(raw.get("primary_sources")),
                response_tone=str(raw.get("response_tone", "")),
                avoid=_as_list(raw.get("avoid")),
                safe_guidance=_as_list(raw.get("safe_guidance")),
            )
        )
    return entries


def lookup_discernment(
    question_or_type: str,
    *,
    root: Path | None = None,
) -> DiscernmentEntry | None:
    """Lookup by exact question_type id, or by keyword hints in free text."""
    text = question_or_type.strip()
    if not text:
        return None
    entries = {e.question_type: e for e in load_discernment_entries(root=root)}
    lowered = text.lower().replace(" ", "_")
    if lowered in entries:
        return entries[lowered]
    if text in entries:
        return entries[text]

    scores: list[tuple[int, DiscernmentEntry]] = []
    haystack = text.lower()
    words = re.findall(r"\b[\w']+\b", haystack)
    for question_type, hints in _HINTS.items():
        entry = entries.get(question_type)
        if not entry:
            continue
        matched_hints = [hint for hint in hints if _hint_matches(hint, haystack, words)]
        score = len(matched_hints)
        if score and (score >= 2 or any(_strong_hint(hint) for hint in matched_hints)):
            scores.append((score, entry))
    if not scores:
        return None
    scores.sort(key=lambda item: item[0], reverse=True)
    return scores[0][1]
