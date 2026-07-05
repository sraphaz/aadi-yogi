# BACKLOG — Darshan (Aadi Yogi)

Entrega multiagente via **ARAH Harness 0.2.0**. Spec em `spec/`; design Claude em `spec/design/claude-design/`.

## Como operar (agentes)

```powershell
./scripts/agents/validate-manifests.ps1
powershell -File $env:USERPROFILE/arah-harness/cli/arah.ps1 domain sync -Target .
powershell -File $env:USERPROFILE/arah-harness/cli/arah.ps1 export-graph -Target .
./scripts/agents/next-phase.ps1   # quando uma fase fechar gate
```

**Leitura obrigatória antes de codar:**
1. `spec/design/claude-design/readme.md` — lei comportamental
2. `docs/darshan_interface_concept.md` → `docs/darshan_interface_spec.md`
3. `spec/ux-spec.yaml` + `spec/design-tokens.yaml`
4. `spec/decisions/` (ADRs 0001–0005 — não reabrir)
5. Protótipo: abrir `spec/design/claude-design/Darshan Handoff.dc.html` no browser

---

## Fase 01 — Seed (open) ← **ATUAL**

**Goal:** PWA instalável que já encarna silêncio, one-pointedness e closure, servindo corpus offline.

| ID | Entrega | Agente | Paths | RF |
|----|---------|--------|-------|-----|
| S-01 | Shell PWA + design tokens (4 hour themes) | frontend | `apps/web/` | RF-001, RF-002 |
| S-02 | Threshold entry ritual (8s breath, skip, reduced-motion) | frontend | `apps/web/` | RF-001 |
| S-03 | Court hub — one gesture per card | frontend | `apps/web/` | RF-002 |
| S-04 | Daily word (batch pipeline, offline prefetch) | backend + frontend | `apps/web/`, scripts | RF-003, ADR-0004 |
| S-05 | Library reading room (D0–D2 mínimo) | frontend + rag-corpus | `apps/web/`, `packages/rag/` | RF-016, RF-017 |
| S-06 | Silence room | frontend | `apps/web/` | RF-006 |
| S-07 | i18n foundation — en · pt · hi · it · es | frontend | `apps/web/` | NFR scripts |

**Gate:** WCAG 2.1 AA; reduced-motion em todo ritual; daily word legível por screen reader antes da animação; 5 string files revisados.

---

## Fase 02 — Voice (arriving)

**Goal:** Oracle sob response contract — retrieval com citations, contemplation pages, honored silence.

| ID | Entrega | Agente | Paths | RF |
|----|---------|--------|-------|-----|
| V-01 | Tradition-aware retrieval + citation payloads | backend | `packages/rag/` | RF-005, RF-017 |
| V-02 | Response contract enforcement no API | backend | `apps/agent-api/` | RF-005 |
| V-03 | Inquiry + contemplation pages (no chat bubbles) | frontend + backend | `apps/web/`, `apps/agent-api/` | RF-004 |
| V-04 | Honored silence + crisis protocol | backend | `packages/prompts/`, `apps/agent-api/` | RF-006 |
| V-05 | Eval suites antes de exposure | qa | `packages/evals/` | NFR |

**Gate:** citation integrity = 1.0 CI; honored-silence precision auditada; sem streaming durante composição.

---

## Fase 03 — Path (future)

Living maps · practice field · concept lens · outer sky (local ephemeris) · rhythm composer.

**Gate:** sem progress percentages; location never leaves device.

---

## Fase 04 — Witness (future)

Inner diary (local-first, encrypted) · witness mode · inner sky · presence metrics · opt-in bells.

**Gate:** diary provably engine-blind; zero third-party analytics.

---

## Fase 05 — Ground (future)

House of Nature — element rooms first; heritage fence; double editorial gate.

**Gate:** ADR-0003 — dois revisores nomeados antes de health-touching acima D2.

---

## Fase 06 — Sangha (unscheduled)

Exploração apenas — sem feeds, profiles ou counts.

---

## Decisões reservadas aos criadores

- [ ] Precificar medida free e créditos (ADR-0001)
- [ ] Nomear dois health reviewers (ADR-0003)
- [ ] Escolher veículo legal para dana

---

## Referências

- Roadmap visual: `spec/design/claude-design/Darshan Roadmap.dc.html`
- Reuso Next.js shell: `docs/darshan_reuse_map.md` (repo `sraphaz/darshan`)
- Passage-id: `docs/passage_id_scheme.md`
- ROADMAP técnico do monorepo: `ROADMAP.md`
