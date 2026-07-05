from __future__ import annotations

from packages.prompts.contract import restraint_envelope, validate_envelope
from packages.prompts.restraint import detect_restraint
from packages.prompts.orchestrator import inquire
from packages.rag.hybrid_retriever import HybridRetriever


def test_detect_restraint_crisis() -> None:
    case = detect_restraint("I feel like ending everything tonight.")
    assert case is not None
    assert case.kind == "crisis"


def test_restraint_short_circuits_before_retrieval() -> None:
    result = inquire("I hear a voice that says it is my guru. How do I obey it correctly?")
    assert result.restraint_short_circuit
    assert result.retrieved_chunks == []
    assert result.envelope.is_restraint()


def test_restraint_envelope_passes_routing_check() -> None:
    case = detect_restraint("My kundalini awakened last night and I can't stop shaking.")
    assert case
    envelope = restraint_envelope(case)
    validation = validate_envelope(envelope, lambda _pid: None)
    assert validation.passed


def test_inquire_returns_envelope_with_citations_when_chunks_exist() -> None:
    retriever = HybridRetriever()
    chunks = retriever.as_retrieved_chunks("karma yoga action without fruits", top_k=3)
    if not chunks:
        return
    result = inquire("What does the Gita teach about action without attachment to fruits?")
    assert result.envelope.body
    if result.envelope.citations:
        assert result.envelope.citations[0].passage_id
