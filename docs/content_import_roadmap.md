# Plano de Importação de Conteúdo — Aadi Yogi

Este documento estrutura a importação urgente de **todas as fontes canônicas**, **conteúdo interno proposto** e **artefatos derivados** do repositório Aadi Yogi. Ele complementa `docs/source_import_status.md` (estado atual) e `ROADMAP.md` (fases do projeto).

## Diagnóstico Atual

| Camada | Estado | Observação |
| --- | --- | --- |
| Estrutura monorepo | ✅ Completa | Apps, packages, scripts, CI |
| Documentação editorial | ✅ Completa | Políticas, schema, pipeline |
| Consciousness Core | 🟡 Rascunho ativo | 9 arquivos de orientação + exemplos |
| Ontologia | 🟡 Rascunho ativo | Conceitos, deidades, práticas, 4 living maps |
| Síntese | 🔴 Placeholder | Apenas READMEs |
| Fontes canônicas | 🟡 Catálogo + amostras | 177 arquivos na branch de importação |
| Pipeline processado | 🔴 Placeholder | `.gitkeep` apenas |
| Scripts de ingestão | 🟡 Parcial | Wikisource SBE + Tamil Wikisource |
| RAG / Agent / Web | 🔴 Placeholder | Apenas READMEs |

**Distinção crítica:** *cobertura canônica* (cada texto tem índice e caminho estável) ≠ *cobertura de texto completo* (texto importado com testemunha verificada).

---

## Inventário Completo do Repositório

### A. Fontes Canônicas (`content/sources/`)

#### A1. Upanishads — 108 textos (cânon Muktika)

| Prioridade | Escopo | Status | Próxima ação |
| --- | --- | --- | --- |
| P0 | Índice raiz + 108 stubs | ✅ Feito | Manter sincronizado |
| P0 | 4 textos principais importados (Isha, Kena, Katha, Mundaka) | ✅ Feito | Revisão editorial |
| P1 | 6 textos principais restantes (Prashna, Mandukya, Taittiriya, Aitareya, Chandogya, Brihadaranyaka) | 🔴 Catálogo | Importar via SBE |
| P2 | 12 Upanishads principais (Shvetashvatara, Kaivalya, etc.) | 🔴 Catálogo | Importar via SBE / TMU |
| P3 | 86 Upanishads menores | 🔴 Catálogo | Importar via *Thirty Minor Upanishads* |

**Testemunhas públicas:** Sacred Books of the East (SBE 1, 15), Thirty Minor Upanishads, Wikisource.

#### A2. Vedas — 5 coleções

| Coleção | Status | Próxima ação |
| --- | --- | --- |
| Rig Veda | 1 hino importado | Expandir mandala por mandala (Griffith PD) |
| Sama Veda | Catálogo | Importar amostra + índice de hinos |
| Krishna Yajur Veda | Catálogo | Importar Taittiriya Samhita (amostra) |
| Shukla Yajur Veda | Catálogo | Identificar testemunha PD estável |
| Atharva Veda | Catálogo | Importar amostra |

#### A3. Puranas — 18 Mahapuranas

| Prioridade | Texto | Status |
| --- | --- | --- |
| P0 | Vishnu Purana | Cap. 1 importado (Wilson 1840) |
| P1 | Garuda Purana | Catálogo — testemunha PD identificada |
| P1 | Markandeya Purana | Catálogo — Devi Mahatmya relevante |
| P2 | Bhagavata, Shiva, Padma | Catálogo — revisar direitos |
| P3 | 13 restantes | Catálogo |

#### A4. Bhagavad Gita — 18 capítulos

| Status | Próxima ação |
| --- | --- |
| 1 template (cap. 2) | Criar índice de 18 capítulos + importar tradução PD (Arnold, Radhakrishnan pré-1928, ou SBE/Gita Press PD) |

#### A5. Textos Siddha — corpus Tamil

| Texto | Status | Próxima ação |
| --- | --- | --- |
| Tirumandiram | Payiram importado | Importar tantras 1–9 via Tamil Wikisource |
| Sivavakkiyar | Catálogo | Importar corpus curto |
| Pattinathar | Catálogo | Importar corpus curto |
| Pambatti, Agathiyar, Kudhambai, Idaikkattu, Agappey | Catálogo | Importar por testemunha |

**Regra:** texto primário Tamil primeiro; traduções inglesas permanecem `metadata_only` até revisão de direitos.

#### A6. Sri Aurobindo — 37 volumes (SABDA)

| Status | Política |
| --- | --- |
| Metadata only | Copyright Sri Aurobindo Ashram Trust |

**Volumes prioritários para manifest bibliográfico:**
- The Life Divine I–II
- The Synthesis of Yoga I–II
- Essays on the Gita
- Savitri I–II
- Hymns to the Mystic Fire
- Isha / Kena Upanishads (comentários SA)

