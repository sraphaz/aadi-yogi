# Source Import Status

This document records what has been imported into the repository, what has only been catalogued, and why.

## Phase 1 Rule

- Import full text only when the underlying text and translation are clearly public domain or otherwise safe to reproduce.
- Import metadata only when the text is copyrighted, permission is unclear, or the available online edition is not a stable canonical source.
- Preserve provenance for every imported item.

## Current Status By Collection

### Upanishads

- Canon coverage now catalogued for all 108 Upanishads in the Muktika list.
- Public-domain translations located in the Sacred Books of the East editions hosted on English Wikisource, with the Internet Sacred Text Archive retained as a parallel witness pool.
- Phase 2 expansion includes Kena, Katha, Mundaka, Prashna, Mandukya, Isha, Kaivalya.
- Phase 3 expansion:
  - **Taittiriya Upanishad** full public-domain translation from English Wikisource standalone witness.
  - **Chandogya Upanishad** all eight prapathakas imported from SBE Volume 1 (partial corpus, complete prapathaka coverage).
  - **Shvetashvatara Upanishad** full public-domain translation from Archive.org OCR witness (SBE Volume 15).
  - **Brihadaranyaka Upanishad** full public-domain translation from Archive.org OCR witness (SBE Volume 15).

### Vedas

- Canon coverage now catalogued for Rig, Sama, Krishna Yajur, Shukla Yajur, and Atharva intake branches.
- Ancient Sanskrit source material is public domain in substance.
- Verified collection pages:
  - `https://www.sacred-texts.com/hin/rvsan/index.htm`
  - `https://www.sacred-texts.com/hin/rigveda/`
  - `https://www.sacred-texts.com/hin/index.htm`
- Phase 1 import:
  - Rig Veda Mandala 1 Hymn 1 with Sanskrit, transliteration, and public-domain English translation by Ralph T. H. Griffith.
- Phase 2 expansion:
  - root Veda canon index
  - intake stubs for Sama Veda, Krishna Yajur Veda, Shukla Yajur Veda, and Atharva Veda
- Caution:
  - The sacred-texts Sanskrit Rig Veda pages describe their Unicode transcription as experimental and not fully vetted.

### Puranas

- Canon coverage now catalogued for all 18 Mahapuranas.
- Public-domain English translation located for the Vishnu Purana:
  - `https://www.sacred-texts.com/hin/vp/index.htm`
- Phase 1 import:
  - Vishnu Purana Book 1 Chapter 1 from the 1840 H. H. Wilson translation.
- Phase 2 expansion:
  - root Mahapurana canon index
  - intake stub indexes for the remaining 17 Mahapuranas
- Important assumption:
  - the repository currently interprets `all Puranas` as the 18 Mahapuranas for canonical baseline coverage; Upapuranas remain a later expansion

### Siddha Texts

- Ancient source tradition is suitable in principle.
- Working intake shelf now created for major Siddha corpora with Tamil primary-text witness leads.
- Verified Siddha collection and text pages:
  - `https://ta.wikisource.org/wiki/சித்தர்_பாடல்கள்`
  - `https://ta.wikisource.org/wiki/திருமந்திரம்`
  - `https://ta.wikisource.org/wiki/சிவவாக்கியார்`
  - `https://ta.wikisource.org/wiki/பட்டினத்தார்`
  - `https://ta.wikisource.org/wiki/பாம்பாட்டிச்_சித்தர்`
  - `https://ta.wikisource.org/wiki/அகத்தியர்_ஞானப்_பாடல்கள்`
  - `https://ta.wikisource.org/wiki/குதம்பைச்_சித்தர்`
  - `https://ta.wikisource.org/wiki/இடைக்காட்டுச்_சித்தர்`
  - `https://ta.wikisource.org/wiki/அகப்பேய்ச்_சித்தர்`
- Phase 1 catalogued only:
  - Tamil Virtual University page
  - Himalayan Academy translation page
  - Thirumandiram.net reference site
- Phase 2 Siddha expansion:
  - root Siddha corpus index for major public-domain-ready texts
  - structured intake stubs for Sivavakkiyar, Pattinathar, Pambatti Siddhar, Agathiyar Gnana Padalgal, Kudhambai Siddhar, Idaikkattu Siddhar, and Agappey Siddhar
  - Tirumandiram section map aligned to payiram plus nine tantras
  - Tirumandiram payiram imported from the Tamil Wikisource witness
- Caution:
  - English translations and modern edited Siddha compilations still require edition-specific rights review before bulk import.

