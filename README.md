# Aadi Yogi

Aadi Yogi is a source-grounded spiritual knowledge repository and AI consciousness architecture.

This repository is designed to preserve, structure, and prepare Indian spiritual source material and aligned modern works for careful AI-assisted guidance. It separates sources, processed artifacts, ontology, consciousness guidance rules, prompts, pipelines, evaluations, and applications so later systems can retrieve and synthesize material with source fidelity.

## What This Repository Is

- A monorepo for spiritual knowledge infrastructure.
- A structured Markdown-first content base with future ingestion in mind.
- A place to define editorial, ethical, and consciousness-aware agent behavior.
- A foundation for later retrieval, evaluation, and application layers.

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

The repository is in the foundation phase. The current scope covers:

- monorepo structure
- editorial and architectural documentation
- source templates and ontology starters
- consciousness core guidelines
- Markdown validation scaffolding
- tests and CI validation

## Validate Markdown

```bash
python scripts/validate/validate_markdown.py
pytest
ruff check .
```

## Next Milestones

- define richer source metadata conventions
- add normalization and chunking pipelines
- expand ontology and living maps
- introduce retrieval and evaluation datasets
- scaffold agent API and web application surfaces
