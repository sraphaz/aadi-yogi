---
id: sources/index
title: Fontes Canônicas - Índice Mestre
source_title: Aadi Yogi Source Corpus
source_type: internal_note
tradition:
  - vedic
  - upanishadic
  - puranic
  - gita
  - siddha
  - integral_yoga
themes:
  - source_navigation
  - collection_intake
  - canon_definition
status: active
notes:
  - "Índice mestre de todas as coleções de fontes canônicas do repositório."
  - "Ver docs/content_import_roadmap.md para o plano completo de importação."
---

# Fontes Canônicas — Índice Mestre

Este índice centraliza todas as coleções de fontes do Aadi Yogi. Cada coleção tem seu próprio índice detalhado com tabela de status por texto.

## Distinção de Cobertura

- **Cobertura canônica:** cada texto-alvo tem `index.md` e caminho estável no repositório.
- **Cobertura de texto:** o conteúdo foi importado com testemunha verificada e proveniência documentada.

## Coleções

| Coleção | Escopo | Índice | Textos PD importados | Status geral |
| --- | --- | --- | --- | --- |
| Upanishads | 108 (cânon Muktika) | [`upanishads/index.md`](upanishads/index.md) | 7 | Catálogo completo; importação em curso |
| Vedas | Rig, Sama, Yajur (×2), Atharva | [`vedas/index.md`](vedas/index.md) | 10 hinos M1 | Catálogo completo; Mandala 1 parcial |
| Puranas | 18 Mahapuranas | [`puranas/index.md`](puranas/index.md) | 1 capítulo | Catálogo completo; amostra iniciada |
| Bhagavad Gita | 18 capítulos | [`bhagavad_gita/index.md`](bhagavad_gita/index.md) | 18 | Completo (Edwin Arnold PD) |
| Textos Siddha | Corpus Tamil principal | [`siddha_texts/index.md`](siddha_texts/index.md) | 13 | Tirumandiram + 3 Siddhars |
| Sri Aurobindo | 37 volumes SABDA | [`sri_aurobindo/index.md`](sri_aurobindo/index.md) | 0 | Metadata only (copyright) |
| A Mãe | 17 volumes SABDA | [`the_mother/index.md`](the_mother/index.md) | 0 | Metadata only (copyright) |

## Status de Importação (resumo)

| Status | Significado |
| --- | --- |
| `catalogued` | Índice criado; texto não importado |
| `import_started_public_domain` | Importação PD iniciada (parcial ou amostra) |
| `imported_public_domain` | Texto PD completo importado |
| `metadata_only` | Apenas metadados (copyright restritivo) |
| `template` | Template editorial (fase fundação) |
| `approved` | Revisado e aprovado editorialmente |

## Próximas Ações Urgentes (Onda 0)

1. Importar Bhagavad Gita capítulos 1–2 (tradução PD).
2. Importar Upanishads Prashna e Mandukya via script SBE.
3. Importar Tirumandiram tantra_01 via Tamil Wikisource.
4. Expandir Rig Veda Mandala 1 (hinos 2–10).

## Documentação Relacionada

- [`docs/content_import_roadmap.md`](../../docs/content_import_roadmap.md) — plano completo de importação
- [`docs/source_import_status.md`](../../docs/source_import_status.md) — status detalhado por coleção
- [`docs/copyright_policy.md`](../../docs/copyright_policy.md) — política de direitos autorais
- [`scripts/ingest/README.md`](../../scripts/ingest/README.md) — scripts de ingestão automatizada
