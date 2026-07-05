# C4 Model - Darshan over the Aadi Yogi Monorepo

Produced following `journey.yaml` next action `architecture` (c4-modeler).
Diagrams use flowchart notation labeled by C4 level so they render on GitHub.

## Level 1 - System Context

```mermaid
flowchart TB
    seeker(["Seeker<br/>(anonymous by default)"])
    editor(["Editor / Curator<br/>(repository contributor)"])

    darshan["Darshan<br/>contemplative PWA"]
    engine["Aadi Yogi Engine<br/>agent API + retrieval"]
    corpus["Corpus Pipeline<br/>this repository"]

    llm["LLM Provider<br/>(swappable, external)"]
    ashram["Official source libraries<br/>(Ashram sites, restricted works)"]

    seeker -->|"gestures, questions, reading"| darshan
    darshan -->|"response contract"| engine
    engine -->|"completion requests<br/>(no diary data ever)"| llm
    engine -->|"passage retrieval with provenance"| corpus
    editor -->|"imports, reviews, facet tagging"| corpus
    corpus -.->|"metadata records point to"| ashram
    darshan -.->|"restricted works link out to"| ashram
```

## Level 2 - Containers

```mermaid
flowchart TB
    subgraph client["Seeker's device"]
        pwa["Darshan PWA (apps/web)<br/>seven gestures + silence room"]
        localstore["Local store<br/>diary (encrypted), anthology,<br/>reading positions, offline corpus bundle"]
        pwa --- localstore
    end

    subgraph server["Server side"]
        api["Agent API (apps/agent-api)<br/>response contract enforcement"]
        retr["Retrieval service (packages/rag)<br/>semantic + exact search"]
        pg[("Postgres + pgvector<br/>chunks, facets, parallels, vectors")]
        api --> retr --> pg
    end

    subgraph build["Build time (CI)"]
        content["content/ sources + ontology<br/>+ consciousness core"]
        chunker["chunking + enrichment<br/>(scripts/chunk, packages/ingestion)"]
        indexer["index + bundle builder (scripts/index)<br/>copyright enforced HERE"]
        evals["Eval harness (packages/evals)<br/>tone, safety, citation integrity,<br/>honored-silence precision"]
        content --> chunker --> indexer --> pg
        indexer -->|"offline reading bundles"| pwa
        evals -->|"release gate"| api
    end

    pwa -->|"HTTPS, anonymous session"| api
    api -->|"prompt (packages/prompts)"| llmp["LLM provider"]
```

## Level 3 - Components of the Agent API

```mermaid
flowchart LR
    q["Incoming question"] --> sd["State Detector<br/>(states_of_response.md)"]
    sd --> guard["Restraint Guard<br/>(silence_and_non_answering.md)"]
    guard -->|"restraint case"| silence["Honored Silence /<br/>Crisis Composer"]
    guard -->|"clear"| mode["Guidance Mode Selector<br/>(guidance_modes.md)"]
    mode --> rq["Retriever Client<br/>facet-aware query"]
    rq --> pb["Prompt Builder<br/>(voice.md + inner_posture.md<br/>+ state x mode matrix)"]
    pb --> llm2["LLM call"]
    llm2 --> cc["Contract Checker<br/>citations resolve? tone rules?<br/>one movement max? no prophecy?"]
    cc -->|"pass"| page["Contemplation Page<br/>(envelope of spec section 4.1)"]
    cc -->|"fail"| pb
    silence --> page
```

## Component Responsibilities and Homes

| Component | Home | Notes |
| --- | --- | --- |
| Seven gestures UI + depth dial | `apps/web` | PWA; tokens from `design-tokens.yaml`; silence room has zero telemetry |
| State detector | `apps/agent-api` | classifier prompt + heuristics; restraint cases short-circuit |
| Guidance mode selector | `apps/agent-api` | maps state x question type to modes |
| Prompt builder | `packages/prompts` | consciousness core compiled into system prompts |
| Retriever | `packages/rag` | passage-level chunks with facets and provenance payloads |
| Chunker / enricher | `packages/ingestion`, `scripts/chunk` | canonical-structure-aligned passage ids (library law) |
| Index + bundle builder | `scripts/index` | copyright filter at build time; offline bundles for reading rooms |
| Contract checker | `apps/agent-api` | rejects/regenerates on citation or tone failure |
| Eval harness | `packages/evals` | golden questions, honored-silence precision, presence metrics |

## Architectural Decisions (draft ADRs)

1. **Copyright at build time, not prompt time**: restricted works never enter
   quotable indexes; the model cannot leak what retrieval cannot see.
2. **Diary is client-side only**: the agent API has no diary endpoints except
   the single witness-mode invitation, which sends one entry transiently and
   stores nothing.
3. **D1 meanings are content, not generation**: batch-drafted, editorially
   reviewed, versioned in the corpus - so the most-read layer is the most
   reviewed layer.
4. **LLM provider behind one interface**: the response contract is enforced
   on our side; providers are swappable without behavioral change.
5. **Offline-first reading**: reading rooms ship as static bundles; only the
   Inquiry requires the network, and says so plainly.
