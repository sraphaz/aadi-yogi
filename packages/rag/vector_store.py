from __future__ import annotations

import json
import math
import pickle
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INDEX_PATH = REPO_ROOT / "data" / "indexes" / "tfidf_vector_store.pkl"
TOKEN_PATTERN = re.compile(r"[a-zA-Z\u0900-\u097F\u0B80-\u0BFF]{3,}")


@dataclass(frozen=True)
class IndexedChunk:
    chunk_id: str
    source_id: str
    text: str
    citation: str | None
    metadata: dict[str, object]
    vector: dict[str, float]


class TfidfVectorStore:
    """Lightweight TF-IDF vector store without external ML dependencies."""

    def __init__(self) -> None:
        self.chunks: list[IndexedChunk] = []
        self.idf: dict[str, float] = {}
        self._vectors: list[dict[str, float]] = []

    @staticmethod
    def tokenize(text: str) -> list[str]:
        return [token.lower() for token in TOKEN_PATTERN.findall(text)]

    @staticmethod
    def _compose_text(record: dict[str, object]) -> str:
        metadata = record.get("metadata", {})
        if not isinstance(metadata, dict):
            metadata = {}
        parts = [
            str(record.get("text", "")),
            str(metadata.get("title", "")),
            " ".join(str(item) for item in metadata.get("themes", []) or []),
            " ".join(str(item) for item in metadata.get("concepts", []) or []),
        ]
        return " ".join(parts)

    def build_from_records(self, records: list[dict[str, object]]) -> None:
        docs_tokens: list[list[str]] = []
        self.chunks = []

        for record in records:
            text = self._compose_text(record)
            tokens = self.tokenize(text)
            metadata = record.get("metadata", {})
            if not isinstance(metadata, dict):
                metadata = {}
            self.chunks.append(
                IndexedChunk(
                    chunk_id=str(record.get("chunk_id", "")),
                    source_id=str(record.get("source_id", "")),
                    text=str(record.get("text", "")),
                    citation=str(metadata.get("citation")) if metadata.get("citation") else None,
                    metadata=metadata,
                    vector={},
                )
            )
            docs_tokens.append(tokens)

        doc_count = max(len(docs_tokens), 1)
        df: Counter[str] = Counter()
        for tokens in docs_tokens:
            df.update(set(tokens))

        self.idf = {term: math.log((1 + doc_count) / (1 + freq)) + 1.0 for term, freq in df.items()}
        self._vectors = [self._tfidf_vector(tokens) for tokens in docs_tokens]
        self.chunks = [
            IndexedChunk(
                chunk_id=chunk.chunk_id,
                source_id=chunk.source_id,
                text=chunk.text,
                citation=chunk.citation,
                metadata=chunk.metadata,
                vector=vector,
            )
            for chunk, vector in zip(self.chunks, self._vectors, strict=True)
        ]

    def _tfidf_vector(self, tokens: list[str]) -> dict[str, float]:
        counts = Counter(tokens)
        total = sum(counts.values()) or 1
        vector: dict[str, float] = {}
        for term, count in counts.items():
            tf = count / total
            vector[term] = tf * self.idf.get(term, 1.0)
        norm = math.sqrt(sum(value * value for value in vector.values())) or 1.0
        return {term: value / norm for term, value in vector.items()}

    def query_vector(self, query: str) -> dict[str, float]:
        return self._tfidf_vector(self.tokenize(query))

    @staticmethod
    def cosine(a: dict[str, float], b: dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        shared = set(a) & set(b)
        return sum(a[t] * b[t] for t in shared)

    def search(self, query: str, top_k: int = 5) -> list[tuple[IndexedChunk, float]]:
        query_vector = self.query_vector(query)
        scored = [(chunk, self.cosine(query_vector, chunk.vector)) for chunk in self.chunks]
        scored = [(chunk, score) for chunk, score in scored if score > 0]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "idf": self.idf,
            "chunks": [
                {
                    "chunk_id": c.chunk_id,
                    "source_id": c.source_id,
                    "text": c.text,
                    "citation": c.citation,
                    "metadata": c.metadata,
                    "vector": c.vector,
                }
                for c in self.chunks
            ],
        }
        with path.open("wb") as handle:
            pickle.dump(payload, handle)

    @classmethod
    def load(cls, path: Path) -> TfidfVectorStore:
        with path.open("rb") as handle:
            payload = pickle.load(handle)
        store = cls()
        store.idf = payload["idf"]
        store.chunks = [
            IndexedChunk(
                chunk_id=item["chunk_id"],
                source_id=item["source_id"],
                text=item["text"],
                citation=item.get("citation"),
                metadata=item.get("metadata", {}),
                vector=item["vector"],
            )
            for item in payload["chunks"]
        ]
        store._vectors = [chunk.vector for chunk in store.chunks]
        return store


def load_records_from_jsonl(chunk_root: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for jsonl_path in sorted(chunk_root.rglob("*.jsonl")):
        with jsonl_path.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
    return records
