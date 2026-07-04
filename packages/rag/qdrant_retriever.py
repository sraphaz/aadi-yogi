from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from packages.rag.embeddings import EmbeddingProvider, HashEmbeddingProvider, normalize_vector
from packages.rag.retriever import RetrievedChunk


QDRANT_URL = os.environ.get("AADI_YOGI_QDRANT_URL", os.environ.get("QDRANT_URL", "")).rstrip("/")
QDRANT_API_KEY = os.environ.get("AADI_YOGI_QDRANT_API_KEY", os.environ.get("QDRANT_API_KEY", ""))
QDRANT_COLLECTION = os.environ.get("AADI_YOGI_QDRANT_COLLECTION", "aadi_yogi_chunks")


class QdrantRetriever:
    """Query vectors from a remote Qdrant collection."""

    def __init__(
        self,
        url: str | None = None,
        api_key: str | None = None,
        collection: str | None = None,
    ) -> None:
        self.url = (url or QDRANT_URL).rstrip("/")
        self.api_key = api_key or QDRANT_API_KEY
        self.collection = collection or QDRANT_COLLECTION

    @property
    def configured(self) -> bool:
        return bool(self.url)

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", "User-Agent": "AadiYogiQdrantRetriever/1.0"}
        if self.api_key:
            headers["api-key"] = self.api_key
        return headers

    def search(
        self,
        query: str,
        provider: EmbeddingProvider | None = None,
        top_k: int = 5,
    ) -> list[tuple[RetrievedChunk, float]]:
        if not self.configured:
            return []
        provider = provider or HashEmbeddingProvider()
        vector = normalize_vector(provider.embed([query])[0])
        payload = {
            "vector": vector,
            "limit": top_k,
            "with_payload": True,
        }
        request = urllib.request.Request(
            f"{self.url}/collections/{self.collection}/points/search",
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(),
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Qdrant search failed ({exc.code}): {detail}") from exc

        hits: list[tuple[RetrievedChunk, float]] = []
        for item in body.get("result", []):
            point_payload = item.get("payload", {})
            if not isinstance(point_payload, dict):
                point_payload = {}
            metadata = point_payload.get("metadata", {})
            if not isinstance(metadata, dict):
                metadata = {}
            chunk = RetrievedChunk(
                chunk_id=str(item.get("id", "")),
                source_id=str(point_payload.get("source_id", "")),
                text=str(point_payload.get("text", "")),
                score=float(item.get("score", 0.0)),
                citation=point_payload.get("citation"),
                metadata=metadata,
            )
            hits.append((chunk, chunk.score))
        return hits
