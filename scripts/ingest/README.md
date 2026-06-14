# Ingest Scripts

This folder is reserved for ingestion helpers such as metadata extraction, intake checks, and handoff from raw materials into curated Markdown workflows.

## Current Intake Approach

- import full text only for clearly public-domain or permission-safe material
- import metadata only for copyrighted or unclear editions
- preserve source provenance in every imported Markdown file

## Phase 1 Imported Collections

- Isha Upanishad public-domain translation
- Rig Veda Mandala 1 Hymn 1
- Vishnu Purana Book 1 Chapter 1

## Phase 1 Metadata-Only Collections

- Tirumandiram
- Sri Aurobindo collected works
- The Mother collected works

## Phase 2 Canon Catalogs

- `content/sources/upanishads/index.md` now tracks the full Muktika canon of 108 Upanishads.
- `content/sources/puranas/index.md` now tracks the 18 Mahapuranas as the baseline Purana corpus.
- `content/sources/vedas/index.md` now tracks Rig, Sama, Krishna Yajur, Shukla Yajur, and Atharva intake branches.

## Practical Rule

Canonical coverage and full-text coverage are not the same thing.

- canonical coverage means every target text has an intake index and a stable repository path
- full-text coverage means the actual text has been imported with a verified witness and explicit provenance
