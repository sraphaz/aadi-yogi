# Darshan Sky Map - Design

Gesture 8 of the Darshan interface: a map of the sky the seeker can consult in
daily life - the outer sky of real cosmic rhythm and the inner sky of their
own planes of being (physical, energetic, emotional, mental, spiritual). One
map, two hemispheres, consulted the way one steps outside to read the weather
before choosing a coat.

Companions: `darshan_interface_concept.md`, `darshan_interface_spec.md`,
`darshan_becoming_path.md` (the day as ashram).

## 1. The Integrity Boundary First

The project's boundaries (`docs/project_vision.md`) forbid prophecy,
deterministic claims and unsupported revelation. The Sky Map is therefore
built on one sentence:

```text
The sky is rhythm, not fate.
The map describes conditions; it never predicts outcomes,
never assigns causes to a person's life,
and never claims to know the seeker's inner state -
it mirrors what the seeker observes.
```

Explicitly out of scope, permanently: natal charts, horoscopes, predictive
astrology, auspicious/inauspicious verdicts about a person's decisions,
planetary "influences" stated as fact. Where the corpus documents jyotisha as
a traditional discipline, that material lives in the Library as documentary
knowledge (D2-D6, cited), not as a live instrument pointed at the seeker.

## 2. The Outer Sky - Rhythms of Heaven

What the traditions actually keep time by, computed from real astronomy,
rendered as a contemplative sky.

### Content

| Rhythm | What is shown | Source ground |
| --- | --- | --- |
| Sun | sunrise, sunset, solar noon, the two sandhyas (junctions), brahmamuhurta | Vedic daily rhythm; the Mother's ashram schedule |
| Moon | phase as drawn sky, tithi (lunar day), purnima / amavasya / ekadashi observances | pan-Indian lunar calendar |
| Season | the six ritus (vasanta, grishma, varsha, sharad, hemanta, shishira) with hemisphere awareness | Vedic/Ayurvedic seasonal wisdom |
| Festivals | major observances (Mahashivaratri, Navaratri, Guru Purnima, darshan days of the Ashram calendar) | corpus calendars |
| Sky itself | a quiet drawn sky matching the actual moment - moon where the moon is, dawn when dawn is | local astronomy, computed on device |

### Behavior

- Opens as a **drawn sky**, not a data dashboard: the dome of the hour with
  the moon in its true phase, the sun's arc, the season's signature at the
  horizon. Numbers appear only on request.
- Every rhythm element opens the depth dial into the Library: tap the full
  moon and D2 offers what the traditions say of purnima - cited passages,
  never app-invented lore.
- Observances are rendered as **invitations, never obligations**: "tonight is
  ekadashi; some traditions keep it with lightness of food and study" - one
  line, sources behind it, no tracking of whether the seeker "kept" anything.
- All astronomy is computed locally (ephemeris math, no network, no third
  party); location is device-side and never leaves it; a seeker who denies
  location gets a sky by city choice or a generic hemisphere sky.
- The rhythm composer (`darshan_becoming_path.md` section 3) can bind to the
  real sky: the dawn word at actual brahmamuhurta, the look-back at actual
  sunset - making the app's day follow heaven's day, not the clock's.

## 3. The Inner Sky - the Map of the Planes

The hemisphere the seeker consults about themselves. Its ground is the
ontology the traditions share and Sri Aurobindo made precise: the being has
instruments - physical, vital/energetic, emotional, mental - and a soul
behind them, with the spiritual above (`content/ontology/concepts.md`,
`states_of_consciousness.md`).

### The five skies

Rendered as five bands of one sky, each with its own weather:

| Plane | Traditional ground | Weather the seeker might mark |
| --- | --- | --- |
| Physical (annamaya, sthula) | body, fatigue, illness, vigor | clear, heavy, restless, depleted, strong |
| Energetic / vital (pranamaya, prana-kosha) | life-force, desire, drive | full, agitated, scattered, flat, flowing |
| Emotional (the heart, chitta) | feeling, relation, mood | open, clouded, storming, tender, dry |
| Mental (manomaya) | thought, clarity, doubt | clear, racing, foggy, rigid, quiet |
| Spiritual (the psychic behind, the above) | aspiration, remembrance, Presence | near, veiled, calling, forgotten, still |

### Behavior - self-observation, mirrored

- **The seeker marks the weather; the app never marks it for them.** A
  consultation is thirty seconds: five bands, one touch per band, in the
  seeker's own sensing. Skipping bands is normal; marking one is enough.
- The map then **mirrors**: the five bands render as one inner sky (the
  vital storming under a clear mind is *visible* as a picture) - and the
  mirror is the intervention: seeing the weather already separates the seer
  from the storm (witness consciousness, `states_of_consciousness.md`).
- After mirroring, one quiet offer, never more: a passage or micro-movement
  fitted to the dominant weather, through the ontology's practices and the
  situation-door corpus ("storm in the vital: the Gita on the tempest of the
  senses", D0 with the dial behind it). Restraint weathers (despair-grade
  emotional storm, physical illness) follow the crisis protocol - fewer
  words, grounding, human support.
- **Consent bridge with the Inquiry**: if the seeker asks a question right
  after consulting the map, they may attach the map with one gesture; the
  state detector receives it as context. Never automatic.
- **The seeker's own patterns, privately**: consultations accumulate
  local-first and encrypted (diary-grade, NFR-001 class). The map can show
  the seeker their own skies across a season - "your vital tends to storm at
  dusk" - as *their* observation reflected, never as diagnosis, never
  leaving the device, never profiled.

### What the inner sky is not

Not a mood tracker with streaks; not a diagnostic instrument; not visible to
the engine without per-consultation consent; not scored, compared, or
gamified. There is no "good" sky - shishira is not a failure of vasanta.

## 4. One Map, Consulted in Daily Life

The two hemispheres compose one consultation, designed to fit inside a
minute at a bus stop:

1. open the map - the outer sky is already there (no input needed);
2. optionally mark the inner sky (five touches at most);
3. receive the mirror and, at most, one quiet offer;
4. close - or press anything into the Library for depth.

The map is also the eighth card of the Court, and its miniature (current
moon + season glyph, never inner data) may sit in the Court's corner as the
app's only ambient element.

## 5. Data and Corpus Requirements

- ephemeris computation on device (sun/moon positions, phases, tithis);
  hemisphere-aware season logic - the creators' darshan repo already
  implements this core (Swiss Ephemeris / mhah-panchang resolver and a
  layered Time Pulse system); see `darshan_reuse_map.md`;
- observance calendar as corpus data (`content/` calendars, editorially
  maintained, cited);
- passage curation per rhythm (purnima, sandhya, seasons) and per inner
  weather (plane x weather -> passages/practices), flowing from the ontology
  enrichment pipeline (`darshan_library_design.md` section 6);
- as the corpus grows (new imports arriving), the map's Library links deepen
  automatically through facets - the map itself never invents content.
