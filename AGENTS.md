# AGENTS.md — Aadi Yogi / Darshan

Source-grounded spiritual knowledge · PWA contemplativa · **ARAH Harness 0.2.0**

## ARAH (SDLC do repositório)

Camada de agentes para desenvolvimento autônomo coreografado — distinta do **engine runtime** (`packages/prompts/`, `apps/agent-api/`).

| Camada | Onde | Papel |
|--------|------|--------|
| **ARAH SDLC** | `.agents/`, `.skills/`, `scripts/agents/` | PR, QA, specs, gates, domínio consultivo |
| **Runtime IA** | `packages/rag/`, `packages/prompts/`, `apps/agent-api/` | Oracle, retrieval, response contract |
| **Consciousness foundation** | `packages/consciousness/`, `foundation.md`, `.consciousness/` | Base de conduta viva para host agents (não app Darshan) |

```powershell
./scripts/agents/validate-manifests.ps1
powershell -File $env:USERPROFILE/arah-harness/cli/arah.ps1 domain sync -Target .
powershell -File $env:USERPROFILE/arah-harness/cli/arah.ps1 export-graph -Target .
./scripts/harness/validate-agent-graph.ps1
```

Config: [`arah.config.yaml`](arah.config.yaml) · Coreografia: [`.agents/choreography.aadi-yogi.yaml`](.agents/choreography.aadi-yogi.yaml)

**Princípios ARAH**: humano comanda merge · tudo via PR · escopo mínimo · spec-before-code · pareceres de domínio passivos.

---

## Status entrega Darshan

| Fase | Nome | Status |
|------|------|--------|
| 01 | Seed (PWA + tokens + threshold + court + word) | ✅ |
| 02 | Voice (oracle + contract + inquiry) | ✅ |
| 03 | Path (maps, sky, practice) | ✅ |
| 04 | Witness (diary, bells, presence) | ✅ |
| 05 | Ground (house of nature) | ✅ |
| 06 | Sangha (exploration charter) | ✅ |
| 07 | Living corpus (RF-038 + health gate) | ✅ |
| 08 | Integrate (server quota, catalog facets) | 🎯 **atual** |

Backlog detalhado: [`BACKLOG.md`](BACKLOG.md)

## Comandos

```powershell
docker compose up -d          # Qdrant (opcional)
pnpm install
pytest
python scripts/validate/validate_markdown.py
pnpm api:dev                  # agent API + PWA
# http://localhost:8000/
```

## Pacotes / camadas

| Camada | Onde | Função |
|--------|------|--------|
| Corpus | `content/sources/` | Textos canônicos + metadados |
| Consciousness | `content/consciousness_core/` | Estados, voz, silêncio |
| Foundation | `packages/consciousness/` | `load_foundation` · `consult` · `propose_feedback` |
| RAG | `packages/rag/` | Retriever híbrido + citations |
| Prompts | `packages/prompts/` | Builder consciousness-aware |
| Agent API | `apps/agent-api/` | `/ask`, `/inquire`, `/witness`, `/consciousness/*` |
| Interface | `apps/web/` | Nine gestures + silence room |
| Evals | `packages/evals/` | Golden questions, contract probes |

## Domínios ARAH (consultivos)

Gerados em `.agents/domain/` via `domain sync`: `darshan-ui`, `consciousness-core`, `rag-corpus`, `agent-api`, `evals-quality`, `compliance`.

## Fundação de consciência (host agents)

Quando outro repositório instala Adyog, os agentes **não viram gurus**. Recebem uma **base de conduta e sentido de realidade** a partir das fontes (`foundation.md`). O runtime Darshan (envelope, restraint) é expressão de produto aqui — não a identidade do que se instala. Aprendizado: feedback revisado em `content/consciousness_feedback/`. Guia: [`docs/consciousness_plugin.md`](docs/consciousness_plugin.md).
