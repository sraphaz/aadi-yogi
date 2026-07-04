from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from packages.rag.dense_vector_store import DEFAULT_DENSE_INDEX_PATH, DenseVectorStore
from packages.rag.embeddings import HashEmbeddingProvider
from packages.rag.retriever import RetrievedChunk, SimpleRetriever
from packages.rag.vector_store import DEFAULT_INDEX_PATH, TfidfVectorStore


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CHUNK_ROOT = REPO_ROOT / "data" / "chunks"
EXPLICIT_SOURCE_SCORE_FLOOR = 0.85


def extract_source_id_hints(query: str) -> list[str]:
    hints: list[str] = []
    mandala_match = re.search(r"mandala\s+(\d+).*?hymn\s+(\d+)", query, re.IGNORECASE)
    if mandala_match:
        book = int(mandala_match.group(1))
        hymn = int(mandala_match.group(2))
        hints.append(f"mandala_{book:02d}_hymn_{hymn:03d}")
    chapter_match = re.search(r"chapter\s+(\d+)", query, re.IGNORECASE)
    if chapter_match:
        hints.append(f"chapter_{int(chapter_match.group(1)):02d}")
    return hints


@dataclass(frozen=True)
class HybridRetrievedChunk:
    chunk_id: str
    source_id: str
    text: str
    score: float
    keyword_score: float
    vector_score: float
    dense_score: float
    citation: str | None
    metadata: dict[str, object]


class HybridRetriever:
    """Combines keyword overlap, TF-IDF, and optional dense embeddings."""

    def __init__(
        self,
        chunk_root: Path = DEFAULT_CHUNK_ROOT,
        index_path: Path = DEFAULT_INDEX_PATH,
        dense_index_path: Path = DEFAULT_DENSE_INDEX_PATH,
        keyword_weight: float = 0.35,
        vector_weight: float = 0.35,
        dense_weight: float = 0.30,
    ) -> None:
        self.keyword_retriever = SimpleRetriever(chunk_root=chunk_root)
        self.index_path = index_path
        self.dense_index_path = dense_index_path
        self.keyword_weight = keyword_weight
        self.vector_weight = vector_weight
        self.dense_weight = dense_weight
        self._vector_store: TfidfVectorStore | None = None
        self._dense_store: DenseVectorStore | None = None

    def _vector_store_instance(self) -> TfidfVectorStore | None:
        if self._vector_store is not None:
            return self._vector_store
        if self.index_path.exists():
            self._vector_store = TfidfVectorStore.load(self.index_path)
            return self._vector_store
        return None

    def _dense_store_instance(self) -> DenseVectorStore | None:
        if self._dense_store is not None:
            return self._dense_store
        if self.dense_index_path.exists():
            self._dense_store = DenseVectorStore.load(self.dense_index_path)
            return self._dense_store
        return None

    def retrieve(self, query: str, top_k: int = 5) -> list[HybridRetrievedChunk]:
        keyword_hits = self.keyword_retriever.retrieve(query, top_k=top_k * 3)
        keyword_map = {hit.chunk_id: hit for hit in keyword_hits}

        vector_map: dict[str, float] = {}
        store = self._vector_store_instance()
        if store is not None:
            for chunk, score in store.search(query, top_k=top_k * 3):
                vector_map[chunk.chunk_id] = score

        dense_map: dict[str, float] = {}
        dense_store = self._dense_store_instance()
        if dense_store is not None:
            provider = HashEmbeddingProvider()
            for chunk, score in dense_store.search_text(query, provider=provider, top_k=top_k * 3):
                dense_map[chunk.chunk_id] = score

        chunk_lookup: dict[str, RetrievedChunk] = {hit.chunk_id: hit for hit in keyword_hits}
        if store is not None:
            for chunk, score in store.search(query, top_k=top_k * 3):
                if chunk.chunk_id not in chunk_lookup:
                    chunk_lookup[chunk.chunk_id] = RetrievedChunk(
                        chunk_id=chunk.chunk_id,
                        source_id=chunk.source_id,
                        text=chunk.text,
                        score=score,
                        citation=chunk.citation,
                        metadata=chunk.metadata,
                    )
        if dense_store is not None:
            provider = HashEmbeddingProvider()
            for chunk, score in dense_store.search_text(query, provider=provider, top_k=top_k * 3):
                if chunk.chunk_id not in chunk_lookup:
                    chunk_lookup[chunk.chunk_id] = RetrievedChunk(
                        chunk_id=chunk.chunk_id,
                        source_id=chunk.source_id,
                        text=chunk.text,
                        score=score,
                        citation=chunk.citation,
                        metadata=chunk.metadata,
                    )

        source_hints = extract_source_id_hints(query)
        combined: list[HybridRetrievedChunk] = []
        for chunk_id, base in chunk_lookup.items():
            keyword_score = keyword_map[chunk_id].score if chunk_id in keyword_map else 0.0
            vector_score = vector_map.get(chunk_id, 0.0)
            dense_score = dense_map.get(chunk_id, 0.0)
            combined_score = (
                self.keyword_weight * keyword_score
                + self.vector_weight * vector_score
                + self.dense_weight * dense_score
            )
            if source_hints and any(hint in base.source_id for hint in source_hints):
                combined_score = max(combined_score, EXPLICIT_SOURCE_SCORE_FLOOR)
            if combined_score <= 0:
                continue
            combined.append(
                HybridRetrievedChunk(
                    chunk_id=base.chunk_id,
                    source_id=base.source_id,
                    text=base.text,
                    score=combined_score,
                    keyword_score=keyword_score,
                    vector_score=vector_score,
                    dense_score=dense_score,
                    citation=base.citation,
                    metadata=base.metadata,
                )
            )

        combined.sort(key=lambda item: item.score, reverse=True)
        return combined[:top_k]

    def as_retrieved_chunks(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        return [
            RetrievedChunk(
                chunk_id=item.chunk_id,
                source_id=item.source_id,
                text=item.text,
                score=item.score,
                citation=item.citation,
                metadata=item.metadata,
            )
            for item in self.retrieve(query, top_k=top_k)
        ]
