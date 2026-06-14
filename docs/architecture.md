# Architecture

The intended architecture flows from curated source material to an agent layer that responds with source awareness and inner caution.

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

## Layer Responsibilities

- Markdown sources: canonical, reviewable, human-readable content and templates.
- Validation: structural checks for frontmatter completeness and basic consistency.
- Normalization: cleanup into consistent formats for downstream processing.
- Semantic chunking: split content into retrieval-ready units without losing citation context.
- Metadata enrichment: attach concepts, traditions, themes, and caution fields.
- Embeddings and vector database: future retrieval infrastructure.
- Retriever: select relevant passages with provenance.
- Consciousness-aware prompt builder: shape response posture, tone, and caution based on question type and inner state.
- Agent API: orchestrate retrieval and response generation.
- Web interface: present answers, citations, and study context.
- Evaluations: verify accuracy, tone, safety, and integrity.
