"""FastAPI service for the Aadi Yogi consciousness-aware agent."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from packages.prompts.builder import PromptBundle, build_prompt
from packages.prompts.llm_client import LLMClient
from packages.prompts.orchestrator import AgentAnswer, ask_question
from packages.rag.embeddings import get_embedding_provider
from packages.rag.hybrid_retriever import HybridRetriever, HybridRetrievedChunk, USE_QDRANT
from packages.rag.qdrant_retriever import QdrantRetriever
from packages.rag.retriever import RetrievedChunk


APP_ROOT = Path(__file__).resolve().parent
WEB_ROOT = APP_ROOT.parent / "web"
STATIC_ROOT = WEB_ROOT / "static"

app = FastAPI(title="Aadi Yogi Agent API", version="0.2.0")
retriever = HybridRetriever()
llm_client = LLMClient()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if STATIC_ROOT.exists():
    app.mount("/static", StaticFiles(directory=STATIC_ROOT), name="static")


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)
    top_k: int = Field(default=5, ge=1, le=20)


class ChunkResponse(BaseModel):
    chunk_id: str
    source_id: str
    score: float
    citation: str | None
    excerpt: str
    keyword_score: float | None = None
    vector_score: float | None = None
    dense_score: float | None = None


class AskResponse(BaseModel):
    question: str
    system_prompt: str
    user_prompt: str
    citations: list[str]
    caution: str | None
    retrieved_chunks: list[ChunkResponse]


class AnswerResponse(BaseModel):
    question: str
    answer: str
    citations: list[str]
    caution: str | None
    provider: str
    model: str
    retrieved_chunks: list[ChunkResponse]


def chunk_to_response(chunk: RetrievedChunk | HybridRetrievedChunk) -> ChunkResponse:
    return ChunkResponse(
        chunk_id=chunk.chunk_id,
        source_id=chunk.source_id,
        score=chunk.score,
        citation=chunk.citation,
        excerpt=chunk.text[:500],
        keyword_score=getattr(chunk, "keyword_score", None),
        vector_score=getattr(chunk, "vector_score", None),
        dense_score=getattr(chunk, "dense_score", None),
    )


@app.get("/")
def root() -> FileResponse:
    index_path = WEB_ROOT / "index.html"
    return FileResponse(index_path)


@app.get("/health")
def health() -> dict[str, object]:
    dense_store = retriever._dense_store_instance()
    embedding_provider = get_embedding_provider(
        prefer_openai=dense_store is not None and dense_store.provider_name != "hash_v1"
    )
    qdrant = QdrantRetriever()
    return {
        "status": "ok",
        "service": "aadi-yogi-agent-api",
        "llm_configured": llm_client.available,
        "embedding_provider": embedding_provider.name,
        "tfidf_index": retriever.index_path.exists(),
        "dense_index": retriever.dense_index_path.exists(),
        "dense_provider": dense_store.provider_name if dense_store else None,
        "qdrant_configured": qdrant.configured,
        "qdrant_enabled": USE_QDRANT and qdrant.configured,
        "qdrant_collection": qdrant.collection if qdrant.configured else None,
    }


@app.post("/retrieve")
def retrieve(request: AskRequest) -> dict[str, object]:
    chunks = retriever.retrieve(request.question, top_k=request.top_k)
    return {
        "question": request.question,
        "chunks": [chunk_to_response(chunk).model_dump() for chunk in chunks],
    }


@app.post("/prompt", response_model=AskResponse)
def prompt(request: AskRequest) -> AskResponse:
    chunks = retriever.as_retrieved_chunks(request.question, top_k=request.top_k)
    bundle: PromptBundle = build_prompt(request.question, chunks=chunks)
    return AskResponse(
        question=request.question,
        system_prompt=bundle.system_prompt,
        user_prompt=bundle.user_prompt,
        citations=bundle.citations,
        caution=bundle.caution,
        retrieved_chunks=[chunk_to_response(chunk) for chunk in chunks],
    )


@app.post("/ask", response_model=AnswerResponse)
def ask(request: AskRequest) -> AnswerResponse:
    result: AgentAnswer = ask_question(
        request.question,
        retriever=retriever,
        llm_client=llm_client,
        top_k=request.top_k,
    )
    return AnswerResponse(
        question=result.question,
        answer=result.answer,
        citations=result.citations,
        caution=result.caution,
        provider=result.provider,
        model=result.model,
        retrieved_chunks=[chunk_to_response(chunk) for chunk in result.retrieved_chunks],
    )
