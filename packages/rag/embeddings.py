from __future__ import annotations

import hashlib
import json
import math
import os
import urllib.error
import urllib.request
from abc import ABC, abstractmethod


DEFAULT_EMBEDDING_MODEL = os.environ.get(
    "AADI_YOGI_EMBEDDING_MODEL", "text-embedding-3-small"
)
DEFAULT_EMBEDDING_BASE_URL = os.environ.get(
    "AADI_YOGI_EMBEDDING_BASE_URL", "https://api.openai.com/v1"
)
DEFAULT_EMBEDDING_API_KEY = os.environ.get("AADI_YOGI_EMBEDDING_API_KEY") or os.environ.get(
    "OPENAI_API_KEY"
)
HASH_EMBEDDING_DIMS = 384


def normalize_vector(values: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in values)) or 1.0
    return [value / norm for value in values]


class EmbeddingProvider(ABC):
    name: str

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


class HashEmbeddingProvider(EmbeddingProvider):
    """Deterministic local embeddings for offline/CI use."""

    name = "hash_v1"

    def __init__(self, dimensions: int = HASH_EMBEDDING_DIMS) -> None:
        self.dimensions = dimensions

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            vector = [0.0] * self.dimensions
            for token in text.lower().split():
                digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
                index = int(digest[:8], 16) % self.dimensions
                vector[index] += 1.0
            vectors.append(normalize_vector(vector))
        return vectors


class OpenAIEmbeddingProvider(EmbeddingProvider):
    name = "openai"

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int = 60,
    ) -> None:
        self.api_key = api_key or DEFAULT_EMBEDDING_API_KEY
        self.base_url = (base_url or DEFAULT_EMBEDDING_BASE_URL).rstrip("/")
        self.model = model or DEFAULT_EMBEDDING_MODEL
        self.timeout = timeout

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not self.available:
            raise RuntimeError("OpenAI embedding API key not configured.")
        payload = {"model": self.model, "input": texts}
        request = urllib.request.Request(
            f"{self.base_url}/embeddings",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "AadiYogiEmbeddings/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Embedding request failed ({exc.code}): {detail}") from exc

        data = body.get("data", [])
        return [item["embedding"] for item in sorted(data, key=lambda item: item["index"])]


def get_embedding_provider(prefer_openai: bool = True) -> EmbeddingProvider:
    if prefer_openai:
        openai_provider = OpenAIEmbeddingProvider()
        if openai_provider.available:
            return openai_provider
    return HashEmbeddingProvider()
