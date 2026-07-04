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


def test_split_chapters_from_sample_text() -> None:
    gita = load_module("import_gutenberg_gita", Path("scripts/ingest/import_gutenberg_gita.py"))
    sample = """
CHAPTER I
First chapter body.

CHAPTER II
Second chapter body.

CHAPTER III
Third chapter body.
"""
    chapters = gita.split_chapters(sample)
    assert [c.number for c in chapters[:3]] == [1, 2, 3]
    assert "First chapter body." in chapters[0].body


def test_simple_retriever_scores_overlap() -> None:
    from packages.rag.retriever import SimpleRetriever

    retriever = SimpleRetriever(chunk_root=Path("data/chunks"))
    score = retriever.score("agni invocation", "Agni mediates the sacrifice", {"themes": ["agni"]})
    assert score > 0


def test_build_prompt_includes_consciousness_rules() -> None:
    from packages.prompts.builder import build_prompt
    from packages.rag.retriever import SimpleRetriever

    bundle = build_prompt("What is dharma?", retriever=SimpleRetriever(chunk_root=Path("data/chunks")))
    assert "source-grounded" in bundle.system_prompt.lower()
    assert "Question:" in bundle.user_prompt
