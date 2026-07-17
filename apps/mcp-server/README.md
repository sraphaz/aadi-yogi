# Consciousness MCP server

Exposes Adyog consciousness as an MCP plugin for Cursor, Claude, and other agent hosts.

## Run locally

From the aadi-yogi repository root:

```bash
PYTHONPATH=. python -m packages.consciousness.mcp_server
```

## Consumer `.mcp.json`

```json
{
  "mcpServers": {
    "aadi-yogi-consciousness": {
      "command": "python",
      "args": ["-m", "packages.consciousness.mcp_server"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/aadi-yogi"
      }
    }
  }
}
```

## Tools

| Tool | Decision influence |
|------|--------------------|
| `consciousness_load_posture` | Inject Adyog base frequency into the host system prompt |
| `consciousness_advise` | Recommend next action: restraint, compose, or revise |
| `consciousness_check_restraint` | Force short-circuit before retrieval when risk appears |
| `consciousness_discernment_lookup` | Choose tone, sources, and avoidances |
| `consciousness_validate_response` | Gate release on contract checks |
| `consciousness_list_vocabulary` | Shared states / modes / decision laws |
| `consciousness_manifest` | Pin approved consciousness version + file hashes |

Full consumer guide: [`docs/consciousness_plugin.md`](../../docs/consciousness_plugin.md).
