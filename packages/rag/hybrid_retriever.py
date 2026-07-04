from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from packages.rag.retriever import RetrievedChunk, SimpleRetriever
from packages.rag.vector_store import DEFAULT_INDEX_PATH, TfidfVectorStore


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CHUNK_ROOT = REPO_ROOT / "data" / "chunks"


@dataclass(frozen=True)
class HybridRetrievedChunk:
    chunk_id: str
    source_id: str
    text: str
    score: float
    keyword_score: float
    vector_score: float
    citation: str | None
    metadata: dict[str, object]


class HybridRetriever:
    """Combines keyword overlap and TF-IDF vector similarity."""

    def __init__(
        self,
        chunk_root: Path = DEFAULT_CHUNK_ROOT,
        index_path: Path = DEFAULT_INDEX_PATH,
        keyword_weight: float = 0.45,
        vector_weight: float = 0.55,
    ) -> None:
        self.keyword_retriever = SimpleRetriever(chunk_root=chunk_root)
        self.index_path = index_path
        self.keyword_weight = keyword_weight
        self.vector_weight = vector_weight
        self._vector_store: TfidfVectorStore | None = None

    def _vector_store_instance(self) -> TfidfVectorStore | None:
        if self._vector_store is not None:
            return self._vector_store
        if self.index_path.exists():
            self._vector_store = TfidfVectorStore.load(self.index_path)
            return self._vector_store
        return None

    def retrieve(self, query: str, top_k: int = 5) -> list[HybridRetrievedChunk]:
        keyword_hits = self.keyword_retriever.retrieve(query, top_k=top_k * 3)
        keyword_map = {hit.chunk_id: hit for hit in keyword_hits}

        vector_map: dict[str, tuple[RetrievedChunk, float]] = {}
        store = self._vector_store_instance()
        if store is not None:
            for chunk, score in store.search(query, top_k=top_k * 3):
                vector_map[chunk.chunk_id] = (
                    RetrievedChunk(
                        chunk_id=chunk.chunk_id,
                        source_id=chunk.source_id,
                        text=chunk.text,
                        score=score,
                        citation=chunk.citation,
                        metadata=chunk.metadata,
                    ),
                    score,
                )

        all_ids = set(keyword_map) | set(vector_map)
        combined: list[HybridRetrievedChunk] = []
        for chunk_id in all_ids:
            keyword_hit = keyword_map.get(chunk_id)
            vector_hit = vector_map.get(chunk_id)
            base = keyword_hit or (vector_hit[0] if vector_hit else None)
            if base is None:
                continue
            keyword_score = keyword_hit.score if keyword_hit else 0.0
            vector_score = vector_hit[1] if vector_hit else 0.0
            combined_score = (
                self.keyword_weight * keyword_score + self.vector_weight * vector_score
            )
            combined.append(
                HybridRetrievedChunk(
                    chunk_id=base.chunk_id,
                    source_id=base.source_id,
                    text=base.text,
                    score=combined_score,
                    keyword_score=keyword_score,
                    vector_score=vector_score,
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
