# AGENTS.md — Aadi Yogi / Darshan

Source-grounded spiritual knowledge · PWA contemplativa · **ARAH Harness 0.2.0**

## ARAH (SDLC do repositório)

Camada de agentes para desenvolvimento autônomo coreografado — distinta do **engine runtime** (`packages/prompts/`, `apps/agent-api/`).

| Camada | Onde | Papel |
|--------|------|-------|
| **ARAH SDLC** | `.agents/`, `.skills/`, `scripts/agents/` | PR, QA, specs, gates, domínio consultivo |
| **Runtime IA** | `packages/rag/`, `packages/prompts/`, `apps/agent-api/` | Oracle, retrieval, response contract |

```powershell
./scripts/agents/validate-manifests.ps1
powershell -File $env:USERPROFILE/arah-harness/cli/arah.ps1 domain sync -Target .
powershell -File $env:USERPROFILE/arah-harness/cli/arah.ps1 export-graph -Target .
```

Config: [`arah.config.yaml`](arah.config.yaml) · Coreografia: [`.agents/choreography.aadi-yogi.yaml`](.agents/choreography.aadi-yogi.yaml)

**Princípios ARAH**: humano comanda merge · tudo via PR · escopo mínimo · spec-before-code · pareceres de domínio passivos.

---

## Status entrega Darshan

| Fase | Nome | Status |
|------|------|--------|
| 01 | Seed (PWA + tokens + threshold + court + word) | 🎯 **atual** |
| 02 | Voice (oracle + contract + inquiry) | arriving |
| 03 | Path (maps, sky, practice) | future |
| 04 | Witness (diary, inner sky) | future |
| 05 | Ground (house of nature) | future |
| 06 | Sangha | unscheduled |

Backlog detalhado: [`BACKLOG.md`](BACKLOG.md)

## Comandos

```powershell
docker compose up -d          # Qdrant (opcional)
pnpm install
pytest
python scripts/validate/validate_markdown.py
pnpm api:dev                  # agent API
# apps/web/ — PWA Darshan (em construção, fase Seed)
```

## Pacotes / camadas

| Camada | Onde | Função |
|--------|------|--------|
| Corpus | `content/sources/` | Textos canônicos + metadados |
| Consciousness | `content/consciousness_core/` | Estados, voz, silêncio |
| RAG | `packages/rag/` | Retriever híbrido + citations |
| Prompts | `packages/prompts/` | Builder consciousness-aware |
| Agent API | `apps/agent-api/` | `/ask`, contract enforcement |
| Interface | `apps/web/` | Nine gestures + silence room |
| Evals | `packages/evals/` | Golden questions, contract probes |

## Princípios de produto (lei comportamental)

- Interface = primeira lição: silêncio, um ponto por tela, closure como sucesso
- Tudo oferecido, nunca imposto; sem streaks, badges, spinners, dark patterns
- Citações sempre resolvíveis (no-orphan-quotation)
- ADRs em `spec/decisions/` — **não reabrir em código**
- Design Claude: `spec/design/claude-design/` (protótipo + tokens + handoff)

## Spec

- Session Sky-Forge: `spec/` (RF-001..038, ux-spec, tokens, NFR)
- Narrativa: `docs/darshan_interface_*.md`
- Handoff hub: `spec/design/claude-design/Darshan Handoff.dc.html`

## Domínios ARAH (consultivos)

Gerados em `.agents/domain/` via `domain sync`: `darshan-ui`, `consciousness-core`, `rag-corpus`, `agent-api`, `evals-quality`, `compliance`.
