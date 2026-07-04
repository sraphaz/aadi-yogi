from __future__ import annotations

import json
import pickle
from dataclasses import dataclass
from pathlib import Path

from packages.rag.embeddings import EmbeddingProvider, HashEmbeddingProvider, normalize_vector
from packages.rag.vector_store import load_records_from_jsonl


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DENSE_INDEX_PATH = REPO_ROOT / "data" / "indexes" / "dense_vector_store.pkl"


@dataclass(frozen=True)
class DenseChunk:
    chunk_id: str
    source_id: str
    text: str
    citation: str | None
    metadata: dict[str, object]
    vector: list[float]


class DenseVectorStore:
    def __init__(self, provider_name: str = "hash_v1") -> None:
        self.provider_name = provider_name
        self.chunks: list[DenseChunk] = []

    @staticmethod
    def compose_text(record: dict[str, object]) -> str:
        metadata = record.get("metadata", {})
        if not isinstance(metadata, dict):
            metadata = {}
        return " ".join(
            [
                str(record.get("text", "")),
                str(metadata.get("title", "")),
                " ".join(str(item) for item in metadata.get("themes", []) or []),
                " ".join(str(item) for item in metadata.get("concepts", []) or []),
            ]
        )

    def build_from_records(
        self,
        records: list[dict[str, object]],
        provider: EmbeddingProvider,
        batch_size: int = 32,
    ) -> None:
        self.provider_name = provider.name
        texts = [self.compose_text(record) for record in records]
        vectors: list[list[float]] = []
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            vectors.extend(provider.embed(batch))

        self.chunks = []
        for record, vector in zip(records, vectors, strict=True):
            metadata = record.get("metadata", {})
            if not isinstance(metadata, dict):
                metadata = {}
            self.chunks.append(
                DenseChunk(
                    chunk_id=str(record.get("chunk_id", "")),
                    source_id=str(record.get("source_id", "")),
                    text=str(record.get("text", "")),
                    citation=str(metadata.get("citation")) if metadata.get("citation") else None,
                    metadata=metadata,
                    vector=normalize_vector(vector),
                )
            )

    @staticmethod
    def cosine(a: list[float], b: list[float]) -> float:
        return sum(x * y for x, y in zip(a, b, strict=True))

    def search(self, query_vector: list[float], top_k: int = 5) -> list[tuple[DenseChunk, float]]:
        normalized = normalize_vector(query_vector)
        scored = [(chunk, self.cosine(normalized, chunk.vector)) for chunk in self.chunks]
        scored = [(chunk, score) for chunk, score in scored if score > 0]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def search_text(
        self,
        query: str,
        provider: EmbeddingProvider | None = None,
        top_k: int = 5,
    ) -> list[tuple[DenseChunk, float]]:
        provider = provider or HashEmbeddingProvider()
        query_vector = provider.embed([query])[0]
        return self.search(query_vector, top_k=top_k)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "provider_name": self.provider_name,
            "chunks": [
                {
                    "chunk_id": chunk.chunk_id,
                    "source_id": chunk.source_id,
                    "text": chunk.text,
                    "citation": chunk.citation,
                    "metadata": chunk.metadata,
                    "vector": chunk.vector,
                }
                for chunk in self.chunks
            ],
        }
        with path.open("wb") as handle:
            pickle.dump(payload, handle)

    @classmethod
    def load(cls, path: Path) -> DenseVectorStore:
        with path.open("rb") as handle:
            payload = pickle.load(handle)
        store = cls(provider_name=str(payload.get("provider_name", "hash_v1")))
        store.chunks = [
            DenseChunk(
                chunk_id=item["chunk_id"],
                source_id=item["source_id"],
                text=item["text"],
                citation=item.get("citation"),
                metadata=item.get("metadata", {}),
                vector=item["vector"],
            )
            for item in payload["chunks"]
        ]
        return store


def build_dense_index(
    chunk_root: Path,
    output_path: Path,
    provider: EmbeddingProvider | None = None,
) -> int:
    from packages.rag.embeddings import get_embedding_provider

    provider = provider or get_embedding_provider(prefer_openai=False)
    records = load_records_from_jsonl(chunk_root)
    store = DenseVectorStore()
    store.build_from_records(records, provider=provider)
    store.save(output_path)
    return len(store.chunks)


def export_jsonl_for_qdrant(store: DenseVectorStore, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for chunk in store.chunks:
            handle.write(
                json.dumps(
                    {
                        "id": chunk.chunk_id,
                        "vector": chunk.vector,
                        "payload": {
                            "source_id": chunk.source_id,
                            "text": chunk.text,
                            "citation": chunk.citation,
                            "metadata": chunk.metadata,
                        },
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
