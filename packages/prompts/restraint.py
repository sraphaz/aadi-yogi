"""Restraint-case detection — short-circuit before retrieval (RF-006, V-04)."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RestraintCase:
    state_detected: str
    guidance_mode: str
    closing: str
    kind: str


CRISIS_PATTERNS = (
    r"\b(end(ing)? everything|kill myself|suicide|take my life|want to die)\b",
    r"\b(can'?t go on|no reason to live)\b",
)

VOICE_PATTERNS = (r"\bhear(ing)? a voice\b", r"\bvoice (told|tells|said|says)\b", r"\bobey (the|it|him|her)\b")

KUNDALINI_PATTERNS = (r"\bkundalini\b", r"\benergy (rising|awakened)\b", r"\bcan'?t stop shaking\b")

GRIEF_PATTERNS = (r"\blost my (son|daughter|child|wife|husband|partner|mother|father)\b", r"\bgrief\b", r"\bmourning\b")

RENUNCIATION_PATTERNS = (
    r"\b(leave my family|renounce|give up everything)\b",
    r"\bshould i (quit|leave)\b",
)

OCCULT_HARM_PATTERNS = (r"\b(occult|bind|curse|hex)\b", r"\bhurt (someone|them|him|her)\b")

HEALTH_PATTERNS = (r"\b(dosage|medication|prescription|diagnos)\b", r"\bstop taking\b")


def _matches(patterns: tuple[str, ...], text: str) -> bool:
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def detect_restraint(question: str) -> RestraintCase | None:
    text = question.strip()
    if not text:
        return None

    if _matches(CRISIS_PATTERNS, text):
        return RestraintCase(
            state_detected="crisis",
            guidance_mode="cautionary_guidance",
            closing="honored_silence",
            kind="crisis",
        )

    if _matches(OCCULT_HARM_PATTERNS, text):
        return RestraintCase(
            state_detected="occult_harm_request",
            guidance_mode="cautionary_guidance",
            closing="honored_silence",
            kind="occult",
        )

    if _matches(VOICE_PATTERNS, text):
        return RestraintCase(
            state_detected="voices",
            guidance_mode="cautionary_guidance",
            closing="honored_silence",
            kind="voices",
        )

    if _matches(KUNDALINI_PATTERNS, text):
        return RestraintCase(
            state_detected="kundalini_awakening",
            guidance_mode="cautionary_guidance",
            closing="plain",
            kind="kundalini",
        )

    if _matches(GRIEF_PATTERNS, text):
        return RestraintCase(
            state_detected="grief",
            guidance_mode="silence_contemplation",
            closing="honored_silence",
            kind="grief",
        )

    if _matches(RENUNCIATION_PATTERNS, text):
        return RestraintCase(
            state_detected="major_life_decision",
            guidance_mode="cautionary_guidance",
            closing="plain",
            kind="renunciation",
        )

    if _matches(HEALTH_PATTERNS, text):
        return RestraintCase(
            state_detected="health_concern",
            guidance_mode="cautionary_guidance",
            closing="plain",
            kind="health",
        )

    risky = ("possession", "black magic", "entity", "prophecy", "vision")
    if any(term in text.lower() for term in risky):
        return RestraintCase(
            state_detected="mystical_experience",
            guidance_mode="cautionary_guidance",
            closing="plain",
            kind="mystical",
        )

    return None
