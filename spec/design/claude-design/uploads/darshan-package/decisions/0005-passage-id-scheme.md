# ADR 0005 - Stable Passage-ID Scheme

Status: accepted (decided from the consciousness core; creators calibrate)

## Context

NFR-012 requires passage identity that survives corpus rebuilds; the
library law ("no quotation is an orphan") and mechanical citation integrity
both depend on it. Full design: `docs/passage_id_scheme.md`.

## What the Consciousness Says

- **Source fidelity** (`project_vision.md`): "no invented citations" -
  the scheme makes this checkable by machine, not just by conscience.
- **Provenance** (`digitalization_pipeline.md`): "preserve provenance from
  physical source to final chunk" - canonical-structure ids are that
  provenance made addressable.

## Decision

Adopt the dot-path canonical scheme (`collection.work.division*.unit`) with
typed zero-padded ordinals, sha256_16 content fingerprints, an accumulative
alias table for re-segmentation, shared ids across renderings (original/
transliteration/translation), and graceful degradation to the parent
division on resolution failure. Details and examples in
`docs/passage_id_scheme.md`.

## Consequences

- Chunking work (`scripts/chunk`) now has its contract and cannot start ad
  hoc; CI gains drift/uniqueness/continuity checks; the eval suite's
  citation integrity becomes fingerprint-verifiable.
