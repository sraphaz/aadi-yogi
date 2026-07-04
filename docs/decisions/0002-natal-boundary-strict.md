# ADR 0002 - Natal Boundary: Strict

Status: accepted (decided from the consciousness core; creators calibrate)

## Context

The darshan repository computes personal natal readings (birth date/time/
place -> jyotish chart, numerology, human design; love/career/year
readings). The Darshan interface design excludes personal astrological
interpretation (`darshan_sky_map_design.md` section 1, RF-031, NFR-016).
`docs/darshan_reuse_map.md` section 3 recorded the open choice: strict
posture or documentary bridge.

## What the Consciousness Says

- **Vision boundaries** (`project_vision.md`): "no prophecy-like dream
  interpretation... no unsupported revelation claims" - personal predictive
  reading is the paradigm case.
- **Voice** (`voice.md`): avoid "deterministic statements"; a natal reading
  is deterministic by genre, whatever disclaimers it carries.
- **Silence doctrine** (`silence_and_non_answering.md`): prophecy-like
  interpretation is a restraint case - the wise response is less claim, not
  more.
- **Non-coercion and identity**: the darshan repo's own protocol says "não
  rotular identidades" - natal typing (your nakshatra is X, your type is Y)
  labels identity at the root.

## Decision

**Strict posture.**

1. The application never collects birth data. No natal chart, numerology or
   human-design computation exists in any code path.
2. The ephemeris serves only the shared sky of now (the Sky Map's outer
   hemisphere) - the same sky for everyone in a place.
3. Jyotisha texts in the corpus remain fully readable as documentary
   Library content (D2-D6, cited), honoring the tradition as knowledge.
4. "Read my chart" requests receive the gentle rhythm-framed refusal
   already specified (NFR-016), pointing to the outer sky and the inner
   sky's self-observation instead.
5. From the darshan repo, the natal engines (`lib/engines/`,
   `lib/readings/` natal parts) are the one area **not** ported; everything
   else in the reuse map stands.

## Consequences

- The inner sky remains the only "personal map" - authored by the seeker's
  own observation, never by the stars about them.
- The open question in `darshan_reuse_map.md` section 3 is closed; journey
  action `natal_boundary_decision` resolved.
