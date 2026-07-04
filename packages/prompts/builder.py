from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from packages.rag.retriever import RetrievedChunk, SimpleRetriever


REPO_ROOT = Path(__file__).resolve().parents[2]
CONSCIOUSNESS_ROOT = REPO_ROOT / "content" / "consciousness_core"


@dataclass(frozen=True)
class PromptBundle:
    system_prompt: str
    user_prompt: str
    citations: list[str]
    caution: str | None


def load_consciousness_snippet(filename: str, max_chars: int = 1200) -> str:
    path = CONSCIOUSNESS_ROOT / filename
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    return text[:max_chars].strip()


def detect_caution(question: str) -> str | None:
    risky_terms = ("kundalini", "suicide", "possession", "black magic", "curse", "entity")
    lowered = question.lower()
    if any(term in lowered for term in risky_terms):
        return (
            "Proceed with grounding, caution, and referral to qualified human support when risk is present."
        )
    return None


def format_citations(chunks: list[RetrievedChunk]) -> list[str]:
    citations: list[str] = []
    for chunk in chunks:
        label = chunk.citation or chunk.source_id
        citations.append(f"- {label}")
    return citations


def build_prompt(question: str, retriever: SimpleRetriever | None = None, top_k: int = 5) -> PromptBundle:
    retriever = retriever or SimpleRetriever()
    chunks = retriever.retrieve(question, top_k=top_k)
    caution = detect_caution(question)

    essence = load_consciousness_snippet("essence.md")
    ethics = load_consciousness_snippet("spiritual_ethics.md")
    synthesis = load_consciousness_snippet("synthesis_rules.md")

    source_block = "\n\n".join(
        f"[Source: {chunk.source_id} | score={chunk.score:.2f}]\n{chunk.text[:800]}"
        for chunk in chunks
    ) or "No matching source chunks were retrieved. Answer with humility and avoid invented citations."

    system_prompt = f"""You are Aadi Yogi, a source-grounded spiritual guidance architecture.

{essence}

Ethical boundaries:
{ethics}

Synthesis rules:
{synthesis}

Rules:
- Do not claim realization or impersonate a guru.
- Cite retrieved sources when making source-grounded statements.
- Name tradition differences instead of flattening them.
- Prefer caution when the question involves intense practice or distress.
"""

    user_prompt = f"""Question:
{question}

Retrieved source excerpts:
{source_block}

Respond with humility, source awareness, and practical clarity."""

    return PromptBundle(
        system_prompt=system_prompt.strip(),
        user_prompt=user_prompt.strip(),
        citations=format_citations(chunks),
        caution=caution,
    )
