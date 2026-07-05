# Reuse Map - sraphaz/darshan -> Darshan Interface

An implemented oracle already exists: [sraphaz/darshan](https://github.com/sraphaz/darshan)
("Luz do Tempo", Next.js 15, MIT). Its philosophy is convergent with this
design - "não prevê; revela", revelation in layers, governance by the
Mother's Twelve Petals, a petal filter before every answer. This document
maps what the Darshan interface should reuse, adapt, or consciously not
reuse from that codebase.

## 1. Reuse As-Is (proven, aligned)

| Asset | Where it lives there | Serves here |
| --- | --- | --- |
| Ephemeris core with provider resolver (Swiss Ephemeris / mhah-panchang) | `lib/core/ephemerisResolver.ts`, `providers/` | Sky Map outer sky (RF-030, INT-006): sun/moon positions, tithi, offline |
| Time Pulse system (layered "now": daily cycle, lunar phase, season) | `lib/timepulse.ts`, `docs/TIME_PULSE_SYSTEM.md` | Outer sky rhythm model; "moon language" copy is already non-fatalist ("lua crescente: tempo de construir") |
| Multi-provider AI gateway (OpenAI / Anthropic / Gemini) | `lib/ai/` | Agent API LLM abstraction (INT-001, C4 ADR 4) |
| Auth by e-mail code + Google OAuth, cookie session | `lib/auth.ts`, `app/api/auth/` | Anonymous-first with optional account (INT-003) |
| Ritual revelation flow (phased reveal UX) | `docs/RITUAL_REVELATION_FLOW.md`, `DarshanReveal.tsx` | Contemplation page pacing and the threshold's reveal grammar |
| Offline oracle mode (no credits, no AI) | `lib/oracleOffline.ts`, `docs/FLUXO_ORACULO_OFFLINE.md` | Seed phase principle: value without LLM dependency |
| Twelve Petals governance + petal filter | `docs/TWELVE_PETALS_GOVERNANCE.md` | Add as a check in the response contract evals (peace vs agitation, opens consciousness vs fixes identity, sincerity vs fear) |

## 2. Adapt (right idea, needs the corpus discipline)

| Asset | What it is there | Adaptation needed here |
| --- | --- | --- |
| Sacred corpus dictionaries (196 Yoga Sutras, Upanishads, Puranas JSONs with klesha/quality tags) | `lib/dictionaries/sacred/` | Migrate into `content/sources/` with frontmatter, citations and passage ids; the tagging scheme (kleshaTargets, qualities) becomes facet enrichment in the ontology pipeline |
| Sacred Remedy Engine (klesha + guna + ayurvedic-quality diagnosis -> text as remedy, 50-state remedy matrix) | `lib/sacredRemedy/`, `remedyMatrix.json` | Strong precursor of the inner sky offer and situation doors; must pass the three-tier health fence (RF-036): its practice/food suggestions map to safe tier only, and "diagnosis" language becomes "mirror" language (the app never labels the seeker) |
| Intent parser + state scorer (offline, dictionary-based) | `lib/input/` | Seed of the state detector in the C4 component model; extend to the consciousness core state taxonomy (states_of_response.md) and keep as offline pre-classifier before LLM state detection |
| Design system + time-visual core (sky rendered by hour) | `docs/DESIGN_SYSTEM.md`, `TIME_VISUAL_CORE.md`, `TimeHeader.tsx` | Merge with `design-tokens.yaml` four hour-themes; their drawn-sky work seeds the Sky Map rendering |
| Credits/payments infra (Stripe + Mercado Pago + PIX, usage ledger) | `lib/finance/`, `docs/BUSINESS_MODEL.md` | Input for the open business-model decision; if adopted, paywalls must never gate the contemplative surfaces (library, silence, daily word) - candidate boundary: credits only for LLM-cost surfaces (Inquiry), everything offline free |
| Next.js 15 app shell, CI, tests | repo root | Candidate scaffold for the Seed prototype instead of starting `apps/web` from zero |

## 3. Consciously Not Reused (divergence to decide with the creators)

The darshan repo computes **personal natal readings** (birth date/time/place ->
jyotish chart, numerology, human design; love/career/year readings). This
design's anti-prophecy boundary (`darshan_sky_map_design.md` section 1,
RF-031) excludes personal astrological interpretation, and the aadi-yogi
project boundaries forbid prophecy-like guidance.

The two postures can coexist honestly in one of two ways:

1. **Strict** (current design): reuse only the non-natal layers (time pulse,
   ephemeris, remedy engine at safe tier); no birth-data collection at all.
2. **Documentary bridge**: keep natal computation out, but let the corpus's
   jyotisha texts remain readable as documentary Library content (already
   the design), and route "read my chart" requests to a gentle refusal with
   rhythm framing (already NFR-016).

Decision recorded as open question for the creators in
`docs/skyforge/darshan/journey.yaml`; until decided, the strict posture
holds.

## 4. Suggested Extraction Path

1. Extract `lib/core/` (ephemeris) into a small shared package consumable by
   `apps/web` - it is pure computation, MIT, already tested.
2. Migrate `lib/dictionaries/sacred/*.json` content into `content/sources/`
   via the manifest pattern (a parallel import agent task - coordinates with
   the ongoing imports).
3. Port the petal filter into `packages/evals` as a rubric.
4. Evaluate the Next.js shell as the Seed prototype base
   (`journey.yaml -> seed_prototype`).
