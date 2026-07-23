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
4. `spec/decisions/` (ADRs 0001–0006 — não reabrir)
5. Protótipo: abrir `spec/design/claude-design/Darshan Handoff.dc.html` no browser

---

## Fase 01 — Seed ✅

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

## Fase 02 — Voice ✅

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

## Fase 03 — Path ✅

Living maps · practice field · outer sky (local ephemeris) · rhythm composer · inner weather marks (local).

| ID | Entrega | Agente | Paths | RF |
|----|---------|--------|-------|-----|
| P-01 | Living maps — aspiration path, posture, stations | frontend | `apps/web/` | RF-009 |
| P-02 | Practice field — offering, look-back, silence link | frontend | `apps/web/` | RF-010 |
| P-03 | Sky map — moon phase, tithi, ritu, sun times (local) | frontend | `apps/web/static/js/ephemeris.js` | RF-030, RF-031 |
| P-04 | Rhythm composer — opt-in joints, sky bind | frontend | `apps/web/` | RF-026, RF-034 |
| P-05 | Inner weather marks on sky map (local-only) | frontend | `apps/web/` | RF-032 (parcial) |

**Gate:** sem progress percentages; location never leaves device; sem dados natais (ADR-0002).

---

## Fase 04 — Witness ✅

Inner diary (local-first, encrypted) · witness mode · presence metrics · opt-in bells.

| ID | Entrega | Agente | Paths | RF |
|----|---------|--------|-------|-----|
| W-01 | Inner diary — AES-GCM, chave derivada do usuário | frontend | `apps/web/static/js/diary-*.js` | RF-012 |
| W-02 | Witness mode — POST `/witness` transiente, sem persistência | backend | `packages/prompts/witness.py`, `apps/agent-api/` | RF-012 |
| W-03 | Look-back/offering espelham no diário | frontend | `apps/web/` | RF-010 |
| W-04 | Presence metrics on-device | frontend | `presence-metrics.js` | RF-015 |
| W-05 | Opt-in dawn/dusk bells (máx. 2/dia) | frontend | `bells.js` | RF-013 |

**Gate:** diary provably engine-blind; zero third-party analytics.

---

## Fase 05 — Ground ✅

House of Nature — element rooms first; heritage fence; double editorial gate.

| ID | Entrega | Agente | Paths | RF |
|----|---------|--------|-------|-----|
| G-01 | House hub — heritage notice, tiers, room states | frontend | `apps/web/` | RF-035, RF-036 |
| G-02 | Fire element room (safe movement + documentary passage) | frontend | `apps/web/static/data/nature/` | RF-035 |
| G-03 | Pancha mahabhuta ontology seed | rag-corpus | `content/ontology/` | RF-035 |
| G-04 | Health tier helpers | backend | `packages/prompts/health_tier.py` | RF-036 |
| G-05 | Sky season link into safe regimen | frontend | `apps/web/` | RF-035 |

**Gate:** ADR-0003 — dois revisores nomeados antes de health-touching acima D2.

---

## Fase 06 — Sangha ✅

Exploração apenas — sem feeds, profiles ou counts.

| ID | Entrega | Agente | Paths | RF |
|----|---------|--------|-------|-----|
| SG-01 | Court card + charter screen (forbidden list, forms) | frontend | `apps/web/` | spec §9.6 |
| SG-02 | Shared silence sitting → silence room (local only) | frontend | `apps/web/static/data/sangha/` | RF-006 |
| SG-03 | Study circle placeholder (`arriving`) | frontend | `apps/web/` | — |

**Gate:** nenhum endpoint social; carta revisada pelos criadores antes de qualquer sync.

---

## Fase 07 — Living Corpus ✅

Protocolo de crescimento honesto — features acendem conforme o corpus importa.

| ID | Entrega | Agente | Paths | RF |
|----|---------|--------|-------|-----|
| LC-01 | Library catalog from manifests + passage JSON | backend | `scripts/content/build_library_catalog.py` | RF-038 |
| LC-02 | Shelves estendem do catalog; estados open/arriving/future | frontend | `apps/web/` | RF-038 |
| LC-03 | Linha quiet "the library has grown" no Court (dismissable) | frontend | `corpus-store.js` | RF-038 |
| LC-04 | Health gate CI — health_sensitive exige safety_review | qa | `scripts/validate/check_health_gate.py` | RF-037 |

**Gate:** catalog.json gerado em CI; nenhum conteúdo closed-tier na UI.

---

## Fase 08 — Integrate ✅

Quota server-side · facets no catalog · shelves arriving honestos.

| ID | Entrega | Agente | Paths | RF |
|----|---------|--------|-------|-----|
| I-01 | Server inquiry quota (`X-Darshan-Device`, 429) | backend | `packages/prompts/inquiry_quota.py` | RF-039 |
| I-02 | GET `/inquiry/quota` + PWA sync | frontend + backend | `inquiry-quota.js`, `apps/agent-api/` | RF-039 |
| I-03 | Catalog facets + shelves upanishads/CWSA arriving | backend | `build_library_catalog.py` | RF-038 |
| I-04 | Consciousness plugin façade + MCP + `/consciousness/*` | backend | `packages/consciousness/`, `apps/mcp-server/` | ADR-0006 |

**Gate:** medida free enforced server-side when calibrated; créditos/pagamento ainda não wired; plugin de consciência testável via Python/MCP/HTTP.

---

## Decisões reservadas aos criadores

Scaffold: [`docs/calibrations/`](docs/calibrations/README.md) · `scripts/validate/check_calibrations.py`

- [x] Precificar medida free e créditos → [`0001-dana.yaml`](docs/calibrations/0001-dana.yaml) ✅ 2026-07-05
- [ ] Nomear dois health reviewers → [`0003-health-reviewers.yaml`](docs/calibrations/0003-health-reviewers.yaml)
- [x] Escolher veículo legal para dana → associação sem fins lucrativos (BR), razão social pendente

---

## Referências

- Roadmap visual: `spec/design/claude-design/Darshan Roadmap.dc.html`
- Reuso Next.js shell: `docs/darshan_reuse_map.md` (repo `sraphaz/darshan`)
- Passage-id: `docs/passage_id_scheme.md`
- ROADMAP técnico do monorepo: `ROADMAP.md`
