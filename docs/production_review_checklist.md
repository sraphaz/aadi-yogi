# Production Review Checklist — Consciousness Core and Agent Layer

Use this checklist before exposing the Aadi Yogi agent to a wider audience.

## Consciousness Core v1

- [ ] `content/consciousness_core/approved_manifest.yaml` reviewed by a human editor
- [ ] No language that claims realization, infallibility, or guru authority
- [ ] Safety guidance present for kundalini, crisis, and intense practices
- [ ] Synthesis rules preserve tradition differences instead of flattening them
- [ ] Examples of bad answers remain available for regression review

## Source Corpus

- [ ] Imported texts declare correct `copyright_status`
- [ ] Citations are specific enough for verification
- [ ] No copyrighted Sri Aurobindo / Mother full text without permission
- [ ] Retrieval eval (`scripts/validate/run_golden_questions.py`) passes
- [ ] Response quality eval (`scripts/validate/run_response_eval.py`) passes

## Retrieval and Embeddings

- [ ] TF-IDF index built (`scripts/index/build_vector_index.py`)
- [ ] Dense index built (`scripts/index/build_dense_index.py`)
- [ ] Optional Qdrant sync tested if hosted vector DB is used
- [ ] Embedding provider documented (hash local vs OpenAI)

## LLM Layer

- [ ] API keys stored outside the repository
- [ ] Fallback mode tested without external LLM
- [ ] LLM mode tested with OpenAI-compatible provider
- [ ] Answers include citations when sources are retrieved
- [ ] Caution appears for risky question classes

## Web/API

- [ ] `/health` reports llm_configured and vector indexes
- [ ] `/ask` returns citations and retrieved excerpts
- [ ] Web UI clearly states the system is not a guru replacement
- [ ] CORS and deployment settings reviewed for production

## Sign-off

| Role | Name | Date | Notes |
| --- | --- | --- | --- |
| Editorial | | | |
| Spiritual care | | | |
| Engineering | | | |
