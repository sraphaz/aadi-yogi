# Darshan - The Path of Becoming

Darshan is not an app the seeker uses; it is a companion in the seeker's
becoming - the slow, daily work of becoming what the corpus calls, in many
tongues, a yogi: one whose ordinary life is progressively unified with
consciousness. This document designs how the application accompanies that
becoming in daily life, without ever certifying, ranking, or performing it.

Companions: `darshan_interface_concept.md` (principles),
`darshan_library_design.md` (the knowledge that feeds the path).

## 1. The Humility Clause

The traditions reserve "Adi Yogi" for the first yogi - the origin of yoga
itself. An application cannot make anyone a yogi, and this one never claims
to. What it can do, and what this design commits to, is faithfully tend the
conditions the sources themselves name: remembrance, sincerity, rhythm,
self-observation, consecrated work, study, silence. The becoming belongs to
the seeker and to Grace. The app tends the garden fence.

Consequences:

- no levels, ranks, certificates, or "spiritual progress scores";
- the seeker's stage is **self-declared and freely changeable**, used only to
  shape tone and emphasis;
- regression, pause and absence are treated with dignity (returning after a
  month is greeted with warmth, never with guilt or a broken streak).

## 2. The Four Postures of the Seeker

Instead of levels, four self-declared postures, drawn from the classical
typology of seekers (Gita 7.16) translated into modern honesty. The seeker
picks one in their own words; it can change any day.

| Posture | The seeker says | The app's emphasis |
| --- | --- | --- |
| **Touched** | "Something is calling; I don't know what." | Receive and Situate doors; D0-D1 depths; zero vocabulary assumed |
| **Seeking** | "I have questions I need to live with." | Inquiry; Living Maps; D1-D2; gentle practice offers |
| **Practicing** | "I keep a practice and want to deepen it." | Practice Field; rhythm weaving; D2-D4; concept lens |
| **Integrating** | "The practice must become my whole day." | Consecration of work; D4-D6; comparative study; the diary as record of sadhana |

The posture changes emphasis and default depth - never access. Everything is
open to everyone at all times.

## 3. The Day as the Ashram

The becoming happens in the seeker's actual day - work, family, conflict,
fatigue - not inside the app. Darshan therefore drapes itself over the
natural joints of a day, taking as its model the rhythm the Mother gave her
ashram: remembrance at waking, consecration before work, recollection in
action, examination at dusk, silence at night.

```text
DAWN      Darshan of the Word          one passage, one intention
MORNING   The Offering                 two lines: what is offered today
MIDDAY    The Remembrance (optional)   a single quiet line from the morning's
                                       passage, if the dawn bell was invited
DUSK      The Look-Back                three questions, no scoring
NIGHT     The Silence Room             and the app goes dark with the seeker
```

Rules of the rhythm:

- The whole arc takes **less than ten minutes of screen time per day**. The
  measure of the design is what happens in the other 23 hours 50 minutes.
- Every element is opt-in and independently removable; the **rhythm
  composer** lets the seeker weave their own day from these joints (a person
  who works nights can invert the whole arc; a parent can move the look-back
  to a lunch break).
- Bells (max two) carry one line and no teaser; missing every bell for a
  year produces exactly zero accumulated debt in the interface.

## 4. Life as Curriculum - the Situation Doors

The classical paths teach through life situations: the Gita begins in a
battlefield crisis; the Mother's correspondence answers school children about
fear and laziness. The **situation portal** (Library door "Situate") makes
life the entry point:

- doors named in human words: grief, fear, anger, work, love, decision,
  illness (of the restraint category - see crisis protocol), dryness of
  practice, joy (yes - a door for consecrating joy, not only for triaging
  pain);
- each door opens to one curated passage (D0/D1) + one offered micro-movement
  for that situation + the constellation for those who want more;
- micro-movements are karma-yoga sized: "before answering that message, one
  breath and inwardly offer the answer"; "do the next task as if it were the
  only one"; never programs, courses or 30-day challenges;
- doors of the restraint category (illness, despair, harm) follow
  `silence_and_non_answering.md`: fewer words, grounding, human support named
  plainly.

## 5. Study as Sadhana - svadhyaya in layers

The Library's seven depths (see `darshan_library_design.md`) are the study
dimension of becoming. What the becoming path adds is **sequence with
affection** - reading journeys, curated editorially, that turn the corpus
into a walkable curriculum without academizing it:

- **First Contact journeys** (posture: Touched): "Ten mornings with the
  Upanishads" - ten D0 words with D1 meanings, one per morning, ending in an
  open door to the Isha reading room. No quiz, no completion certificate;
  the journey simply ends where the book begins.
- **Foundation journeys** (Seeking/Practicing): the Gita in eighteen
  sittings (one chapter each, D3), with the concept lens pre-warmed for the
  chapter's key terms.
- **Deepening journeys** (Integrating): The Synthesis of Yoga part by part,
  paired with the corresponding practices in the Practice Field; Savitri
  canto by canto in the hour of dawn.
- Every journey is a **suggested order, not a course**: no enrollment, no
  progress percent, resumable and abandonable in dignity.

## 6. The Mirror - diary, anthology and the long arc

Becoming needs memory. Three mirrors, all private by architecture:

- **The Inner Diary** (spec 3.7): free writing; on invitation, the witness
  response can gently link an entry to the corpus ("what you describe, the
  Gita calls the sattwic doubt...") - one link, one citation, no analysis.
- **The Anthology**: passages kept across the years become the seeker's own
  book - the trace of their taste for truth, exportable, theirs.
- **The Season Letter** (opt-in, quarterly): the app composes a short letter
  to the seeker from their own kept passages and diary titles (never
  contents unless witness-invited), in the voice of a friend returning their
  own words: "this season you kept returning to surrender." No metrics, no
  comparisons, no year-in-review confetti. The letter can be turned off
  forever with one gesture.

## 7. What Success Looks Like

The becoming path succeeds when the app matters less: when the dawn word is
remembered at noon without the bell; when the offering happens with the
hands already on the work; when the seeker reads the Gita on paper and only
returns to Darshan for the concept lens; when the Silence Room is empty
because the silence has moved into the house. The presence metrics of
`darshan_interface_spec.md` section 6 are proxies for exactly this - and the
final metric has no sensor.
