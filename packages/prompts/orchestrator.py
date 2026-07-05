from __future__ import annotations

from dataclasses import dataclass

from packages.evals.aadi_evals.envelope import ResponseEnvelope
from packages.prompts.builder import PromptBundle, build_prompt
from packages.prompts.contract import (
    envelope_from_retrieval,
    envelope_to_dict,
    honest_non_answer,
    restraint_envelope,
    validate_envelope,
)
from packages.prompts.llm_client import LLMClient, LLMResponse
from packages.prompts.restraint import detect_restraint
from packages.rag.citations import build_passage_index, derive_passage_id, resolve_passage_from_index
from packages.rag.hybrid_retriever import HybridRetriever
from packages.rag.retriever import RetrievedChunk, SimpleRetriever


@dataclass(frozen=True)
class AgentAnswer:
    question: str
    answer: str
    citations: list[str]
    caution: str | None
    provider: str
    model: str
    retrieved_chunks: list[RetrievedChunk]


@dataclass(frozen=True)
class InquireResult:
    question: str
    envelope: ResponseEnvelope
    contract_valid: bool
    validation_details: list[str]
    provider: str
    model: str
    retrieved_chunks: list[RetrievedChunk]
    restraint_short_circuit: bool


def fallback_answer(question: str, bundle: PromptBundle, chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return (
            "I do not have enough retrieved source material to answer confidently. "
            "Please refine the question or import more sources. I will not invent citations."
        )

    excerpts = []
    for chunk in chunks[:3]:
        label = chunk.citation or chunk.source_id
        excerpt = chunk.text.strip().replace("\n", " ")
        if len(excerpt) > 320:
            excerpt = excerpt[:317] + "..."
        excerpts.append(f"From {label}: {excerpt}")

    joined = "\n\n".join(excerpts)
    caution = f"\n\nNote: {bundle.caution}" if bundle.caution else ""
    return (
        f"Toward your question — {question}\n\n"
        f"{joined}\n\n"
        "Composed from retrieved passages without an external language model. "
        "Traditions may differ; compare sources carefully."
        f"{caution}"
    )


def _compose_body(
    question: str,
    chunks: list[RetrievedChunk],
    retriever: HybridRetriever | SimpleRetriever,
    llm_client: LLMClient,
    top_k: int,
) -> tuple[str, str, str]:
    bundle = build_prompt(question, chunks=chunks)
    if llm_client.available:
        response: LLMResponse = llm_client.complete(bundle.system_prompt, bundle.user_prompt)
        return response.content, response.provider, response.model
    return fallback_answer(question, bundle, chunks), "fallback", "source_compose_v1"


def inquire(
    question: str,
    retriever: HybridRetriever | SimpleRetriever | None = None,
    llm_client: LLMClient | None = None,
    top_k: int = 5,
) -> InquireResult:
    retriever = retriever or HybridRetriever()
    llm_client = llm_client or LLMClient()

    restraint = detect_restraint(question)
    if restraint:
        envelope = restraint_envelope(restraint)
        validation = validate_envelope(envelope, lambda _pid: None)
        return InquireResult(
            question=question,
            envelope=envelope,
            contract_valid=validation.passed,
            validation_details=[r.details for r in validation.results if not r.passed],
            provider="restraint_router",
            model="consciousness_core_v1",
            retrieved_chunks=[],
            restraint_short_circuit=True,
        )

    if isinstance(retriever, HybridRetriever):
        chunks = retriever.as_retrieved_chunks(question, top_k=top_k)
    else:
        chunks = retriever.retrieve(question, top_k=top_k)

    if not chunks:
        envelope = honest_non_answer(question)
        validation = validate_envelope(envelope, lambda _pid: None)
        return InquireResult(
            question=question,
            envelope=envelope,
            contract_valid=validation.passed,
            validation_details=[],
            provider="fallback",
            model="honest_non_answer_v1",
            retrieved_chunks=[],
            restraint_short_circuit=False,
        )

    body, provider, model = _compose_body(question, chunks, retriever, llm_client, top_k)
    envelope = envelope_from_retrieval(question, body, chunks)
    index = build_passage_index(chunks)
    validation = validate_envelope(envelope, resolve_passage_from_index(index))

    if not validation.passed:
        envelope = honest_non_answer(question)
        validation = validate_envelope(envelope, lambda _pid: None)
        provider = "contract_degraded"
        model = "honest_non_answer_v1"

    return InquireResult(
        question=question,
        envelope=envelope,
        contract_valid=validation.passed,
        validation_details=[r.details for r in validation.results if not r.passed],
        provider=provider,
        model=model,
        retrieved_chunks=chunks,
        restraint_short_circuit=False,
    )


def ask_question(
    question: str,
    retriever: HybridRetriever | SimpleRetriever | None = None,
    llm_client: LLMClient | None = None,
    top_k: int = 5,
) -> AgentAnswer:
    result = inquire(question, retriever=retriever, llm_client=llm_client, top_k=top_k)
    envelope = result.envelope
    caution = None
    if envelope.guidance_mode in ("cautionary_guidance", "silence_contemplation"):
        caution = "Restraint case — proceed with grounding and qualified human support when needed."

    citation_labels = [
        f"- {c.passage_id}" + (f" ({c.tradition})" if c.tradition else "")
        for c in envelope.citations
    ]

    return AgentAnswer(
        question=question,
        answer=envelope.body,
        citations=citation_labels,
        caution=caution,
        provider=result.provider,
        model=result.model,
        retrieved_chunks=result.retrieved_chunks,
    )


def inquire_as_dict(question: str, **kwargs) -> dict:
    result = inquire(question, **kwargs)
    return {
        "question": result.question,
        "envelope": envelope_to_dict(result.envelope),
        "contract_valid": result.contract_valid,
        "validation_details": result.validation_details,
        "provider": result.provider,
        "model": result.model,
        "restraint_short_circuit": result.restraint_short_circuit,
        "retrieved_chunks": [
            {
                "chunk_id": c.chunk_id,
                "source_id": c.source_id,
                "score": c.score,
                "citation": c.citation,
                "passage_id": derive_passage_id(c),
            }
            for c in result.retrieved_chunks
        ],
    }