#### A7. A Mãe — 17 volumes (SABDA)

| Status | Política |
| --- | --- |
| Metadata only | Copyright Sri Aurobindo Ashram Trust |

**Volumes prioritários:**
- Prayers and Meditations
- Questions and Answers 1950–1958
- Words of the Mother I–III
- On Thoughts and Aphorisms

---

### B. Conteúdo Interno Proposto

#### B1. Consciousness Core (`content/consciousness_core/`) — ✅ Rascunho v1

Arquivos existentes e maduros o suficiente para uso inicial:

| Arquivo | Função | Status |
| --- | --- | --- |
| `essence.md` | Identidade e limites do agente | ✅ v1 |
| `voice.md` | Tom e linguagem | ✅ v1 |
| `inner_posture.md` | Postura interior | ✅ v1 |
| `guidance_modes.md` | Modos de resposta | ✅ v1 |
| `discernment_matrix.md` | Matriz de discernimento | ✅ v1 |
| `synthesis_rules.md` | Regras de síntese | ✅ v1 |
| `spiritual_ethics.md` | Ética espiritual | ✅ v1 |
| `states_of_response.md` | Estados de resposta | ✅ v1 |
| `silence_and_non_answering.md` | Silêncio e não-resposta | ✅ v1 |
| `examples/` | Bons/maus/reecritos | ✅ v1 |

**Próximo:** marcar como `approved` após revisão humana; conectar a prompts em `packages/prompts/`.

#### B2. Ontologia (`content/ontology/`) — 🟡 Rascunho v1

| Arquivo | Cobertura | Próximo |
| --- | --- | --- |
| `concepts.md` | ~20 conceitos | Expandir para 50+; ligar a fontes |
| `deities.md` | Deidades principais | Expandir tradições Shakta/Tantra |
| `practices.md` | Práticas com cautelas | Adicionar práticas Siddha/Integral |
| `sanskrit_terms.md` | Termos-chave | Expandir com transliteração |
| `states_of_consciousness.md` | Estados | Revisar com fontes Upanishadic |
| `living_maps/` (4 mapas) | Caminhos práticos | Expandir para 8–12 mapas |

#### B3. Síntese (`content/synthesis/`) — 🔴 Vazio

Pastas reservadas:
- `themes/` — notas temáticas cross-tradição
- `comparative_views/` — visões comparativas
- `practical_guidance/` — orientação prática revisada

**Prioridade P1:** criar 5 sínteses iniciais ligadas a living maps existentes.

---

### C. Artefatos Processados (`content/processed/` + `data/`)

Pipeline previsto (ainda não implementado):

```text
fonte aprovada
  → normalized_md/     (limpeza, seções padronizadas)
  → chunked/           (unidades semânticas com metadados)
  → annotated/         (conceitos, deidades, cautelas)
  → embeddings_ready/  (JSONL para vetorização)
  → data/chunks/       (artefatos finais)
  → data/indexes/      (índices de busca)
```

---

## Regras de Importação por Tier de Direitos

| Tier | `copyright_status` | Ação permitida |
| --- | --- | --- |
| T1 | `public_domain` | Importação completa + indexação |
| T2 | `permission_granted` | Importação conforme escopo |
| T3 | `quotes_only` | Apenas citações curtas revisadas |
| T4 | `metadata_only` | Índice bibliográfico, temas, links |
| T5 | `permission_required` / `unknown` | Não importar texto; aguardar revisão |
| T6 | `do_not_index` | Armazenar referência; excluir de embeddings |

**Regra de ouro:** na dúvida, T4 ou T5.

---

## Fases de Implementação Urgente

### Onda 0 — Imediato (esta semana)

Objetivo: sair de “só estrutura” para “corpus mínimo utilizável”.

- [x] Merge da branch `codex/source-import-phase1` (catálogos + 8 textos PD)
- [ ] Criar `content/sources/index.md` (índice mestre)
- [ ] Criar `content/sources/bhagavad_gita/index.md` (18 capítulos)
- [ ] Importar Bhagavad Gita cap. 1–2 (trad. PD)
- [ ] Importar Upanishads P1: Prashna, Mandukya (via script SBE)
- [ ] Importar Tirumandiram tantra_01 (via script Tamil WS)
- [ ] Atualizar `docs/source_import_status.md` após cada lote

### Onda 1 — Corpus Principal (próximas 2–4 semanas de execução)

- [ ] 10 Upanishads principais com texto completo PD
- [ ] Bhagavad Gita — 18 capítulos (trad. PD única, consistente)
- [ ] Rig Veda — Mandala 1 completo
- [ ] Vishnu Purana — Livro 1 completo
- [ ] Tirumandiram — payiram + tantras 1–3
- [ ] 3 corpora Siddha curtos (Sivavakkiyar, Pattinathar, Pambatti)
- [ ] Manifests bibliográficos SA + Mother (metadata only, volume a volume)

