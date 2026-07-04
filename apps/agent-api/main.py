"""FastAPI scaffold for the Aadi Yogi consciousness-aware agent."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from packages.prompts.builder import PromptBundle, build_prompt
from packages.rag.retriever import RetrievedChunk, SimpleRetriever


app = FastAPI(title="Aadi Yogi Agent API", version="0.1.0")
retriever = SimpleRetriever()


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)
    top_k: int = Field(default=5, ge=1, le=20)


class ChunkResponse(BaseModel):
    chunk_id: str
    source_id: str
    score: float
    citation: str | None
    excerpt: str


class AskResponse(BaseModel):
    question: str
    system_prompt: str
    user_prompt: str
    citations: list[str]
    caution: str | None
    retrieved_chunks: list[ChunkResponse]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "aadi-yogi-agent-api"}


@app.post("/retrieve")
def retrieve(request: AskRequest) -> dict[str, object]:
    chunks = retriever.retrieve(request.question, top_k=request.top_k)
    return {
        "question": request.question,
        "chunks": [
            {
                "chunk_id": chunk.chunk_id,
                "source_id": chunk.source_id,
                "score": chunk.score,
                "citation": chunk.citation,
                "excerpt": chunk.text[:500],
            }
            for chunk in chunks
        ],
    }


@app.post("/prompt", response_model=AskResponse)
def prompt(request: AskRequest) -> AskResponse:
    bundle: PromptBundle = build_prompt(request.question, retriever=retriever, top_k=request.top_k)
    chunks: list[RetrievedChunk] = retriever.retrieve(request.question, top_k=request.top_k)
    return AskResponse(
        question=request.question,
        system_prompt=bundle.system_prompt,
        user_prompt=bundle.user_prompt,
        citations=bundle.citations,
        caution=bundle.caution,
        retrieved_chunks=[
            ChunkResponse(
                chunk_id=chunk.chunk_id,
                source_id=chunk.source_id,
                score=chunk.score,
                citation=chunk.citation,
                excerpt=chunk.text[:500],
            )
            for chunk in chunks
        ],
    )
