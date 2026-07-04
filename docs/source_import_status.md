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
- Verified collection pages:
  - `https://en.wikisource.org/wiki/Sacred_Books_of_the_East/Volume_1`
  - `https://en.wikisource.org/wiki/Sacred_Books_of_the_East/Volume_15`
  - `https://www.sacred-texts.com/hin/sbe01/index.htm`
  - `https://www.sacred-texts.com/hin/sbe15/index.htm`
  - `https://www.sacred-texts.com/hin/tmu/index.htm`
- Phase 1 import:
  - Isha Upanishad public-domain English translation by Max Muller.
- Phase 2 expansion:
  - root canon index for the full 108-text corpus
  - intake stub indexes established across the remaining 107 Upanishads before full-text import began
  - Kena Upanishad public-domain English translation by Max Muller from the Talavakara-upanishad witness in SBE 1
  - Katha Upanishad public-domain English translation by Max Muller from SBE 15
  - Mundaka Upanishad public-domain English translation by Max Muller from SBE 15

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

- Mandala 1 Hymns 1–10 imported from English Wikisource (Griffith translation).

### Tirumandiram Expansion

- Tantras 1–3 imported from Tamil Wikisource in addition to payiram.

### Pipeline and Agent Scaffold

- Normalization, chunking, and embeddings-ready artifacts operational.
- 376 chunks across 39 imported sources.
- Agent API scaffold at `apps/agent-api/main.py` with retriever and prompt builder.
- 5 synthesis notes and 8 golden questions with retrieval eval passing.

### Internal Content (Consciousness Core + Ontology + Synthesis)

- Consciousness Core: 9 guidance files at v1 draft (`content/consciousness_core/`).
- Ontology: concepts, deities, practices, sanskrit terms, states, 4 living maps.
- Synthesis: 5 initial notes in `content/synthesis/`.
- These are not source imports but are required for agent behavior; see `docs/content_import_roadmap.md` section B.

## Next Safe Expansion

1. Import additional principal Upanishads when stable Wikisource witnesses become available (Taittiriya, Shvetashvatara, Brihadaranyaka, Chandogya, Kaushitaki).
2. Expand Rig Veda Mandala 1 beyond hymn 10 and begin Mandala 2 intake.
3. Continue Tirumandiram tantras 4–9 and shorter Siddha corpora.
4. Add more public-domain Purana witnesses beyond Vishnu Purana chapter 1.
5. Keep Sri Aurobindo and the Mother at metadata-only unless reuse rights are confirmed.
6. Connect embedding generation and vector database to the prepared JSONL corpus.
7. Add LLM orchestration atop the agent API prompt scaffold.
