# Darshan Interface - Specification

Companion to `darshan_interface_concept.md`. That document says why; this one
says what and how. A complete Sky-Forge maturity package (brief, functional
requirements, NFRs, UX spec, design tokens, market benchmark, C4 model, SKY
merit indices, maturity, journey) lives in `docs/skyforge/darshan/`, formatted
for direct import as a Sky-Forge session.

Two deepening documents extend this specification:

- `darshan_library_design.md` - the Library in layers of depth: the seven
  depths (D0-D6), the depth dial, classification facets, the six doors of
  consultation, reading rooms, and the editorial pipeline that makes depth real.
- `darshan_becoming_path.md` - how the application accompanies the seeker's
  becoming in daily life: the four postures, the day as ashram, situation
  doors, reading journeys, and the mirrors (diary, anthology, season letter).
- `darshan_sky_map_design.md` - gesture 8: the outer sky of real cosmic
  rhythm and the inner sky of the five planes, with the rhythm-not-fate
  boundary.
- `darshan_nature_health_design.md` - gesture 9: elements, land, body,
  health and longevity heritage inside a three-tier responsibility fence.
- `darshan_reuse_map.md` - what to reuse, adapt or consciously not reuse
  from the already-implemented oracle at github.com/sraphaz/darshan
  (ephemeris core, time pulse, sacred remedy engine, twelve-petals filter,
  Next.js shell).

## 1. Product Definition

- **Working name**: Darshan (interface layer of the Aadi Yogi engine).
- **Form**: progressive web application, mobile-first, installable, with the
  reading surfaces usable offline.
- **Users**: seekers, students of the traditions, practitioners of integral
  yoga; explicitly not positioned as therapy, religion-as-a-service, or
  entertainment.
- **Engine**: the Aadi Yogi architecture already defined in
  `docs/architecture.md` (sources -> chunking -> embeddings -> retriever ->
  consciousness-aware prompt builder -> agent API), with the consciousness
  core (`content/consciousness_core/`) as the behavioral law.

## 2. Information Architecture

Seven quiet surfaces, one hidden room. No global feed. No home dashboard.

```text
Threshold (entry ritual)
└── The Court (single calm hub, one gesture per card)
    ├── Darshan of the Word   (daily passage)
    ├── Inquiry               (oracle; contemplation pages)
    ├── Living Maps           (guided inner journeys)
    ├── Practice Field        (silence, offering, evening look-back, japa)
    ├── Library               (reading rooms, concept lens, comparisons)
    ├── Sky Map               (outer rhythm + inner weather; see 3.8)
    ├── House of Nature       (elements, body, health heritage; see 3.9)
    ├── Inner Diary           (private journal, witness mode)
    └── Silence Room          (mauna mode; also reachable from anywhere)
```

Navigation rule: maximum one level of depth from the Court. Every surface has
an explicit closing gesture that returns through the Court or ends the
session with a short farewell line and no re-engagement hook.

## 3. Screens and Flows

### 3.1 Threshold

- Cold start: full-bleed quiet background attuned to local hour (pre-dawn,
  day, dusk, night palettes). A breath cue (~4s in, ~4s out) plays once.
- All backend warm-up happens behind the breath; no spinners anywhere in the
  app. If loading exceeds the breath, the cue simply continues.
- Skippable by a single tap for accessibility and for users who have chosen
  "direct entry" in settings (non-coercion applies to the ritual itself).

### 3.2 Darshan of the Word

- One passage per calendar day, selected by a curation policy:
  seasonal/festival awareness -> seeker's active living map -> otherwise a
  curated rotation across all traditions in the corpus.
- Rendering: passage alone, large type, generous margins, fade-in at reading
  pace; source line beneath (work, section, tradition); optional "hear the
  original" (e.g. Sanskrit audio) when licensing permits.
- One optional deepening: a short source-grounded commentary (engine-generated,
  citation-first, guidance mode: source_commentary).
- Terminal state: a closing mark. No "next", no archive scrolling by default;
  yesterday's word is gone the way a day is gone. (A settings-level
  "remembered words" list exists for accessibility and study, off by default.)

### 3.3 Inquiry (the oracle)

Flow:

