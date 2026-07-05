"""Tests for living corpus catalog builder (RF-038)."""

from __future__ import annotations

from scripts.content.build_library_catalog import build_catalog, shelf_id_for_passage


def test_build_catalog_has_gita_shelf() -> None:
    catalog = build_catalog()
    assert catalog["passage_count"] >= 1
    ids = {s["id"] for s in catalog["shelves"]}
    assert "gita" in ids
    gita = next(s for s in catalog["shelves"] if s["id"] == "gita")
    assert gita["state"] == "open"
    assert "gita-ii-47" in gita["passages"]


def test_shelf_id_from_passage_id() -> None:
    assert shelf_id_for_passage({"passage_id": "gita.bhagavad_gita.ch02.v047", "_file": "x"}) == "gita"
