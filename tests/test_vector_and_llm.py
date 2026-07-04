from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_tfidf_vector_store_search() -> None:
    from packages.rag.vector_store import TfidfVectorStore

    store = TfidfVectorStore()
    store.build_from_records(
        [
            {
                "chunk_id": "a",
                "source_id": "test/a",
                "text": "Agni fire invocation sacrifice",
                "metadata": {"themes": ["agni"], "concepts": ["fire"]},
            },
            {
                "chunk_id": "b",
                "source_id": "test/b",
                "text": "Turiya consciousness om mandukya",
                "metadata": {"themes": ["turiya"], "concepts": ["om"]},
            },
        ]
    )
    hits = store.search("agni fire", top_k=1)
    assert hits
    assert hits[0][0].chunk_id == "a"


def test_hybrid_retriever_prefers_relevant_source() -> None:
    from packages.rag.hybrid_retriever import HybridRetriever
    from packages.rag.vector_store import TfidfVectorStore, load_records_from_jsonl

    chunk_root = Path("data/chunks")
    if not chunk_root.exists():
        return

    records = load_records_from_jsonl(chunk_root)
    store = TfidfVectorStore()
    store.build_from_records(records)
    index_path = Path(".tmp_pytest/test_index.pkl")
    index_path.parent.mkdir(parents=True, exist_ok=True)
    store.save(index_path)

    retriever = HybridRetriever(index_path=index_path)
    hits = retriever.retrieve("Turiya in Mandukya Upanishad", top_k=3)
    assert hits
    assert any("mandukya" in hit.source_id for hit in hits)


def test_orchestrator_fallback_answer() -> None:
    from packages.prompts.llm_client import LLMClient
    from packages.prompts.orchestrator import ask_question
    from packages.rag.hybrid_retriever import HybridRetriever

    result = ask_question(
        "What is dharma?",
        retriever=HybridRetriever(),
        llm_client=LLMClient(api_key=None),
        top_k=3,
    )
    assert result.provider == "fallback"
    assert result.answer


def test_llm_client_requires_api_key() -> None:
    from packages.prompts.llm_client import LLMClient

    client = LLMClient(api_key=None)
    assert not client.available
