# Production Setup — OpenAI Embeddings + Qdrant

This guide covers running the Aadi Yogi retrieval stack with hosted dense vectors and optional LLM synthesis.

## Prerequisites

- Python 3.11+
- Docker (for local Qdrant) or a hosted Qdrant instance
- OpenAI-compatible API keys for embeddings and (optionally) LLM

## 1. Environment

Copy the example file and fill in secrets:

```bash
cp .env.example .env
```

Key variables:

| Variable | Purpose |
|----------|---------|
| `AADI_YOGI_EMBEDDING_API_KEY` | OpenAI embeddings for dense index |
| `AADI_YOGI_QDRANT_URL` | Qdrant HTTP endpoint |
| `AADI_YOGI_QDRANT_COLLECTION` | Collection name (default `aadi_yogi_chunks`) |
| `AADI_YOGI_USE_QDRANT=1` | Route dense retrieval through Qdrant |
| `AADI_YOGI_LLM_API_KEY` | Optional LLM for `/ask` synthesis |

## 2. Start Qdrant

```bash
docker compose up -d qdrant
```

Verify: `curl http://localhost:6333/collections`

## 3. Build and Sync Indexes

Run the full pipeline (normalize → chunk → TF-IDF → dense → Qdrant):

```bash
./scripts/run_production_pipeline.sh
```

Or step by step with OpenAI embeddings and Qdrant sync:

```bash
pnpm pipeline:normalize
pnpm pipeline:chunk
pnpm pipeline:embeddings
pnpm pipeline:index
PYTHONPATH=. python3 scripts/index/build_dense_index.py --prefer-openai --sync-qdrant
```

Without OpenAI keys, the dense index falls back to deterministic `hash_v1` embeddings (suitable for CI).

## 4. Run the API

```bash
export $(grep -v '^#' .env | xargs)
pnpm api:dev
```

Check health:

```bash
curl http://localhost:8000/health
```

Expected fields: `llm_configured`, `embedding_provider`, `tfidf_index`, `dense_index`, `qdrant_configured`, `qdrant_enabled`.

## 5. Evaluations

```bash
pnpm eval:golden
pnpm eval:response
```

## Deployment Notes

- Store `.env` outside version control; never commit API keys.
- Re-run `build_dense_index.py --prefer-openai --sync-qdrant` after corpus imports.
- Use the same embedding model in production that was used to build the Qdrant collection.
- Complete `docs/production_review_checklist.md` before public exposure.
