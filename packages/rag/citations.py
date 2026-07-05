"""Passage ids and citation payloads for retrieval (RF-017, V-01)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from packages.rag.retriever import RetrievedChunk


@dataclass(frozen=True)
class CitationPayload:
    passage_id: str
    quote: str
    tradition: str
    source_id: str
    citation_label: str | None


def derive_passage_id(chunk: RetrievedChunk) -> str:
    meta = chunk.metadata or {}
    if meta.get("passage_id"):
        return str(meta["passage_id"])

    source_id = chunk.source_id.replace("\\", "/")
    parts = source_id.split("/")
    collection = parts[0] if parts else source_id
    if collection == "bhagavad_gita" and len(parts) >= 2:
        chapter = parts[1].replace("chapter_", "ch")
        idx = meta.get("chunk_index")
        suffix = f".c{int(idx):04d}" if idx is not None else ""
        return f"gita.{chapter}{suffix}"

    normalized = source_id.replace("/", ".")
    idx = meta.get("chunk_index")
    if idx is not None:
        return f"{normalized}.c{int(idx):04d}"
    return normalized


def normalize_tradition(value: object) -> str:
    if isinstance(value, list):
        return str(value[0]) if value else ""
    if value is None:
        return ""
    return str(value)


def primary_tradition(chunk: RetrievedChunk) -> str:
    meta = chunk.metadata or {}
    return normalize_tradition(meta.get("tradition"))


def excerpt_quote(text: str, max_len: int = 100) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_len:
        return cleaned
    snippet = cleaned[:max_len]
    if " " in snippet:
        snippet = snippet.rsplit(" ", 1)[0]
    return snippet


def chunk_to_citation_payload(chunk: RetrievedChunk) -> CitationPayload:
    return CitationPayload(
        passage_id=derive_passage_id(chunk),
        quote=excerpt_quote(chunk.text),
        tradition=primary_tradition(chunk),
        source_id=chunk.source_id,
        citation_label=chunk.citation,
    )


def build_passage_index(chunks: list[RetrievedChunk]) -> dict[str, str]:
    """Map passage_id -> full text for contract validation."""
    index: dict[str, str] = {}
    for chunk in chunks:
        index[derive_passage_id(chunk)] = chunk.text
    return index


def resolve_passage_from_index(index: dict[str, str]) -> callable:
    def resolver(passage_id: str) -> str | None:
        return index.get(passage_id)

    return resolver
