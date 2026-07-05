#!/usr/bin/env python3
"""Build daily-word batch JSON for the Darshan PWA (ADR-0004: reviewed batches, not live)."""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = REPO_ROOT / "apps" / "web" / "static" / "data" / "daily-words.json"

# Seed batch — editorially reviewed entries; extend monthly per ADR-0004.
SEED_ENTRIES = {
    "2026-07-04": {
        "passage_id": "gita.bhagavad_gita.ch02.v047",
        "word": {
            "en": "offering",
            "pt": "oferecimento",
            "hi": "अर्पण",
            "it": "offerta",
            "es": "ofrenda",
        },
        "d1": {
            "en": "You have a right to action, but never to its fruits. Let not the fruits be your motive, nor attachment your guide in inaction.",
            "pt": "Tens direito à ação, mas nunca aos seus frutos. Que os frutos não sejam teu motivo, nem o apego teu guia na inação.",
            "hi": "कर्म करने का तुम्हारा अधिकार है, परंतु फल पर नहीं।",
            "it": "Hai diritto all'azione, ma non ai suoi frutti.",
            "es": "Tienes derecho a la acción, pero no a sus frutos.",
        },
        "d2": {
            "en": "Thou hast a right to action, but only to action, never to its fruits.",
            "pt": "Tens direito à ação, mas somente à ação, nunca aos seus frutos.",
            "hi": "कर्म करने का तुम्हारा अधिकार है, कर्म के फल पर नहीं।",
            "it": "Hai diritto all'azione, ma solo all'azione, mai ai suoi frutti.",
            "es": "Tienes derecho a la acción, pero solo a la acción, nunca a sus frutos.",
        },
        "citation": {
            "en": "Bhagavad Gita, II.47 · tr. Sri Aurobindo",
            "pt": "Bhagavad Gita, II.47 · tr. Sri Aurobindo",
            "hi": "Bhagavad Gita, II.47 · tr. Sri Aurobindo",
            "it": "Bhagavad Gita, II.47 · tr. Sri Aurobindo",
            "es": "Bhagavad Gita, II.47 · tr. Sri Aurobindo",
        },
    },
    "2026-07-05": {
        "passage_id": "gita.bhagavad_gita.ch02.v048",
        "word": {"en": "yoga", "pt": "yoga", "hi": "योग", "it": "yoga", "es": "yoga"},
        "d1": {
            "en": "Perform action, abandoning attachment, being equal-minded in success and failure. This equanimity is called yoga.",
            "pt": "Executa a ação, abandonando o apego, igual no sucesso e no fracasso. Esta equanimidade chama-se yoga.",
            "hi": "आसक्ति त्यागकर, सफलता और असफलता में समान रहते हुए कर्म करो। यह समत्व योग है।",
            "it": "Agisci abbandonando l'attaccamento, uguale nel successo e nel fallimento.",
            "es": "Actúa abandonando el apego, igual en el éxito y en el fracaso.",
        },
        "d2": {
            "en": "Perform action, O Dhananjaya, abandoning attachment, being steadfast in success and failure alike.",
            "pt": "Executa a ação, ó Dhananjaya, abandonando o apego, firme no sucesso e no fracasso.",
            "hi": "हे धनंजय, आसक्ति त्यागकर कर्म करो।",
            "it": "Agisci, o Dhananjaya, abbandonando l'attaccamento.",
            "es": "Actúa, oh Dhananjaya, abandonando el apego.",
        },
        "citation": {
            "en": "Bhagavad Gita, II.48 · tr. Sri Aurobindo",
            "pt": "Bhagavad Gita, II.48 · tr. Sri Aurobindo",
            "hi": "Bhagavad Gita, II.48 · tr. Sri Aurobindo",
            "it": "Bhagavad Gita, II.48 · tr. Sri Aurobindo",
            "es": "Bhagavad Gita, II.48 · tr. Sri Aurobindo",
        },
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build daily-words.json for Darshan PWA")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--batch", default=f"{date.today():%Y-%m}-seed")
    args = parser.parse_args()

    payload = {
        "version": "1.0",
        "batch": args.batch,
        "reviewed": True,
        "generated_at": date.today().isoformat(),
        "entries": SEED_ENTRIES,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output} ({len(SEED_ENTRIES)} entries)")


if __name__ == "__main__":
    main()
