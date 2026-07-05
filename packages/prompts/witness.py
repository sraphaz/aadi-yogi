"""Witness mode — transient reflection, no persistence (RF-012)."""

from __future__ import annotations

from dataclasses import dataclass

from packages.prompts.llm_client import LLMClient, LLMResponse
from packages.prompts.restraint import detect_restraint
from packages.rag.citations import derive_passage_id, primary_tradition
from packages.rag.hybrid_retriever import HybridRetriever
from packages.rag.retriever import RetrievedChunk, SimpleRetriever


WITNESS_SYSTEM = """You are a witness, not an advisor. Reflect the seeker's own words back
with care. Offer no diagnosis, no prediction, no instruction unless it is a single gentle
movement marked optional. At most one cited source resonance if retrieval is provided.
Keep the response under 120 words. Do not claim memory of this entry afterwards."""


@dataclass(frozen=True)
class WitnessCitation:
    passage_id: str
    quote: str
    tradition: str = ""


@dataclass(frozen=True)
class WitnessResult:
    body: str
    citation: WitnessCitation | None
    provider: str
    model: str
    restraint: bool


def _fallback_witness(text: str, chunk: RetrievedChunk | None) -> WitnessResult:
    excerpt = text.strip().replace("\n", " ")
    if len(excerpt) > 180:
        excerpt = excerpt[:177] + "..."
    body = (
        f"What is written here carries weight: {excerpt}\n\n"
        "No conclusion is offered — only that it was received with care."
    )
    citation = None
    if chunk:
        quote = chunk.text.strip().replace("\n", " ")
        if len(quote) > 220:
            quote = quote[:217] + "..."
        citation = WitnessCitation(
            passage_id=derive_passage_id(chunk),
            quote=quote,
            tradition=primary_tradition(chunk),
        )
        body += f"\n\nOne source may echo this: {quote}"
    return WitnessResult(body=body, citation=citation, provider="fallback", model="witness_compose_v1", restraint=False)


def witness_reflect(
    text: str,
    retriever: HybridRetriever | SimpleRetriever | None = None,
    llm_client: LLMClient | None = None,
) -> WitnessResult:
    """Reflect one invited diary entry. Caller must not persist *text*."""
    trimmed = text.strip()
    if len(trimmed) < 3:
        return WitnessResult(
            body="The page is nearly empty. When words arrive, the witness can receive them once.",
            citation=None,
            provider="witness",
            model="empty_v1",
            restraint=False,
        )

    restraint = detect_restraint(trimmed)
    if restraint:
        return WitnessResult(
            body=(
                "What is written here asks for steadiness first — not interpretation. "
                "Ground, breathe, reach for human presence if needed. "
                "The witness holds no memory of this afterwards."
            ),
            citation=None,
            provider="restraint_router",
            model="consciousness_core_v1",
            restraint=True,
        )

    retriever = retriever or HybridRetriever()
    llm_client = llm_client or LLMClient()

    if isinstance(retriever, HybridRetriever):
        chunks = retriever.as_retrieved_chunks(trimmed[:800], top_k=1)
    else:
        chunks = retriever.retrieve(trimmed[:800], top_k=1)

    chunk = chunks[0] if chunks else None
    user_prompt = f"Seeker's diary entry (read once, do not store):\n\n{trimmed[:4000]}"
    if chunk:
        user_prompt += f"\n\nOptional source resonance:\n{chunk.text[:600]}"

    if llm_client.available:
        response: LLMResponse = llm_client.complete(WITNESS_SYSTEM, user_prompt)
        citation = None
        if chunk:
            quote = chunk.text.strip().replace("\n", " ")
            if len(quote) > 220:
                quote = quote[:217] + "..."
            citation = WitnessCitation(
                passage_id=derive_passage_id(chunk),
                quote=quote,
                tradition=primary_tradition(chunk),
            )
        return WitnessResult(
            body=response.content.strip(),
            citation=citation,
            provider=response.provider,
            model=response.model,
            restraint=False,
        )

    return _fallback_witness(trimmed, chunk)
