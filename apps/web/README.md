# Darshan PWA — Seed phase

Contemplative interface served by the agent API at `http://localhost:8000/`.

## Run

```powershell
pnpm api:dev
# open http://localhost:8000/
```

## Seed deliverables (S-01–S-07)

| ID | Feature |
|----|---------|
| S-01 | PWA shell + 4 hour themes (`data-hour`) |
| S-02 | Threshold entry ritual (8s breath, skip, reduced-motion) |
| S-03 | Court hub — one gesture per card |
| S-04 | Daily word (batch JSON, offline via service worker) |
| S-05 | Library reading room (D0–D2 depth dial) |
| S-06 | Silence room |
| S-07 | i18n — en · pt · hi · it · es |

## Structure

```
apps/web/
├── index.html
├── manifest.webmanifest
├── sw.js
└── static/
    ├── css/          # design tokens (from spec/design-tokens.yaml)
    ├── js/           # app, strings, theme
    ├── data/         # daily-words.json, library passages
    └── icons/
```

## Daily word batch

Editorial batches per ADR-0004 — never generated live:

```powershell
python scripts/content/build_daily_words.py
```

## Design reference

- Tokens: `spec/design-tokens.yaml`
- Prototype: `spec/design/claude-design/Darshan App.dc.html`
- Spec: `spec/ux-spec.yaml`

## Install as PWA

Use browser “Install app” after first visit. Service worker caches static assets and daily word data for offline use.

## GitHub Pages

Static shell deploys automatically from `main` via `.github/workflows/deploy-pages.yml`.

- URL: https://sraphaz.github.io/aadi-yogi/
- Oracle/API routes (`/inquire`, `/ask`, …) require `pnpm api:dev` locally — not available on Pages.
