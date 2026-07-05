# Ingest Scripts

This folder holds ingestion helpers such as metadata extraction, intake checks, and handoff from raw materials into curated Markdown workflows.

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

## Phase 2 Public-Domain Upanishad Expansion

- `content/sources/upanishads/kena/full.public_domain.md`
- `content/sources/upanishads/katha/full.public_domain.md`
- `content/sources/upanishads/mundaka/full.public_domain.md`

## Phase 2 Siddha Expansion

- `content/sources/siddha_texts/index.md` now tracks a working intake shelf for major Tamil Siddha corpora.
- `content/sources/siddha_texts/tirumandiram/payiram/full.public_domain.md` imports the first Tamil primary-text witness from Tamil Wikisource.
- additional major Siddha corpora are catalogued as intake stubs pending witness-by-witness import.

## Wikisource SBE Importer

- script: `scripts/ingest/import_wikisource_sbe.py`
- current configured texts: `kena`, `katha`, `mundaka`
- usage:

```bash
python scripts/ingest/import_wikisource_sbe.py kena katha mundaka
```

## Tamil Wikisource Importer

- script: `scripts/ingest/import_ta_wikisource.py`
- current configured texts: `tirumandiram_payiram`
- usage:

```bash
python scripts/ingest/import_ta_wikisource.py tirumandiram_payiram
```

## Ashram PDF Libraries

### download_ashram_pdfs.py

Downloads the official PDF libraries of the Sri Aurobindo Ashram into the gitignored `data/raw/` tree, driven by the manifests in `manifests/`.

```bash
python scripts/ingest/download_ashram_pdfs.py                 # all manifests
python scripts/ingest/download_ashram_pdfs.py --force         # re-download
```

### manifests/

Declarative YAML manifests describing each collection: download URLs, volume metadata, themes, and the per-volume `full_text` copyright decision that controls whether converted text may be committed to `content/sources/` or must stay local. See the header comments inside each manifest for the classification rationale.

- `sri_aurobindo_cwsa.yaml`: The Complete Works of Sri Aurobindo (37 volumes, 31 PDFs).
- `the_mother_cwm.yaml`: Collected Works of the Mother (18 French PDF volumes).

Conversion to Markdown lives in `scripts/convert/pdf_to_markdown.py`, which applies the per-volume copyright decision (full text vs metadata-only record).

## Practical Rule

Canonical coverage and full-text coverage are not the same thing.

- canonical coverage means every target text has an intake index and a stable repository path
- full-text coverage means the actual text has been imported with a verified witness and explicit provenance
