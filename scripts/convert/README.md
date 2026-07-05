# Convert Scripts

Helpers that transform raw source artifacts into repository-ready Markdown.

## pdf_to_markdown.py

Converts the Ashram library PDFs downloaded by `scripts/ingest/download_ashram_pdfs.py` into Markdown with YAML frontmatter, following the manifests in `scripts/ingest/manifests/`. Requires `pdftotext` (poppler-utils).

```bash
python scripts/convert/pdf_to_markdown.py                       # all manifests
python scripts/convert/pdf_to_markdown.py --include-restricted  # also convert
                                                                # restricted volumes
                                                                # into gitignored
                                                                # data/markdown/
```

Behavior per volume:

- `full_text: true` volumes (public domain) are written to `content/sources/` with provenance frontmatter, page anchors (`<!-- pdf page N -->`), and `status: draft` pending editorial review.
- `full_text: false` volumes get a committed metadata-only record, and optionally a local, gitignored full-text conversion for personal study.
