from __future__ import annotations

import re


OCR_SKIP_PATTERNS = (
    re.compile(r"^Digitized by Google$", re.I),
    re.compile(r"^\d+\s+[A-Z\- ]+UPANISHAD\.?$"),
    re.compile(r"^[IVXLC]+\s+ADHYAYA", re.I),
    re.compile(r"^PAGE\s*$", re.I),
    re.compile(r"^See the editor", re.I),
)

OCR_REPLACEMENTS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bpfirva\b", re.I), "purva"),
    (re.compile(r"\bfsvara\b", re.I), "isvara"),
    (re.compile(r"\bIswara\b"), "Isvara"),
    (re.compile(r"\bPiirai?a\b", re.I), "Purana"),
    (re.compile(r"\bBrah-\s*\n\s*man\b", re.I), "Brahman"),
    (re.compile(r"Brah-\s+man"), "Brahman"),
    (re.compile(r"\bw'ho\b"), "who"),
    (re.compile(r"\bVishiiu\b", re.I), "Vishnu"),
    (re.compile(r"\bVifnu\b", re.I), "Vishnu"),
    (re.compile(r"Vi[\$§]nu", re.I), "Vishnu"),
    (re.compile(r"\bGarufa\b", re.I), "Garuda"),
    (re.compile(r"\bParana\b", re.I), "Purana"),
    (re.compile(r"\bPuraija\b", re.I), "Purana"),
    (re.compile(r"\bYag#avalkya\b"), "Yajnavalkya"),
    (re.compile(r"\bPfirvapragfia\b"), "Purvaprajna"),
    (re.compile(r"\bC'andik[aā]\b", re.I), "Chandika"),
    (re.compile(r"\bMahd-mdyd\b", re.I), "Maha-maya"),
    (re.compile(r"\bSu-ratha\b"), "Suratha"),
    (re.compile(r"\bManv-antara\b"), "Manvantara"),
    (re.compile(r"\bSavai'ioi\b"), "Savarni"),
    (re.compile(r"\bmdyd\b", re.I), "maya"),
    (re.compile(r"\bvai\^ya\b", re.I), "vaishya"),
    (re.compile(r"\bDevi-m&h&tmya\b", re.I), "Devi-mahatmya"),
    (re.compile(r"\bMdhdtmya\b", re.I), "Mahatmya"),
    (re.compile(r"(\w)-\s+(\w)"), r"\1\2"),
    (re.compile(r"  +"), " "),
)


def fix_ocr_text(text: str) -> str:
    for pattern, replacement in OCR_REPLACEMENTS:
        text = pattern.sub(replacement, text)
    return text


def clean_ocr_lines(body: str, *, fix_hyphenation: bool = True) -> str:
    if fix_hyphenation:
        body = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", body)
    lines: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            if lines and lines[-1]:
                lines.append("")
            continue
        if any(pattern.search(line) for pattern in OCR_SKIP_PATTERNS):
            continue
        if line.startswith("*") and len(line) < 120:
            continue
        line = re.sub(r"\s+", " ", line)
        line = fix_ocr_text(line)
        if line:
            lines.append(line)
    while lines and not lines[-1]:
        lines.pop()
    return "\n\n".join(lines).strip()