1. **Composing**: a single text field in an empty screen. Placeholder rotates
   between gentle prompts ("What is moving in you?"). While composing, the
   engine performs no streaming, no autocomplete - composition is private.
2. **Deepening (conditional)**: at most one clarifying reflection before
   answering, and only when the question's state detection is ambiguous
   ("There may be two questions here - which one matters tonight?").
3. **Contemplation page**: the response is delivered as one composed page,
   not chat bubbles:
   - a short answer body in the voice defined by
     `content/consciousness_core/voice.md`;
   - inline source quotations, each visibly cited and linked into the Library;
   - when traditions differ, a "the traditions differ here" block naming the
     difference instead of averaging it;
   - at most one offered movement (practice suggestion), clearly optional;
   - possible endings: plain close, a returned question, or **honored
     silence** (see 4.3).
4. **Resting**: after a page is delivered, the interface offers three exits -
   sit with it (opens Silence Room), keep it (saves to contemplation shelf),
   or leave. Asking a follow-up is possible but the input field reappears
   only after a short interval (~one breath), preserving the rhythm of a well,
   not a slot machine.

Contemplation pages are permanent, reread-able artifacts with their sources
attached; the shelf is a small stack, not a history log.

### 3.4 Living Maps

- Maps are rendered from `content/ontology/living_maps/` (ego to psychic
  being, suffering to conscious growth, aspiration path, surrender path).
- A map is a vertical path of stations. Each station: one teaching (cited),
  one reflection question, one offered movement. Advancing is always manual;
  the map never nags, never expires, and moving backwards is a first-class
  gesture ("return to an earlier station") without any loss framing.
- Time grain: stations suggest "stay here some days"; the interface never
  shows progress percentages.

### 3.5 Practice Field

- **Silence timer**: duration chosen by a slow dial; screen darkens to near
  black; a single closing bell. No stats page afterwards - only "received."
- **Offering**: a two-line ritual before work ("What is offered today?"),
  stored privately, optionally echoed at dusk.
- **Evening look-back**: three fixed questions in the Mother's spirit
  (What was sincere? What resisted? What is asked of tomorrow?), free text,
  no scoring, feeding nothing but the seeker's own diary.
- **Japa support**: optional counter with haptic-only feedback, screen off
  friendly.

### 3.6 Library

