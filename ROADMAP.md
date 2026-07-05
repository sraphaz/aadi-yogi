# Roadmap — Aadi Yogi

> Plano detalhado de importação: [`docs/content_import_roadmap.md`](docs/content_import_roadmap.md)
> Status de importação: [`docs/source_import_status.md`](docs/source_import_status.md)

## Phase 1 — Foundation ✅

- [x] establish monorepo structure
- [x] define repository policies and editorial standards
- [x] create source templates and ontology starters
- [x] add Markdown validation, tests, and CI
- [x] define consciousness core guidelines (v1 draft)

## Phase 2 — Source Operations ✅

- [x] catalogar 108 Upanishads, 18 Mahapuranas, 5 Vedas, corpus Siddha, Bhagavad Gita
- [x] importar corpus PD principal (39 textos normalizados)
- [x] Bhagavad Gita — 18 capítulos (Edwin Arnold, Gutenberg PD)
- [x] Upanishads PD: Isha, Kena, Katha, Mundaka, Prashna, Mandukya
- [x] Rig Veda Mandala 1 — hinos 1–10
- [x] Tirumandiram: payiram + tantras 1–3
- [x] scripts de ingestão: Wikisource SBE, Tamil Wikisource, Gutenberg Gita, Rig Veda WS
- [x] índice mestre + índice Bhagavad Gita
- [x] importar as Obras Completas de Sri Aurobindo (CWSA) e mapear as Obras da Mãe (CWM) das bibliotecas oficiais do Ashram (download por manifesto + conversão PDF→Markdown)
- [ ] revisão editorial dos volumes CWSA convertidos por máquina (status: draft)
- [ ] OCR dedicado com suporte a escrita bengali para o volume 9 do CWSA
- [ ] formalizar checkpoints de revisão de qualidade de fontes

## Phase 3 — Retrieval Foundations ✅

- [x] normalization script (`scripts/convert/normalize_md.py`)
- [x] semantic chunking script (`scripts/chunk/semantic_chunk.py`)
- [x] embeddings-ready preparation (`scripts/index/prepare_embeddings.py`)
- [x] TF-IDF vector index (`scripts/index/build_vector_index.py`)
- [x] hybrid retriever (`packages/rag/hybrid_retriever.py`)
- [x] golden questions dataset and eval runner
- [ ] external embedding model + hosted vector database (future upgrade)

## Phase 4 — Consciousness-Aware Agent Layer ✅

- [x] prompt builder with approved consciousness core v1
- [x] LLM orchestration (OpenAI-compatible API + fallback)
- [x] `/ask` endpoint with citations and caution
- [ ] human production sign-off for consciousness core

## Phase 5 — Interfaces and Evaluation ✅

- [x] agent API (`apps/agent-api/main.py`)
- [x] web UI (`apps/web/`)
- [x] golden question retrieval eval in CI
- [ ] LLM response quality evaluation suite
- [ ] manual spiritual care review loop

## Métricas Atuais

| Métrica | Valor |
| --- | --- |
| Textos PD importados | 49 |
| Upanishads com texto PD | 7 / 108 |
| Capítulos Gita importados | 18 / 18 |
| Tirumandiram seções | 10 |
| Corpora Siddha curtos | 3 |
| Chunks prontos | 390 |
| Vector index | TF-IDF (390 chunks) |
| Notas de síntese | 5 |
| Golden questions | 8 (100% retrieval pass) |
| Consciousness core | v1 approved |