### Sri Aurobindo

- Official catalog inspected:
  - `https://www.sabda.in/catalog/show.php?id=cw`
- The inspected SABDA page advertises the Complete Works and shows a current Sri Aurobindo Ashram Trust copyright notice.
- Phase 1 action:
  - metadata-only catalog
  - no full-text import

### The Mother

- Official catalog inspected:
  - `https://www.sabda.in/catalog/show.php?id=cw`
- The inspected SABDA page lists the 17-volume Collected Works and shows a current Sri Aurobindo Ashram Trust copyright notice.
- Phase 1 action:
  - metadata-only catalog
  - no full-text import

### Bhagavad Gita

- All 18 chapters imported from Edwin Arnold's public-domain translation (Project Gutenberg #2388).
- Index at `content/sources/bhagavad_gita/index.md`.

### Mandukya Upanishad

- Public-domain Max Muller lineage translation imported at `content/sources/upanishads/mandukya/full.public_domain.md`.

### Prashna Upanishad

- Phase 2 import complete via Wikisource SBE Volume 15.

### Rig Veda Expansion

- Mandala 1 **all 191 hymns** imported from English Wikisource (Griffith translation).
- Mandala 2 **all 43 hymns** imported from English Wikisource (Griffith translation).
- Mandala 3 **all 62 hymns** imported from English Wikisource (Griffith translation).
- Mandala 4 **all 58 hymns** imported from English Wikisource (Griffith translation).
- Mandala 5 **all 87 hymns** imported from English Wikisource (Griffith translation).
- Mandala 6 **all 75 hymns** imported from English Wikisource (Griffith translation).
- Mandala 7 **all 104 hymns** imported from English Wikisource (Griffith translation).
- **Family books (Mandalas 2–7) complete**: 429 hymns total.
- Mandala 8 **all 92 hymns**, Mandala 9 **all 114 hymns**, Mandala 10 **all 191 hymns** imported.
- **Full Rig Veda Samhita (Mandalas 1–10): 1017 hymns complete.**
- Import script supports `--book`, `--from`, `--to`, `--skip-existing`, and retry with backoff for rate limits.

### Siddha Expansion (Phase 3)

- Agathiyar Gnana Padalgal, Kudhambai Siddhar, Idaikkattu Siddhar, and **Agappey Siddhar** imported from Tamil Wikisource.
- Garuda Purana Book 1 Chapter 1 sample imported (public-domain witness).

### Tirumandiram Expansion

- Tantras 1–9 imported from Tamil Wikisource in addition to payiram.

### Pipeline and Agent Scaffold

- Normalization, chunking, TF-IDF index, dense embeddings (hash/OpenAI), and optional Qdrant export/sync operational.
- **3523 chunks** across **1072** normalized source artifacts.
- Hybrid retriever combines keyword, TF-IDF, and dense signals with explicit source-reference injection (hymn, chapter, prapathaka).
- Optional Qdrant-backed dense retrieval via `AADI_YOGI_USE_QDRANT=1` and `QdrantRetriever`.
- Agent API at `apps/agent-api/main.py` with `/health`, `/retrieve`, `/prompt`, `/ask` and Portuguese web UI at `/`.
- 5 synthesis notes, consciousness core v1 approved, **22 golden questions** (100% retrieval), **22/22** response quality checks (fallback mode).
- Optional LLM via `AADI_YOGI_LLM_API_KEY`; optional OpenAI embeddings via `AADI_YOGI_EMBEDDING_API_KEY`.
- Production setup: `docker-compose.yml`, `.env.example`, `docs/production_setup.md`, `scripts/run_production_pipeline.sh`.

### Internal Content (Consciousness Core + Ontology + Synthesis)

- Consciousness Core: 9 guidance files at v1 draft (`content/consciousness_core/`).
- Ontology: concepts, deities, practices, sanskrit terms, states, 4 living maps.
- Synthesis: 5 initial notes in `content/synthesis/`.
- These are not source imports but are required for agent behavior; see `docs/content_import_roadmap.md` section B.

## Next Safe Expansion

1. Add more public-domain Purana witnesses beyond Vishnu and Garuda sample chapters.
2. Keep Sri Aurobindo and the Mother at metadata-only unless reuse rights are confirmed.
3. Run LLM-backed response quality eval with `AADI_YOGI_LLM_API_KEY`.
4. Complete human production review via `docs/production_review_checklist.md`.
5. Improve OCR cleanup for Brihadaranyaka Archive.org witness where needed.
