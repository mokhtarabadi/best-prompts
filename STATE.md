# STATE.md — Cognitive Lead AI SOP Repository

## Current Architecture

This repository serves as the **HQ (Headquarters)** for the Cognitive Lead AI multi-agent system. It contains:
- `system-prompt.md` — V4.1 multi-agent prompt defining personas, Agentic Reasoning, and OpenCode protocol
- `skill-templates/` — Reusable Agent Skills (SKILL.md with YAML frontmatter) for common tech stacks and workflows
  - `code-search/SKILL.md` — Custom context MCP code search strategy (importable template)
- `.opencode/skills/` — Native OpenCode skills for progressive disclosure
  - `sop-maintenance/SKILL.md` — Rules for editing this repository
  - `code-search/SKILL.md` — Custom context MCP code search strategy

## Key Integrations

- **Custom Context MCP** — Local Python FastMCP server (`mcp-context-server/server.py`) for deterministic, `.gitignore`-aware file reading and directory tree exploration. Runs via `uv run` with zero-install dependency management.
- **OpenCode Protocol** — All implementation tasks are dispatched via `<opencode_task>` XML blocks.

## Completed Features

- V4 Multi-Agent Skills architecture migration (monolithic AGENTS.md → SKILL.md)
- 6 stack templates in `skill-templates/` (Node.js, Spring Boot, Flask, Next.js, Android Kotlin, Android Java)
- V4.1 production-ready refinements (MCP support, STATE.md, test enforcement)
- Custom Context MCP server replacing Semble — deterministic `.gitignore`-aware file exploration with `get_directory_tree` and `read_source_files` tools; `read_source_files` writes reports to `context-reports/` to prevent context bloat
- `code-search` template added to `skill-templates/` for reusable import into new projects

## Known Items

- `opencode.json` configured with `custom_context` MCP server (replaced Semble)
- No application code in this repository — documentation/SOP only
