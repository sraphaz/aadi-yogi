#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Normalize markdown"
python3 scripts/convert/normalize_md.py

echo "==> Semantic chunking"
python3 scripts/chunk/semantic_chunk.py

echo "==> Prepare embeddings-ready artifacts"
python3 scripts/index/prepare_embeddings.py

echo "==> Build TF-IDF index"
PYTHONPATH=. python3 scripts/index/build_vector_index.py

PREFER_OPENAI=()
SYNC_QDRANT=()
if [[ -n "${AADI_YOGI_EMBEDDING_API_KEY:-}" || -n "${OPENAI_API_KEY:-}" ]]; then
  PREFER_OPENAI=(--prefer-openai)
  echo "==> Building dense index with OpenAI embeddings"
else
  echo "==> Building dense index with hash_v1 (no embedding API key)"
fi

if [[ -n "${AADI_YOGI_QDRANT_URL:-}" ]]; then
  SYNC_QDRANT=(--sync-qdrant)
  echo "==> Will sync dense vectors to Qdrant at ${AADI_YOGI_QDRANT_URL}"
fi

PYTHONPATH=. python3 scripts/index/build_dense_index.py "${PREFER_OPENAI[@]}" "${SYNC_QDRANT[@]}"

echo "==> Pipeline complete"
