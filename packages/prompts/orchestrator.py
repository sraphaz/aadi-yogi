from __future__ import annotations

from dataclasses import dataclass

from packages.prompts.builder import PromptBundle, build_prompt
from packages.prompts.llm_client import LLMClient, LLMResponse
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
    caution = (
        f"\n\nCaution: {bundle.caution}" if bundle.caution else ""
    )
    return (
        f"Here is a source-grounded orientation toward your question: {question}\n\n"
        f"{joined}\n\n"
        "This response was composed from retrieved passages without an external LLM. "
        "Traditions may differ; compare sources carefully and seek living guidance when needed."
        f"{caution}"
    )


def ask_question(
    question: str,
    retriever: HybridRetriever | SimpleRetriever | None = None,
    llm_client: LLMClient | None = None,
    top_k: int = 5,
) -> AgentAnswer:
    retriever = retriever or HybridRetriever()
    llm_client = llm_client or LLMClient()

    if isinstance(retriever, HybridRetriever):
        chunks = retriever.as_retrieved_chunks(question, top_k=top_k)
    else:
        chunks = retriever.retrieve(question, top_k=top_k)

    bundle = build_prompt(question, chunks=chunks)

    if llm_client.available:
        response: LLMResponse = llm_client.complete(bundle.system_prompt, bundle.user_prompt)
        answer = response.content
        provider = response.provider
        model = response.model
    else:
        answer = fallback_answer(question, bundle, chunks)
        provider = "fallback"
        model = "source_compose_v1"

    if bundle.caution:
        answer = f"{answer}\n\n⚠ {bundle.caution}"

    return AgentAnswer(
        question=question,
        answer=answer,
        citations=bundle.citations,
        caution=bundle.caution,
        provider=provider,
        model=model,
        retrieved_chunks=chunks,
    )
