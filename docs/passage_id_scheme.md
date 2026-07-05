# Stable Passage-ID Scheme

Design for NFR-012: passage identity that survives corpus rebuilds, bundle
updates and re-segmentation, so that positions, anthologies, contemplation
shelves and citations never break. This is the technical foundation of the
library law ("no quotation is an orphan", `darshan_library_design.md`).

Decision record: `docs/decisions/0005-passage-id-scheme.md`.

## 1. Principles

1. **Identity from canon, not from layout.** An id encodes the passage's
   place in the work's canonical structure (book/canto/chapter/verse/
   aphorism/letter), never PDF pages, byte offsets or chunk indexes -
   canonical structure is the one thing that survives every reprocessing.
2. **Ids are immutable and never reused.** Once published in a bundle, an
   id always denotes the same text (or its corrected form).
3. **Drift is detected, not silently absorbed.** Every id carries a content
   fingerprint; when the underlying text changes (OCR fix, retranslation),
   the fingerprint changes and the pipeline must state why.
4. **Renderings are properties, not identities.** Original language,
   transliteration and translations of the same canonical unit share one id
   with different rendering channels - alignment is free by construction.

## 2. Format

```text
passage_id := {collection}.{work}(.{division})*.{unit}
collection := short registered code        cwsa | cwm | upanishads | gita |
                                            vedas | puranas | tantras | siddha ...
work       := slug registered in manifest  savitri | life_divine | isha | tirumandiram ...
division   := typed ordinal                bk1 | pt2 | cnt03 | ch12 | sec04 ...
unit       := typed ordinal                p0042 (paragraph) | v0113 (verse/line-group) |
                                            m01 (mantra) | a027 (aphorism) | l0311 (letter) |
                                            e19140101 (dated entry) | s196 (sutra)
```

Examples:

```text
cwsa.savitri.bk1.cnt1.v0001          Savitri, Book One, Canto One, first verse unit
cwsa.life_divine.bk1.ch01.p0003      The Life Divine, Book I, Chapter 1, 3rd paragraph
upanishads.isha.m01                  Isha Upanishad, mantra 1
gita.ch02.s47                        Bhagavad Gita 2.47
siddha.tirumandiram.t3.v0578         Tirumandiram, Tantra Three, verse 578
cwm.prayers_and_meditations.e19140101   Prayer of 1 January 1914
```

Rules: lowercase ASCII, dot-separated, ordinals zero-padded to the width
declared per work in its manifest (so lexicographic order = canonical
order). The typed prefix (`p`, `v`, `m`, `a`, `l`, `e`, `s`) makes the unit
kind self-describing.

## 3. Fingerprint and Drift

Alongside every id, the index stores:

```yaml
passage_id: cwsa.life_divine.bk1.ch01.p0003
fingerprint: sha256_16(normalized_text)   # first 16 hex chars
corpus_version: 2026.07                    # bundle that introduced/last touched it
```

Normalization before hashing: NFC unicode, collapse whitespace, strip the
page-anchor comments, lowercase nothing (case is text). A fingerprint change
without a manifest-declared reason (`ocr_correction`, `edition_change`,
`resegmentation`) fails CI.

## 4. Re-segmentation and Aliases

When editorial work splits or merges units (e.g. one long paragraph becomes
two), ids change - the old id is not deleted but aliased:

```yaml
# data/indexes/passage_aliases.yaml (accumulative, versioned)
- old: cwsa.life_divine.bk1.ch01.p0003
  new: [cwsa.life_divine.bk1.ch01.p0003a, cwsa.life_divine.bk1.ch01.p0003b]
  reason: resegmentation
  since: 2026.09
```

Resolution order everywhere (app, API, evals): exact id -> alias chain ->
parent division (graceful degradation: a broken verse link still lands on
the canto, never on a 404). Anthologies and shelves migrate lazily through
the same chain.

## 5. Renderings and Alignment

```yaml
passage_id: upanishads.isha.m01
renderings:
  sa-deva:  { source: upanishads/isha/original, fingerprint: ... }   # Devanagari
  sa-iast:  { source: derived_transliteration, fingerprint: ... }
  en-aurobindo: { source: cwsa.volume_17, fingerprint: ... }
```

The D5 layer (original) and comparative views read alignment straight from
the shared id. Where canonical structures differ across editions (verse
numbering variants), the manifest declares the numbering authority per work
and maps variants in an `edition_concordance` table - the id always follows
the declared authority.

## 6. Citation Payload

What the response contract carries per citation (spec section 4.1) becomes:

```yaml
citation:
  passage_id: gita.ch02.s47
  corpus_version: 2026.07
  quote_fingerprint: sha256_16(quoted_span_normalized)
```

Citation integrity (eval suite) then checks: id resolves (with aliases),
the quoted span exists inside the passage text, fingerprints match the
bundle. This makes "no invented citations" mechanically verifiable.

## 7. Implementation Order

1. Registry: collection/work codes + ordinal widths + numbering authority
   declared in the existing ingestion manifests.
2. Chunker (`scripts/chunk`) emits `passage_id` + `fingerprint` per unit,
   aligned to canonical structure per work type (verse works, prose works,
   letter/entry works).
3. Alias table + CI checks (fingerprint drift, id uniqueness, ordinal
   continuity).
4. Index and bundles key everything by passage_id; citation resolver in the
   agent API implements the resolution order.
