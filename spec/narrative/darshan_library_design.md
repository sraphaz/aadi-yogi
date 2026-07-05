# Darshan Library - Design in Layers of Depth

The Library is the heart of Darshan. This document designs it with care: how
the knowledge is classified, how it is consulted, and how it reveals itself in
layers of depth - from a single line received at dawn to the complete book,
the original passage, and the original language.

Companion documents: `darshan_interface_concept.md` (gesture 6),
`darshan_interface_spec.md` (section 3.6), `darshan_becoming_path.md` (how the
Library serves the seeker's becoming).

## 1. The Law of the Library

```text
No quotation is an orphan.
Every line shown anywhere in the application can be followed,
in unbroken steps, to the complete work it came from -
and, where it exists, to the original language.
```

This single law produces most of the design. It is the opposite of the
content-farm pattern (decontextualized quotes floating free) and the opposite
of the academic pattern (context so heavy the living word suffocates). Darshan
holds both ends: the lightness of one line, the integrity of the whole book.

## 2. The Seven Depths

Every unit of knowledge in the corpus can be encountered at seven depths. The
seeker moves between them with one continuous gesture - the **depth dial** -
never losing their place. Each depth is complete in itself; none is
obligatory; the deeper ones are always present but never pushed.

```text
D0  The Word         one line, alone on the screen
D1  The Meaning      a plain-language rendering, one short paragraph
D2  The Passage      the excerpt in its immediate context, fully cited
D3  The Section      the complete chapter / canto / hymn, readable whole
D4  The Book         the complete work, in its reading room
D5  The Original     source language - Sanskrit, Tamil, French - with
                     transliteration and, where available, word-by-word senses
D6  The Constellation  the passage among the traditions: parallels,
                     differences, ontology concepts, related practices
```

### How the depths behave

- **D0 - The Word.** The daily darshan, a line inside an Inquiry answer, a
  station teaching in a Living Map. Typographically honored, always carrying
  its invisible thread to D2+.
- **D1 - The Meaning.** One paragraph in the engine's voice: what this says,
  plainly, without flattening. Written under the response contract (cited,
  humble, no certainty performance). This is the depth for the person who has
  never opened an Upanishad.
- **D2 - The Passage.** The actual source text around the line - the verses
  before and after, the letter in full, the aphorism with the Mother's
  commentary. The citation becomes visible here as lineage: work, section,
  translator, edition.
- **D3 - The Section.** The chapter of The Life Divine, the canto of Savitri,
  the complete hymn, the full talk. Reading typography, position memory,
  estimated reading time stated calmly (never as pressure).
- **D4 - The Book.** The complete work in its reading room, with its own
  table of contents, introduction, and provenance page (edition, copyright
  status, how it entered the corpus). For restricted works
  (`docs/copyright_policy.md`) D4 presents the metadata record and the
  dignified path to the official source - the law of no-orphan-quotations
  includes honesty about where the corpus must point outward.
- **D5 - The Original.** Devanagari for Sanskrit, Tamil script for the
  Tirumandiram, French for the Mother. Transliteration (IAST) shown in
  parallel; word-by-word glosses where the corpus has them (e.g. Sri
  Aurobindo's own Vedic word studies). The seeker can hear the original where
  licensed audio exists. This depth teaches reverence: the translation is a
  window, not the house.
- **D6 - The Constellation.** The passage placed among the traditions: the
  ontology concepts it touches, parallel passages elsewhere in the corpus
  (Isha's "kurvann eveha karmani" beside the Gita's karma yoga beside the
  Mother's consecration of work), explicit difference blocks where the
  traditions genuinely diverge, and the practices the passage informs. Built
  from `content/ontology/` and the retrieval index; every parallel is a real
  passage, never a generated paraphrase.

### The depth dial in the hand

One vertical gesture (or two keys) moves through depths; the current depth is
always named; entering and leaving a depth never loses reading position at
any other depth. From any Inquiry answer, any daily word, any map station:
press into the quote and the dial opens at D2, with D0/D1 above and D3-D6
below.

## 3. Classification - the Facets

The corpus is classified along seven facets, all drawn from existing
repository structures, so classification is data, not opinion:

| Facet | Source of truth | Examples |
| --- | --- | --- |
| Tradition | frontmatter `tradition` | vedic, upanishadic, gita, puranic, tantra, siddha, integral_yoga |
| Canon | `content/sources/` hierarchy | collection -> work -> book/part -> section -> passage |
| Theme | frontmatter `themes` + ontology | surrender, evolution, death_and_immortality, work |
| Concept | `content/ontology/concepts.md`, `sanskrit_terms.md` | psychic_being, tapas, prana, shraddha |
| Practice | `content/ontology/practices.md` | japa, consecration_of_work, self_observation, silence |
| State / situation | `states_of_consciousness.md` + living maps | grief, doubt, aspiration, conflict, decision |
| Depth readiness | editorial field | first_contact, practitioner, source_dense |

Rules of the facets:

- Facets combine ("siddha texts about the body, source_dense") but the
  interface shows at most two active facets at once - browsing must stay
  contemplative, not become a database session.
- The **state/situation facet is the bridge of affection**: it lets a person
  arrive with their life ("I am grieving", "conflict at work", "I cannot
  decide") and be met by classified wisdom without needing to know any
  tradition's vocabulary. This facet always routes through the response
  contract's state detection, so a crisis arrival is met with restraint, not
  with a search-results page.
- `depth_readiness` is editorial kindness, not gatekeeping: everything is
  open to everyone; the field only shapes ordering and the gentleness of the
  introduction.

## 4. The Six Doors of Consultation

Six ways in, for six postures of seeking. All six converge on the same
passages and the same depth dial.

1. **Receive** (no intention needed): the daily Word arrives; the dial does
   the rest. For the person who does not yet know what to ask.
2. **Ask** (a question): the Inquiry oracle. Its contemplation pages are
   woven from D2 passages; every quotation opens the dial.
3. **Situate** (a life moment): the situation portal - a small, warm set of
   doors ("grief", "fear", "work", "love", "decision", "practice is dry")
   leading to a curated first passage plus its constellation, in the right
   guidance mode for that state.
4. **Browse** (curiosity): facet browsing - by tradition, theme, concept,
   practice - rendered as a calm garden of entries, not an infinite grid.
5. **Study** (discipline): the reading rooms - complete works, canonical
   order, table of contents, bookmarks, concept lens active in the margin.
6. **Follow** (a path): the Living Maps - each station opens its teachings
   at D2 with the dial available, so a map quietly becomes a curriculum.

Search serves all doors: exact search (works offline over the local corpus)
and semantic search (online, retrieval index), always filterable by facet,
always returning passages-with-provenance, never snippets without a home.

## 5. The Reading Rooms

Where the complete books live. Designed with the affection one gives to a
physical library:

- **The shelf**: collections presented as quiet shelves (Vedas, Upanishads,
  Gita, Puranas, Tantras, Siddha texts, Complete Works of Sri Aurobindo,
  Collected Works of the Mother), each with a one-paragraph introduction of
  its spirit, not marketing copy.
- **The room**: one work, its table of contents, its provenance page, its
  reading surface. Long-form typography (D3/D4), hour-aware light, offline
  once visited, position memory forever.
- **The margin**: the concept lens lives in the margin - marked terms open
  tradition-by-tradition senses without leaving the page; a margin note can
  be kept privately (feeds the seeker's anthology, never any index).
- **The threshold of the room**: entering a book for the first time offers
  its D1 - "what this work is, in one breath" - then leaves the seeker alone
  with the text.
- **The anthology**: passages the seeker keeps assemble into a personal
  anthology (their own "book of hours"), organized by their own facets,
  exportable as plain Markdown - the seeker's data is the seeker's.

## 6. Editorial Pipeline for Depth

What must exist in the corpus for the seven depths to be real (extends
`docs/digitalization_pipeline.md`):

1. **Passage segmentation**: chunking (`scripts/chunk`) must produce units
   aligned with canonical structure (verse, aphorism, letter, paragraph-in-
   chapter), each with a stable passage id - the anchor of the whole design.
2. **D1 renderings**: engine-generated plain meanings are drafted in batch,
   then editorially reviewed before being served as static content (they are
   content, not live generation - reviewable, versionable, correctable).
3. **Parallels index**: cross-tradition parallels curated as data
   (`content/synthesis/comparative_views/`), seeded by retrieval similarity,
   confirmed by editorial review. A parallel without review renders with an
   explicit "machine-suggested parallel" mark.
4. **Original alignment**: where original-language sources are imported,
   verse-level alignment tables map translation passages to original
   passages (starting with texts where Sri Aurobindo's own translations sit
   beside the Sanskrit he translated - already in the CWSA corpus).
5. **Facet enrichment**: theme/concept/practice tagging at passage level,
   machine-proposed, editorially confirmed, stored in chunk metadata.
6. **Depth readiness marks**: editorial pass assigning `first_contact` /
   `practitioner` / `source_dense` per work and, where useful, per section.

Every editorial state is visible in the interface as quiet honesty: reviewed
renderings carry no mark; machine-drafted ones say so.

## 7. What This Feels Like (three moments)

**Maria, who has never read scripture.** At dusk she opens the situation door
"grief". She receives one line from the Katha Upanishad (D0), reads its plain
meaning (D1), and stops there. Three days later she presses deeper and finds
the passage (D2) - Nachiketas at the door of Death - and one evening, without
noticing the transition, she is reading the whole first valli (D3). Nothing
ever told her to go deeper. The depth was simply always there, warm, one
gesture away.

**Rafael, a practitioner.** In the Gita's reading room (D4) he keeps meeting
the word "yajna". The concept lens in the margin opens its senses - Vedic
sacrifice, the Gita's offering of works, the Mother's consecration. He turns
the dial to D6 and finds the Isha Upanishad and the Synthesis of Yoga holding
the same fire from different sides, with one difference block naming what
Vedanta and Tantra do differently with renunciation. He keeps two passages;
his anthology grows by one page.

**Ana, in a hard week.** She asks the Inquiry a question that is really about
fear. The state detection leads with acknowledgment; the answer quotes one
line of Savitri. She presses into the quote - D2 shows her the passage in
Canto Nine; D5 shows her the line in its metrical body. She does not read
more that night. The app offers the Silence Room, and she takes it.
