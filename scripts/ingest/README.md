# Ingest Scripts

Operational helpers that bring external source material into the repository workflow.

## download_ashram_pdfs.py

Downloads the official PDF libraries of the Sri Aurobindo Ashram into the gitignored `data/raw/` tree, driven by the manifests in `manifests/`.

```bash
python scripts/ingest/download_ashram_pdfs.py                 # all manifests
python scripts/ingest/download_ashram_pdfs.py --force         # re-download
```

## manifests/

Declarative YAML manifests describing each collection: download URLs, volume metadata, themes, and the per-volume `full_text` copyright decision that controls whether converted text may be committed to `content/sources/` or must stay local. See the header comments inside each manifest for the classification rationale.

- `sri_aurobindo_cwsa.yaml`: The Complete Works of Sri Aurobindo (37 volumes, 31 PDFs).
- `the_mother_cwm.yaml`: Collected Works of the Mother (18 French PDF volumes).
