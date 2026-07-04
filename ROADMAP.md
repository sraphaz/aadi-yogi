# Roadmap — Aadi Yogi

> Plano detalhado de importação: [`docs/content_import_roadmap.md`](docs/content_import_roadmap.md)
> Status de importação: [`docs/source_import_status.md`](docs/source_import_status.md)

## Phase 1 — Foundation ✅

- [x] establish monorepo structure
- [x] define repository policies and editorial standards
- [x] create source templates and ontology starters
- [x] add Markdown validation, tests, and CI
- [x] define consciousness core guidelines (v1 draft)

## Phase 2 — Source Operations 🟡 EM ANDAMENTO

**Objetivo urgente:** sair de estrutura vazia para corpus mínimo utilizável.

### Onda 0 — Imediato

- [x] catalogar 108 Upanishads (Muktika)
- [x] catalogar 18 Mahapuranas
- [x] catalogar 5 coleções Védicas
- [x] catalogar corpus Siddha principal
- [x] importar 4 Upanishads PD (Isha, Kena, Katha, Mundaka)
- [x] importar amostra Rig Veda + Vishnu Purana + Tirumandiram payiram
- [x] scripts de ingestão Wikisource SBE + Tamil Wikisource
- [x] índice mestre de fontes (`content/sources/index.md`)
- [x] índice Bhagavad Gita (18 capítulos)
- [ ] importar Bhagavad Gita cap. 1–2 (PD)
- [ ] importar Upanishads Prashna + Mandukya
- [ ] importar Tirumandiram tantra_01

### Onda 1 — Corpus Principal

- [ ] 10 Upanishads principais com texto PD completo
- [ ] Bhagavad Gita — 18 capítulos
- [ ] Rig Veda Mandala 1 completo
- [ ] Vishnu Purana Livro 1 completo
- [ ] Tirumandiram tantras 1–3
- [ ] 3 corpora Siddha curtos
- [ ] manifests bibliográficos Sri Aurobindo + Mother (metadata)

### Onda 2 — Expansão Canônica

- [ ] 108 Upanishads — texto ou stub enriquecido
- [ ] 18 Mahapuranas — amostra PD por purana
- [ ] 4 Vedas — amostra representativa
- [ ] expandir ontologia (50+ conceitos ligados a fontes)
- [ ] 5 notas de síntese iniciais em `content/synthesis/`

## Phase 3 — Retrieval Foundations

- [ ] design chunk schemas and metadata enrichment
- [ ] implement normalization script (`scripts/convert/`)
- [ ] implement semantic chunking script (`scripts/chunk/`)
- [ ] prepare embeddings-ready artifacts
- [ ] evaluate candidate vector storage strategies
- [ ] golden questions dataset in `packages/evals/`

## Phase 4 — Consciousness-Aware Agent Layer

- [ ] formalize prompt builder inputs (`packages/prompts/`)
- [ ] connect retriever outputs to response modes
- [ ] add source-aware citation formatting
- [ ] expand safety and caution mechanisms
- [ ] approve consciousness core v1

## Phase 5 — Interfaces and Evaluation

- [ ] scaffold agent API (`apps/agent-api/`)
- [ ] scaffold web interface (`apps/web/`)
- [ ] build golden questions and evaluation suites
- [ ] compare response quality across traditions and question types
- [ ] manual review loop for spiritual care and tradition integrity

## Métricas Atuais

| Métrica | Valor |
| --- | --- |
| Textos com índice canônico | ~140 |
| Textos PD importados | 8 |
| Upanishads com texto PD | 4 / 108 |
| Capítulos Gita importados | 0 / 18 |
| Consciousness core files | 9 (v1 draft) |
| Living maps | 4 |
| Chunks prontos | 0 |
