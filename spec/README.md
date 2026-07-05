# Spec — Darshan (Aadi Yogi)

Fonte de verdade para ARAH spec-before-code e gates de CI.

## Artefatos de sessão

| Arquivo | Conteúdo |
|---------|----------|
| `functional-requirements.yaml` | 38 RFs com acceptance criteria |
| `ux-spec.yaml` | 17 telas, 7 journeys, anti-patterns |
| `design-tokens.yaml` | 4 hour themes, tipografia, motion |
| `nfr.yaml` | privacy, a11y, health fence, scripts |
| `integrations.yaml` | engine, infra, ephemeris |
| `c4-model.md` | arquitetura C4 |
| `journey.yaml` | estado da sessão Sky-Forge |

## Design Claude (handoff visual)

Pacote exportado em `design/claude-design/`:

- `Darshan Handoff.dc.html` — hub de entrega
- `Darshan App.dc.html` — protótipo interativo (9 gestures)
- `Darshan Site.dc.html` — site institucional
- `Darshan Roadmap.dc.html` — 6 fases de implementação
- `tokens/`, `guidelines/`, `styles.css`

## Decisões (não reabrir)

`decisions/` — ADRs 0001–0005 (dana, natal, health, editorial, passage-id).

## Narrativa

`narrative/` espelha `docs/darshan_interface_*.md` do pacote Claude.

Espelho upstream: `docs/skyforge/darshan/` (regenerável via `scripts/export/build_darshan_package.py`).
