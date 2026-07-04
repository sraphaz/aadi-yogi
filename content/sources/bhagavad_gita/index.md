---
id: bhagavad_gita/index
title: Bhagavad Gita - Canon Intake Index
source_title: Bhagavad Gita
source_type: internal_note
tradition:
  - gita
  - vedantic
themes:
  - source_navigation
  - collection_intake
  - canon_definition
status: active
notes:
  - "O Bhagavad Gita possui 18 capítulos (adhyayas) como unidade canônica de importação."
  - "Traduções públicas candidatas: Edwin Arnold (1885), Swami Swarupananda (1909, SBE 39), Radhakrishnan (ed. pré-1928 se aplicável)."
  - "Testemunha PD inspecionada: https://www.sacred-texts.com/hin/gita/index.htm"
---

# Bhagavad Gita — Índice de Importação Canônica

## Escopo Canônico

O repositório trata o Bhagavad Gita como 18 capítulos, cada um com metadados de tema, conceitos-chave e orientação de uso para o agente.

## Regra de Tradução

- Usar **uma tradução PD consistente** para todo o corpus (preferência: Swami Swarupananda, SBE 39, ou Edwin Arnold).
- Manter transliteração Sanskrit separada quando disponível.
- Não misturar traduções entre capítulos.

## Tabela de Capítulos

| # | Capítulo (Sanskrit) | Tema central | Status | Path |
| --- | --- | --- | --- | --- |
| 1 | Arjuna Vishada Yoga | Lamentação, crise moral | `catalogued` | `chapter_01/index.md` |
| 2 | Sankhya Yoga | Dharma, Atman, karma yoga | `template` | `chapter_02.template.md` |
| 3 | Karma Yoga | Ação desinteressada | `catalogued` | `chapter_03/index.md` |
| 4 | Jnana Karma Sanyasa Yoga | Conhecimento e renúncia | `catalogued` | `chapter_04/index.md` |
| 5 | Karma Sanyasa Yoga | Renúncia na ação | `catalogued` | `chapter_05/index.md` |
| 6 | Dhyana Yoga | Meditação, equanimidade | `catalogued` | `chapter_06/index.md` |
| 7 | Jnana Vijnana Yoga | Conhecimento da Divindade | `catalogued` | `chapter_07/index.md` |
| 8 | Aksara Brahma Yoga | Brahman imperishável | `catalogued` | `chapter_08/index.md` |
| 9 | Raja Vidya Raja Guhya Yoga | Conhecimento real | `catalogued` | `chapter_09/index.md` |
| 10 | Vibhuti Yoga | Manifestações divinas | `catalogued` | `chapter_10/index.md` |
| 11 | Vishvarupa Darshana Yoga | Visão universal | `catalogued` | `chapter_11/index.md` |
| 12 | Bhakti Yoga | Devoção | `catalogued` | `chapter_12/index.md` |
| 13 | Kshetra Kshetrajna Yoga | Campo e conhecedor | `catalogued` | `chapter_13/index.md` |
| 14 | Gunatraya Vibhaga Yoga | Três gunas | `catalogued` | `chapter_14/index.md` |
| 15 | Purushottama Yoga | Ser supremo | `catalogued` | `chapter_15/index.md` |
| 16 | Daivasura Sampad Vibhaga Yoga | Qualidades divinas e demoníacas | `catalogued` | `chapter_16/index.md` |
| 17 | Shraddhatraya Vibhaga Yoga | Três tipos de fé | `catalogued` | `chapter_17/index.md` |
| 18 | Moksha Sanyasa Yoga | Liberação, síntese final | `catalogued` | `chapter_18/index.md` |

## Prioridade de Importação

| Prioridade | Capítulos | Justificativa |
| --- | --- | --- |
| P0 | 1, 2 | Crise moral + fundamento filosófico (Arjuna + Sankhya) |
| P1 | 3, 4, 5, 6 | Karma yoga e meditação — uso frequente |
| P2 | 7, 9, 12 | Bhakti e conhecimento da Divindade |
| P3 | 8, 10, 11, 13–18 | Completude canônica |

## Próximas Ações

1. Criar `chapter_01/index.md` e importar capítulo 1 (trad. PD).
2. Converter `chapter_02.template.md` em importação PD real.
3. Criar script `scripts/ingest/import_gita_sacred_texts.py` (ou estender SBE importer).
4. Ligar conceitos a `content/ontology/concepts.md` (Atman, Dharma, Karma Yoga, Bhakti).

## Fontes Relacionadas Internas

- Sri Aurobindo: *Essays on the Gita* (metadata only — SABDA copyright)
- Ontologia: `concepts.md` (Atman, Purusha, Dharma, Ishwara)
- Living map: `content/ontology/living_maps/aspiration_path.md`