- Reading rooms per collection (Upanishads, Gita, Vedas, Puranas, Tantras,
  Tirumandiram, CWSA, the Mother's records), typeset for long-form reading,
  offline-capable, with position memory.
- **Concept lens**: tapping a marked term (from `content/ontology/`) opens a
  side panel: definition, tradition-by-tradition senses, related practices,
  and "where the traditions differ".
- **Comparative view**: two passages side by side with an engine-written,
  cited comparison that names differences explicitly (guidance mode:
  comparative_philosophy).
- Every quotation anywhere in the app deep-links here, to the passage in
  context - citation as lineage, not liability.
- Restricted works (per `docs/copyright_policy.md`) surface as metadata
  records with guidance to the official sources; the interface never renders
  reconstructed text of a restricted volume as if it were quotation.

### 3.7 Inner Diary

- Local-first storage, encrypted at rest with a key derived from the user's
  credential; never used for retrieval training, profiling, or any metric.
- Default mode: pure writing surface. The engine is architecturally blind to
  it.
- **Witness mode** (explicit invitation per entry): the engine reads the
  invited entry only, responds once as a witness - reflecting the seeker's own
  words, offering at most one source resonance with citation - and does not
  retain the entry in any index.
- Diary content never influences Inquiry answers unless the seeker pastes it
  there themselves.

### 3.8 Sky Map

Full design in `darshan_sky_map_design.md`. Contract essentials:

- **Outer sky**: sun, moon/tithi, season and observances computed on device
  (local ephemeris, no network, location never transmitted); rendered as a
  drawn sky; every element opens the depth dial into cited sources;
  observances are invitations, never obligations or tracked duties.
- **Inner sky**: five bands (physical, energetic, emotional, mental,
  spiritual); the seeker marks the weather, the app mirrors it as one sky
  and offers at most one passage or safe movement; restraint-grade weather
  routes to the crisis protocol.
- **Privacy**: inner-sky consultations are diary-grade (local-first,
  encrypted, never profiled, never visible to the engine without a
  per-consultation consent gesture that attaches the map to an Inquiry).
- **Hard boundary**: no natal charts, horoscopes, predictions or
  auspiciousness verdicts anywhere; jyotisha material in the corpus renders
  only as documentary Library content.
- The rhythm composer may bind bells to the real sky (dawn word at
  brahmamuhurta, look-back at actual sunset).

### 3.9 House of Nature

Full design in `darshan_nature_health_design.md`. Contract essentials:

- Rooms: the Elements (pancha mahabhuta, also a Library facet), the Land,
  the Body as Temple (dinacharya, ritucharya, mitahara), Long Life (Siddha
  kaya kalpa heritage), Healing Memory (traditional medicine as documentary
  library).
- **Heritage notice** permanently visible on every surface of the House:
  cited heritage, not medical advice; accompanies qualified care, never
  replaces it.
- **Three tiers enforced by content tagging**: safe (offerable as
  micro-movements), documentary (readable, cited, marked "under qualified
  guidance traditionally; not instructed here"), closed (never rendered as
  guidance; routes to crisis protocol).
- Illness-related arrivals and questions always take the restraint posture
  of the consciousness core.
- **Double editorial gate**: health-touching content requires editorial +
  safety review before rendering above D2; collections flagged
  `health_sensitive` in their import manifests cannot skip it.
- **Living corpus states**: rooms render as open / arriving / future as the
  parallel import work lands new collections - honestly, never as vaporware.

### 3.10 Silence Room

- Reachable from every surface with the same gesture (long-press anywhere on
  the chrome, or a persistent minimal glyph).
- Near-black screen, one slow luminous pulse (breath pace), no text, no
  timer, no exit prompt. Exit by the same gesture.
- The application treats time in this room as the most successful time it can
  host, and correspondingly it is the only "feature" with zero telemetry.

## 4. The Response Contract

Every Inquiry answer is produced under a contract enforced by the agent API
and audited by the evaluation suite.

### 4.1 Envelope

```yaml
response:
  state_detected: aspiration | pain | confusion | crisis | grief | doubt |
                  devotional_opening | philosophical_inquiry | ...   # states_of_response.md
  guidance_mode: orientation | study | practice | symbolic_interpretation |
                 comparative_philosophy | source_commentary |
                 cautionary_guidance | silence_contemplation           # guidance_modes.md
  body: composed answer text (voice.md rules)
  citations: [{source_id, passage_ref, tradition}]   # required when body makes source claims
  differences: [{topic, positions: [{tradition, position}]}]  # optional, never flattened
  offered_movement: {text, safety_class} | null       # at most one, always optional
  closing: plain | returned_question | honored_silence
```

### 4.2 Hard rules

- No source claim without a real citation resolvable in the Library
  (no invented citations - `docs/project_vision.md`).
- No prophecy, no deterministic life predictions, no medical or psychiatric
  instruction; symbolic interpretation is probabilistic by construction.
- Restricted-copyright works may be referenced and pointed to, never quoted
  beyond fair-use excerpt policy (`docs/copyright_policy.md`).
- Tone always passes the voice rules; "guru performance" phrasings are
  eval-tested against `content/consciousness_core/examples/bad_answers.md`.

### 4.3 Honored silence and the crisis protocol

- When state detection lands in the restraint cases of
  `content/consciousness_core/silence_and_non_answering.md` (kundalini
  claims, voices, health, psychiatric crisis, death decisions, occult
  practice...), the contract forces `guidance_mode: cautionary_guidance` or
  `silence_contemplation`: fewer words, grounding first, explicit
  encouragement toward qualified human support, and - where legally advisable -
  region-appropriate crisis resources.
- Honored silence is rendered as a dedicated page: a short acknowledgment
  ("This deserves more silence than words"), one grounding pointer, and the
  Silence Room offered. It is counted in evaluations as a success mode, not a
  failure fallback.

## 5. State, Rhythm and Atmosphere

- **Hour awareness**: palette, pacing and the Court's ordering shift with
  local time (dawn favors the Word; dusk favors the look-back). No content is
  locked by time - only emphasis.
- **Session arc**: every session has an implicit arc (threshold -> one or two
  gestures -> closing). After ~2 gestures the Court begins to surface the
  closing gesture more prominently. The app will end a session gracefully but
  will never guilt, count, or streak.
- **Notifications**: none by default. The seeker may explicitly invite up to
  two daily bells (dawn word, dusk look-back) which arrive as a single quiet
  line and never contain content teasers.

## 6. Presence Metrics and Evaluation

Implemented in `packages/evals` alongside answer-quality suites:

| Metric | Definition | Direction |
| --- | --- | --- |
| closure_rate | sessions ended via closing gesture / all sessions | up |
| rhythm_steadiness | dispersion of visit hours around the seeker's own rhythm | stable |
| depth_ratio | contemplation pages reread + sources opened / questions asked | up |
| movement_adoption | offered movements marked "tried" (self-report) | up |
| honored_silence_precision | eval-audited correctness of silence/caution decisions | up |
| citation_integrity | resolvable citations / citations rendered | = 1.0 |
| petal_filter_pass | answers passing the Twelve Petals rubric (peace vs agitation, opens consciousness vs fixes identity, sincerity vs fear - adopted from the darshan repo) | up |

Explicitly forbidden as targets: session length, DAU/retention curves,
questions per user, notification opt-in rate.

## 7. System Mapping (to this monorepo)

| Layer | Home | Responsibility |
| --- | --- | --- |
| Corpus | `content/sources/` | canonical texts + metadata records |
| Ontology | `content/ontology/` | concept lens, living maps, term marking |
| Behavior law | `content/consciousness_core/` | states, modes, voice, silence doctrine |
| Chunking/index | `scripts/chunk`, `scripts/index`, `packages/ingestion` | retrieval units with provenance |
| Retrieval | `packages/rag` | tradition-aware retriever with citation payloads |
| Prompting | `packages/prompts` | consciousness-aware prompt builder (state x mode matrix) |
| Agent API | `apps/agent-api` | response contract enforcement, crisis protocol, rate rhythm |
| Interface | `apps/web` | the seven gestures + silence room (PWA) |
| Evaluation | `packages/evals` | golden questions, tone/safety audits, presence metrics |

## 8. Non-Functional Requirements (summary)

Full detail in `docs/skyforge/darshan/nfr.yaml`.

- **Privacy**: diary local-first and encrypted; no third-party analytics; no
  advertising ever; anonymous use as the default mode.
- **Accessibility**: WCAG 2.1 AA; every ritual element (breath, fades,
  silence room) has a reduced-motion and screen-reader-honest equivalent;
  rituals are skippable.
- **Latency posture**: answers may take seconds - the interface absorbs
  latency into contemplative pacing rather than demanding sub-second LLM
  calls; hard ceiling before an honest "still composing" state: 20s.
- **Offline**: Library reading rooms, daily word (prefetched), practice
  field, and diary work offline; Inquiry requires connection and says so
  plainly.
- **Languages**: English and Portuguese at launch; source quotations remain
  in their canonical language with translation where licensed.
- **Integrity**: citation resolution rate of 1.0 enforced by CI evals;
  copyright policy enforced at index build time, not at prompt time.

## 9. Build Phases

1. **Seed**: Threshold, Court, Darshan of the Word, Library reading rooms
   (static, offline), Silence Room. No LLM required - this phase already
   embodies the design dharma and ships value from the imported corpus.
2. **Voice**: retrieval + response contract + Inquiry with contemplation
   pages; honored-silence and crisis protocols; evaluation suites live
   before public exposure.
3. **Path**: Living Maps, Practice Field, concept lens, comparative view;
   the Sky Map's outer hemisphere (local ephemeris, observance calendar,
   sky-bound rhythm composer).
4. **Witness**: Inner Diary with witness mode; the Sky Map's inner hemisphere
   with private patterns; presence metrics dashboards (internal);
   notification bells (opt-in).
5. **Ground**: the House of Nature, opening room by room as the parallel
   corpus imports land and pass the double editorial gate (element rooms
   first - they draw on the already-imported corpus; healing memory last).
6. **Sangha (exploratory, unscheduled)**: shared silence sittings and
   study circles - only if it can be done without social-media dynamics.
