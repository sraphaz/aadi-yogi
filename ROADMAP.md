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

## Phase 3 — Retrieval Foundations ✅

- [x] normalization script (`scripts/convert/normalize_md.py`)
- [x] semantic chunking script (`scripts/chunk/semantic_chunk.py`)
- [x] embeddings-ready preparation (`scripts/index/prepare_embeddings.py`)
- [x] golden questions dataset (`packages/evals/golden_questions.json`)
- [x] keyword retriever (`packages/rag/retriever.py`)
- [ ] vector database selection and embedding generation (future)

## Phase 4 — Consciousness-Aware Agent Layer ✅ (scaffold)

- [x] prompt builder (`packages/prompts/builder.py`)
- [x] connect retriever outputs to response modes
- [x] source-aware citation formatting in prompt bundle
- [x] caution detection for risky topics
- [ ] approve consciousness core v1 after human review
- [ ] LLM orchestration layer (future)

## Phase 5 — Interfaces and Evaluation ✅ (scaffold)

- [x] scaffold agent API (`apps/agent-api/main.py`)
- [x] golden question retrieval eval runner
- [ ] scaffold web interface (`apps/web/`)
- [ ] LLM-backed response quality evaluation
- [ ] manual review loop for spiritual care

## Métricas Atuais

| Métrica | Valor |
| --- | --- |
| Textos com índice canônico | ~160 |
| Textos PD importados | 39 |
| Upanishads com texto PD | 6 / 108 |
| Capítulos Gita importados | 18 / 18 |
| Hinos Rig Veda M1 | 10 |
| Tirumandiram seções importadas | 4 (payiram + tantras 1–3) |
| Chunks prontos | 376 |
| Notas de síntese | 5 |
| Golden questions | 8 (100% retrieval pass) |
