from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CHUNK_ROOT = REPO_ROOT / "data" / "chunks"


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    source_id: str
    text: str
    score: float
    citation: str | None
    metadata: dict[str, object]


class SimpleRetriever:
    """Keyword retriever over chunked JSONL artifacts."""

    def __init__(self, chunk_root: Path = DEFAULT_CHUNK_ROOT) -> None:
        self.chunk_root = chunk_root
        self._records: list[dict[str, object]] | None = None

    def _load_records(self) -> list[dict[str, object]]:
        if self._records is not None:
            return self._records

        records: list[dict[str, object]] = []
        if not self.chunk_root.exists():
            self._records = records
            return records

        for jsonl_path in sorted(self.chunk_root.rglob("*.jsonl")):
            with jsonl_path.open(encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
        self._records = records
        return records

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return {token for token in re.findall(r"[a-zA-Z\u0900-\u097F\u0B80-\u0BFF]+", text.lower()) if len(token) > 2}

    def score(self, query: str, text: str, metadata: dict[str, object]) -> float:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return 0.0
        haystack = " ".join(
            [
                text.lower(),
                str(metadata.get("title", "")).lower(),
                " ".join(str(item) for item in metadata.get("themes", []) or []),
                " ".join(str(item) for item in metadata.get("concepts", []) or []),
            ]
        )
        text_tokens = self._tokenize(haystack)
        overlap = query_tokens & text_tokens
        return len(overlap) / len(query_tokens)

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        scored: list[RetrievedChunk] = []
        for record in self._load_records():
            metadata = record.get("metadata", {})
            if not isinstance(metadata, dict):
                metadata = {}
            if "chunk_index" in record and "chunk_index" not in metadata:
                metadata = {**metadata, "chunk_index": record["chunk_index"]}
            text = str(record.get("text", ""))
            score = self.score(query, text, metadata)
            if score <= 0:
                continue
            scored.append(
                RetrievedChunk(
                    chunk_id=str(record.get("chunk_id", "")),
                    source_id=str(record.get("source_id", "")),
                    text=text,
                    score=score,
                    citation=str(metadata.get("citation")) if metadata.get("citation") else None,
                    metadata=metadata,
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]

    def find_by_source_hints(self, hints: list[str]) -> list[RetrievedChunk]:
        if not hints:
            return []
        matches: list[RetrievedChunk] = []
        for record in self._load_records():
            source_id = str(record.get("source_id", ""))
            if not any(hint in source_id for hint in hints):
                continue
            metadata = record.get("metadata", {})
            if not isinstance(metadata, dict):
                metadata = {}
            if "chunk_index" in record and "chunk_index" not in metadata:
                metadata = {**metadata, "chunk_index": record["chunk_index"]}
            text = str(record.get("text", ""))
            matches.append(
                RetrievedChunk(
                    chunk_id=str(record.get("chunk_id", "")),
                    source_id=source_id,
                    text=text,
                    score=1.0,
                    citation=str(metadata.get("citation")) if metadata.get("citation") else None,
                    metadata=metadata,
                )
            )
        return matches
