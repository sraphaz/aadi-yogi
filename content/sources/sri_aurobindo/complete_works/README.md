# The Complete Works of Sri Aurobindo (CWSA)

The 37-volume Complete Works, imported from the official library of the Sri Aurobindo Ashram (https://www.sriaurobindoashram.org/sriaurobindo/writings.php).

## What Is Here

- **Full-text volumes** (`status: draft`, `copyright_status: public_domain`): volumes consisting predominantly of works published during Sri Aurobindo's lifetime (he passed in 1950), which are in the public domain in India and most jurisdictions. The text was machine-converted from the official PDFs with `pdftotext`; running headers and footers were removed and PDF page anchors preserved. Editorial review is still pending.
- **Metadata-only records** (`status: metadata_only`): volumes consisting predominantly of posthumously first-published manuscripts, letters or editorial apparatus (e.g. Record of Yoga, the Letters volumes, the Index), over which the Sri Aurobindo Ashram Trust may still hold active copyright, plus volume 9, whose non-Unicode Bengali typesetting defeats machine extraction. These can be downloaded and converted locally for personal study; see `scripts/ingest/README.md`.

## Regenerating

```bash
python scripts/ingest/download_ashram_pdfs.py scripts/ingest/manifests/sri_aurobindo_cwsa.yaml
python scripts/convert/pdf_to_markdown.py scripts/ingest/manifests/sri_aurobindo_cwsa.yaml
```

The per-volume classification and its rationale live in `scripts/ingest/manifests/sri_aurobindo_cwsa.yaml`.
