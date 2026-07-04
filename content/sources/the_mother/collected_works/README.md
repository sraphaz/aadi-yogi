# Collected Works of the Mother (CWM)

The Collected Works of the Mother, mapped from the official library of the Sri Aurobindo Ashram (https://www.sriaurobindoashram.org/mother/writings.php). The downloadable PDFs offered by the Ashram are the French originals (18 volumes); the 17-volume English edition is browsable online only.

## Copyright Handling

The Mother passed in 1973, so her works remain under active copyright of the Sri Aurobindo Ashram Trust (in India until at least 2034), and the Ashram explicitly restricts reproduction. Following `docs/copyright_policy.md`, this folder contains **metadata-only records** for every volume: bibliographic data, themes, descriptions and citations, but no full text.

The ingestion pipeline still works end to end for personal local study: PDFs download into `data/raw/` and full-text conversions land in `data/markdown/`, both gitignored.

```bash
python scripts/ingest/download_ashram_pdfs.py scripts/ingest/manifests/the_mother_cwm.yaml
python scripts/convert/pdf_to_markdown.py scripts/ingest/manifests/the_mother_cwm.yaml --include-restricted
```

If the repository later obtains permission from the Sri Aurobindo Ashram Trust, flipping `full_text` in `scripts/ingest/manifests/the_mother_cwm.yaml` and re-running the converter will materialize the texts here.
