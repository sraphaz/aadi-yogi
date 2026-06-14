# Copyright Policy

The repository may track metadata, templates, excerpts, or references for works with different legal statuses. Every source entry should declare a clear status.

```yaml
copyright_status:
  - public_domain
  - permission_required
  - permission_granted
  - internal_use_only
  - metadata_only
  - quotes_only
  - unknown
  - do_not_index
```

## Rules

- Copyrighted works must not be fully included unless permission explicitly allows it.
- Works marked `metadata_only`, `quotes_only`, `permission_required`, `unknown`, or `do_not_index` need restrictive handling.
- Indexing and embeddings must respect the declared status, not just storage access.
- When in doubt, store metadata and templates only.
- During early template work, `verify` may be used as a provisional placeholder until the final canonical status is assigned.
