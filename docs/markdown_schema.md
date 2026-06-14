# Markdown Schema

Markdown source files under `content/sources/` should use YAML frontmatter as the first block in the file.

## Required Fields

```yaml
id:
title:
source_type:
tradition:
themes:
status:
```

## Additional Required Fields For Primary Texts

```yaml
citation:
copyright_status:
```

## Recommended Fields

```yaml
author:
source_title:
section:
language_original:
language_current:
translator:
concepts:
deities:
practices:
use_for:
avoid_for:
related_sources:
notes:
```

## Conventions

- `id` should be stable and path-like.
- `tradition`, `themes`, `concepts`, `deities`, and `practices` should usually be lists.
- `status` should describe lifecycle state such as `template`, `draft`, `review`, or `approved`.
- `citation` should be specific enough for later verification, or clearly marked `TBD` when exact reference work remains to be confirmed.
