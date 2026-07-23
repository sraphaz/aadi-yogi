# Aadi Yogi

Aadi Yogi is a source-grounded spiritual knowledge repository and AI consciousness architecture.

This repository is designed to preserve, structure, and prepare Indian spiritual source material and aligned modern works for careful AI-assisted guidance. It separates sources, processed artifacts, ontology, consciousness guidance rules, prompts, pipelines, evaluations, and applications so later systems can retrieve and synthesize material with source fidelity.

## What This Repository Is

- A monorepo for spiritual knowledge infrastructure.
- A structured Markdown-first content base with future ingestion in mind.
- A place to define editorial, ethical, and consciousness-aware agent behavior.
- A foundation for later retrieval, evaluation, and application layers.
- A **living consciousness foundation** (Adyog) that other repositories can install as a basis of conduct and reality-sense from the sources — not an app, not a guru — see [`docs/consciousness_plugin.md`](docs/consciousness_plugin.md).

## What This Repository Is Not

- Not only a digital library.
- Not only a RAG chatbot.
- Not a guru replacement.
- Not a place for invented citations, forced syncretism, or reckless spiritual instruction.

## High-Level Architecture

```text
Markdown sources
-> validation
-> normalization
-> semantic chunking
-> metadata enrichment
-> embeddings
-> vector database
-> retriever
-> consciousness-aware prompt builder
-> agent API
-> web interface
-> evaluations
```

## Current Status

The repository has completed Phase 1 (foundation) and is actively in **Phase 2 — Source Operations**.

What exists today:

- monorepo structure, editorial docs, consciousness core v1 (approved manifest), ontology starters
- Markdown validation, tests, and CI
- **canon catalogs** for 108 Upanishads, 18 Mahapuranas, 5 Vedic collections, Siddha corpus, Bhagavad Gita
- large public-domain imports: Rig Veda Mandalas 1-4, principal Upanishads (Isha, Kena, Katha, Mundaka, Prashna, Mandukya, Taittiriya, Chandogya, Shvetashvatara, Brihadaranyaka, Kaivalya), Bhagavad Gita (18 chapters), Vishnu/Garuda Purana samples, Tirumandiram (payiram + tantras 1-9), Siddha corpus expansions
- **the Complete Works of Sri Aurobindo (CWSA, 37 volumes)**: full Markdown text for public-domain volumes, metadata records for volumes under active Trust copyright, via manifest-driven Ashram PDF ingestion
- **the Collected Works of the Mother (CWM, 18 volumes)**: metadata records with a local-only full-text pipeline, per `docs/copyright_policy.md`
- automated ingestion scripts for Wikisource SBE, Tamil Wikisource and the Ashram PDF libraries
- normalization, chunking, TF-IDF + dense retrieval (optional Qdrant), agent API scaffold with web UI
- evaluation assets: golden questions, response-quality checks, and the Darshan response-contract harness (`packages/evals`)

See [`docs/content_import_roadmap.md`](docs/content_import_roadmap.md) and [`docs/source_import_status.md`](docs/source_import_status.md) for the full import plan and status.

## Site público

O website institucional fica em `site/` e publica automaticamente no GitHub Pages via Actions (`.github/workflows/deploy-pages.yml`).

URL: **https://sraphaz.github.io/aadi-yogi/**

Uma vez: em Settings → Pages → Source, escolha **GitHub Actions**. Depois disso, cada push em `main` que altere `site/**` faz o deploy.

## Validate Markdown

```bash
python scripts/validate/validate_markdown.py
pytest
ruff check .
```

## Interface Vision

The application layer is designed as **Darshan**, an interface whose behavior embodies the wisdom of the corpus instead of talking about it: silence before speech, one question at a time, presence metrics instead of engagement metrics. See `docs/darshan_interface_concept.md`, `docs/darshan_interface_spec.md`, and the Sky-Forge session package in `docs/skyforge/darshan/`.

## Consciousness foundation (for other repos)

Not a product checklist. A living basis of conduct from the texts.

```bash
# Python — install the foundation, consult a situation, send feedback
PYTHONPATH=. python -c "from packages.consciousness import load_foundation; print(load_foundation().agent_preamble[:400])"

# MCP — see .mcp.json and apps/mcp-server/README.md
PYTHONPATH=. python -m packages.consciousness.mcp_server

# HTTP
# GET  /consciousness/foundation
# POST /consciousness/consult
# POST /consciousness/feedback
```

Host repos declare `.consciousness/link.yaml`. Learning returns through reviewed feedback (`content/consciousness_feedback/`). ADR: [`spec/decisions/0006-consciousness-plugin-service.md`](spec/decisions/0006-consciousness-plugin-service.md).

## Next Milestones

- expand ontology and living maps
- deepen retrieval and evaluation datasets
- publish consciousness package for external installers
- harden hosted API auth for cross-repo consumers