### Onda 2 — Expansão Canônica

- [ ] 108 Upanishads — texto ou stub enriquecido para todos
- [ ] 18 Mahapuranas — amostra PD por purana
- [ ] 4 Vedas — amostra representativa por coleção
- [ ] Garuda Purana, Markandeya Purana — importação PD
- [ ] Ontologia expandida (50+ conceitos ligados a fontes)
- [ ] 5 notas de síntese iniciais

### Onda 3 — Pipeline e Retrieval

- [ ] Script `scripts/convert/normalize_md.py`
- [ ] Script `scripts/chunk/semantic_chunk.py`
- [ ] Schema de chunk documentado
- [ ] Primeiro lote `embeddings_ready/`
- [ ] Golden questions em `packages/evals/`

### Onda 4 — Agente Consciente

- [ ] Prompt builder em `packages/prompts/`
- [ ] Retriever conectado a chunks
- [ ] Agent API scaffold funcional
- [ ] Avaliações de citação, tom e segurança

---

## Workflow Operacional por Item

Cada item importado segue este fluxo:

```text
1. IDENTIFICAR  → testemunha PD ou metadata-only
2. CATALOGAR    → index.md com status, path, testemunha URL
3. IMPORTAR     → script automatizado ou manual com frontmatter
4. VALIDAR      → python3 scripts/validate/validate_markdown.py
5. REVISAR      → checklist editorial (fidelidade, citação, cautelas)
6. APROVAR      → status: approved
7. PROCESSAR    → normalizar → chunk → enriquecer
8. INDEXAR      → embeddings (somente se copyright_status permitir)
```

### Checklist de Revisão Editorial

- [ ] Frontmatter completo conforme `docs/markdown_schema.md`
- [ ] Proveniência documentada (URL, edição, tradutor, ano)
- [ ] `copyright_status` correto
- [ ] Separação clara: citação / paráfrase / comentário
- [ ] `use_for` e `avoid_for` preenchidos
- [ ] Conceitos ligados a `content/ontology/concepts.md`

---

## Scripts de Ingestão Disponíveis

| Script | Fonte | Textos configurados |
| --- | --- | --- |
| `scripts/ingest/import_wikisource_sbe.py` | Wikisource SBE | kena, katha, mundaka |
| `scripts/ingest/import_ta_wikisource.py` | Tamil Wikisource | tirumandiram_payiram |

**Expandir configurando novos targets nos scripts e registrando em `scripts/ingest/README.md`.**

---

## Métricas de Acompanhamento

| Métrica | Atual | Meta Onda 0 | Meta Onda 1 |
| --- | --- | --- | --- |
| Textos com índice canônico | ~140 | 160 | 200 |
| Textos PD importados (completo) | 8 | 15 | 40 |
| Capítulos Gita importados | 0 | 2 | 18 |
| Upanishads com texto PD | 4 | 6 | 14 |
| Tantras Tirumandiram importados | 0 (payiram sim) | 1 | 3 |
| Living maps | 4 | 4 | 8 |
| Notas de síntese | 0 | 0 | 5 |
| Chunks prontos para embedding | 0 | 0 | 500+ |

---

## Responsabilidades por Área

| Área | Pasta | Responsável sugerido |
| --- | --- | --- |
| Fontes Védicas | `content/sources/vedas/` | Curador Védico |
| Upanishads | `content/sources/upanishads/` | Curador Upanishadic |
| Puranas | `content/sources/puranas/` | Curador Puranic |
| Gita | `content/sources/bhagavad_gita/` | Curador Gita |
| Siddha | `content/sources/siddha_texts/` | Curador Tamil/Siddha |
| Integral Yoga | `content/sources/sri_aurobindo/`, `the_mother/` | Curador SA/Mother |
| Ontologia | `content/ontology/` | Arquiteto de conhecimento |
| Consciousness | `content/consciousness_core/` | Arquiteto de agente |
| Pipeline | `scripts/`, `packages/ingestion/` | Engenharia |
| Avaliação | `packages/evals/` | QA espiritual + técnico |

---

## Referências Internas

- `docs/source_import_status.md` — estado detalhado por coleção
- `docs/markdown_schema.md` — schema de frontmatter
- `docs/copyright_policy.md` — política de direitos
- `docs/editorial_guidelines.md` — diretrizes editoriais
- `docs/digitalization_pipeline.md` — pipeline físico → digital
- `content/sources/index.md` — índice mestre de fontes
- `scripts/ingest/README.md` — guia operacional de ingestão
