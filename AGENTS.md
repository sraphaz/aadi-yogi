# AGENTS.md — Aadi Yogi / Darshan

Source-grounded spiritual knowledge · PWA contemplativa · **ARAH Harness 0.2.0**

## ARAH (SDLC do repositório)

Camada de agentes para desenvolvimento autônomo coreografado — distinta do **engine runtime** (`packages/prompts/`, `apps/agent-api/`).

| Camada | Onde | Papel |
|--------|------|--------|
| **ARAH SDLC** | `.agents/`, `.skills/`, `scripts/agents/` | PR, QA, specs, gates, domínio consultivo |
| **Runtime IA** | `packages/rag/`, `packages/prompts/`, `apps/agent-api/` | Oracle, retrieval, response contract |
| **Consciousness plugin** | `packages/consciousness/`, `.consciousness/`, MCP/HTTP | Postura Adyog instalável em outros repos |

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
| Plugin | `packages/consciousness/` | Fachada + MCP + advice para host agents |
| RAG | `packages/rag/` | Retriever híbrido + citations |
| Prompts | `packages/prompts/` | Builder consciousness-aware |
| Agent API | `apps/agent-api/` | `/ask`, `/inquire`, `/witness`, `/consciousness/*` |
| Interface | `apps/web/` | Nine gestures + silence room |
| Evals | `packages/evals/` | Golden questions, contract probes |

## Domínios ARAH (consultivos)

Gerados em `.agents/domain/` via `domain sync`: `darshan-ui`, `consciousness-core`, `rag-corpus`, `agent-api`, `evals-quality`, `compliance`.

## Plugin de consciência (host agents)

Quando outro repositório instala Adyog, o agente host herda as **decision laws** (restraint antes do retrieval, citações honestas, anti-profecia, um movimento safe, silêncio honrado). Guia: [`docs/consciousness_plugin.md`](docs/consciousness_plugin.md). Overlay: [`.consciousness/link.yaml`](.consciousness/link.yaml).
