"""Tests for witness mode (RF-012)."""

from packages.prompts.witness import witness_reflect


def test_witness_empty_entry():
    result = witness_reflect("  ")
    assert result.provider == "witness"
    assert "empty" in result.body.lower() or "nearly" in result.body.lower()


def test_witness_restraint_short_circuit():
    result = witness_reflect("I want to kill myself tonight")
    assert result.restraint is True
    assert result.citation is None


def test_witness_fallback_without_llm(monkeypatch):
    class FakeRetriever:
        def retrieve(self, question, top_k=1):
            from packages.rag.retriever import RetrievedChunk

            return [
                RetrievedChunk(
                    chunk_id="c1",
                    source_id="gita",
                    text="Perform action without attachment to fruits.",
                    score=0.9,
                    citation="Gita II.47",
                    metadata={"tradition": "vedanta", "chunk_index": 0},
                )
            ]

    result = witness_reflect(
        "Today I tried to work without grasping at outcomes.",
        retriever=FakeRetriever(),
        llm_client=None,
    )
    assert result.provider == "fallback"
    assert result.citation is not None
    assert "attachment" in result.body.lower() or "weight" in result.body.lower()
