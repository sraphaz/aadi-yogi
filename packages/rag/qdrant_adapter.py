from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from packages.rag.dense_vector_store import DenseVectorStore, export_jsonl_for_qdrant


QDRANT_URL = os.environ.get("AADI_YOGI_QDRANT_URL", os.environ.get("QDRANT_URL", "")).rstrip("/")
QDRANT_API_KEY = os.environ.get("AADI_YOGI_QDRANT_API_KEY", os.environ.get("QDRANT_API_KEY", ""))
QDRANT_COLLECTION = os.environ.get("AADI_YOGI_QDRANT_COLLECTION", "aadi_yogi_chunks")


class QdrantAdapter:
    """Optional adapter to upsert local dense vectors into Qdrant."""

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
        headers = {"Content-Type": "application/json", "User-Agent": "AadiYogiQdrantAdapter/1.0"}
        if self.api_key:
            headers["api-key"] = self.api_key
        return headers

    def ensure_collection(self, vector_size: int) -> None:
        if not self.configured:
            raise RuntimeError("Qdrant URL not configured.")
        payload = {"vectors": {"size": vector_size, "distance": "Cosine"}}
        request = urllib.request.Request(
            f"{self.url}/collections/{self.collection}",
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(),
            method="PUT",
        )
        try:
            with urllib.request.urlopen(request, timeout=30):
                return
        except urllib.error.HTTPError as exc:
            if exc.code == 409:
                return
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Qdrant collection setup failed ({exc.code}): {detail}") from exc

    def upsert_store(self, store: DenseVectorStore, batch_size: int = 64) -> int:
        if not store.chunks:
            return 0
        if not self.configured:
            raise RuntimeError("Qdrant URL not configured.")
        vector_size = len(store.chunks[0].vector)
        self.ensure_collection(vector_size)

        upserted = 0
        for start in range(0, len(store.chunks), batch_size):
            batch = store.chunks[start : start + batch_size]
            points = [
                {
                    "id": chunk.chunk_id,
                    "vector": chunk.vector,
                    "payload": {
                        "source_id": chunk.source_id,
                        "text": chunk.text,
                        "citation": chunk.citation,
                        "metadata": chunk.metadata,
                    },
                }
                for chunk in batch
            ]
            request = urllib.request.Request(
                f"{self.url}/collections/{self.collection}/points?wait=true",
                data=json.dumps({"points": points}).encode("utf-8"),
                headers=self._headers(),
                method="PUT",
            )
            with urllib.request.urlopen(request, timeout=60):
                upserted += len(points)
        return upserted


def sync_dense_store_to_qdrant(store: DenseVectorStore) -> int:
    adapter = QdrantAdapter()
    if not adapter.configured:
        return 0
    return adapter.upsert_store(store)


def export_qdrant_jsonl(store: DenseVectorStore, output_path: Path) -> None:
    export_jsonl_for_qdrant(store, output_path)
