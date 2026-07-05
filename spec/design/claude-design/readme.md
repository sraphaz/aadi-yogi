# Darshan Design System

The visual and behavioral language of **Darshan** — the contemplative interface of the
Aadi Yogi wisdom engine. A digital darshan, not a chatbot: the interface itself must
behave from the wisdom it carries (silence before speech, one-pointedness, non-coercion,
renunciation by design). The medium teaches louder than the message, so these tokens and
patterns are behavioral law, not decoration.

## Sources

- `uploads/darshan-package/session/design-tokens.yaml` — token source of truth (v1.0)
- `uploads/darshan-package/session/ux-spec.yaml` — screens, journeys, forbidden anti-patterns
- `uploads/darshan-package/narrative/darshan_interface_concept.md` — ten design principles
- `uploads/darshan-package/narrative/darshan_interface_spec.md` — screens, flows, response contract
- `uploads/darshan-package/narrative/darshan_library_design.md` — seven depths, six doors
- Source repository: https://github.com/sraphaz/aadi-yogi · prior art: github.com/sraphaz/darshan

## Content fundamentals

- **Voice**: calm but not cold, deep but not obscure, reverent but not dogmatic. Never
  performs certainty, never performs mysticism, never claims realization.
- **Everything is offered, never assigned**: "a safe first movement could be…", "if you
  wish, keep it". No imperatives of obligation, no urgency, no scarcity, no teasers.
- **Warm nouns, lowercase** for doors and gestures: `grief`, `work`, `joy`, `the word`,
  `the well`. Labels whisper (small caps, letterspaced); the sacred word speaks (large serif).
- **Citation is lineage, not liability**: every quotation names work · section · tradition
  and can be followed to the complete book. No orphan quotations, ever.
- **No emoji. No exclamation marks.** Sentences end quietly.
- **Closure is success**: every surface offers a way to leave in peace ("go gently").
  Nothing re-engages: no streaks, badges, counters, or "you might also like".
- Languages: english · português · हिन्दी · italiano · español — every surface of app and
  site ships in all five; quotations stay in canonical language. Hindi UI pairs Manrope
  with Noto Sans Devanagari (set via `[data-lang="hi"]`).

## Visual foundations

- **Hour themes** (`data-hour`): pre_dawn (deep indigo, ember warmth) · day (warm paper)
  · dusk (rose ash) · night (near black, one warm point). Palette follows the seeker's
  local hour; manual override allowed. Only these four grounds — never pure white/black.
- **Two accents only**: `--accent-flame` (aspiration: links, active depth) and
  `--accent-gold` (reverence: ornaments, closing marks). `--halo` is reserved for focus
  rings and the breath pulse. `--warn` marks cautionary surfaces — warm umber, never red.
- **Type**: Source Serif 4 belongs to the sacred word alone (D0 2.25rem → D2 1.375rem →
  reading 1.125rem). Manrope is the interface. Noto Serif Devanagari/Tamil + Gentium Plus
  (IAST) render originals. JetBrains Mono renders passage ids and provenance.
- **Space is doctrine**: `--space-breath` (4rem) around any D0 word; reading measure
  capped at 62ch; one screen holds one thing.
- **Motion is breath**: 8s pulse, 1.8s passage reveal, 600ms dial, 150ms hover; single
  easing `--ease-calm`. All fades collapse to instant under reduced motion (the pulse
  becomes a static glyph). **No spinners anywhere** — loading is absorbed into the
  threshold breath.
- **Surfaces**: flat `--surface`; cards on `--surface-raised` with 1px hairline borders
  (color-mix of ink at ~12%); radius 12px soft / pill for chips; **no shadows**, no
  glassmorphism, no gradients except the drawn sky of the Sky Map.
- **Focus states**: 2px `--halo` ring, offset 2px. Hover: opacity/ink shifts at 150ms —
  nothing moves, nothing grows.
- **Touch targets ≥ 44px** (WCAG 2.1 AA; NFR-003). Every ritual is skippable.

## Iconography

There is no icon set and none should be invented. The system's only glyphs are
typographic and geometric: the ring `◦`, the point `·`, a 1px line, and the breath
pulse (a circle). Doors and cards are named in words, not pictured. Never icons of
despair, never decorative SVG illustration. **No logo exists**: the wordmark is the
word `darshan` set lowercase in Source Serif 4 — do not draw a mark.

## Forbidden (from ux-spec.yaml)

Feeds and infinite scroll · streaks, badges, gamification · push notifications by
default · engagement-time optimization · autoplay and content teasers · dark patterns
· horoscopes/predictions · health diagnosis or dosage · mood-tracker scoring.

## Intentional additions (to calibrate with the creators)

`--radius-soft: 12px`, `--radius-pill`, `--touch-target: 44px`, `--hairline: 1px`,
leading/weight/tracking values — sensible defaults not present in design-tokens.yaml v1.0.

## Index

- `styles.css` — global entry (imports everything under `tokens/`)
- `tokens/` — fonts · colors (4 hour themes) · typography · spacing · motion
- `guidelines/` — specimen cards (colors per hour, type, spacing, motion, component
  patterns: court card, situation doors, depth dial, citation, contemplation page,
  heritage notice, silence room)
- Deliverables built on this system: `Darshan App.dc.html` (prototype — all 9 gestures + silence room, library reading room, sky map, house of nature, inner diary, dana/credits per ADR-0001; 5 languages, new screens pt+en),
  `Darshan Site.dc.html` (institutional site v2 — entrada / caminho / biblioteca / dana / integridade / perguntas, billing per ADR-0001, pt+en via `site-strings.js`; v1 kept as `Darshan Site v1.dc.html`),
  `Darshan Roadmap.dc.html` (dev roadmap), `Darshan Handoff.dc.html` (handoff hub)
