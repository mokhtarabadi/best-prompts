---
name: audit-agents
description: Enforces decentralized task management, UI/UX design strictness, and global state constraints within AGENTS.md.
---

# OpenCode Skill: Agent Protocol Auditor

## 🛑 STRICT EXECUTION RULES (Priority 1)
1. **Primary Source of Truth**: You MUST read `AGENTS.md` at the project root using local file read tools.
2. **Read-Only First**: Evaluate the contents of `AGENTS.md` against the Target Audit Criteria before attempting any file modifications.
3. **Immutable Formatting**: If patching is required, maintain the exact Markdown list structure, headers, and spacing of the existing file.

## Target Audit Criteria
The `AGENTS.md` file MUST explicitly contain the following operational constraints, ideally within a `Task Management & OpenCode Rules` section:
- **Decentralized Task Management**: Agents MUST strictly use decentralized, individual task files in the `tasks/` directory (e.g., `tasks/02-feature-name.md`) as their single source of truth.
- **No Monolithic State**: Agents are strictly forbidden from creating, updating, or reading monolithic tracking files at the project root (e.g., `TODO.md`, `STATE.md`).
- **Lifecycle Documentation**: Agents MUST read the active task file before modifying code. Upon completion, they MUST update the active task file and `CHANGELOG.md` to document final status, technical changes, and architectural reasoning.
- **UI/UX Enforcement**: Any UI/UX changes MUST enforce the guidelines defined in the project's `DESIGN.md`.

## Resolution Protocol
1. **Evaluation**: Compare the active `AGENTS.md` text against the Target Audit Criteria.
2. **Patching**: If any constraints are missing, ambiguous, or incorrect, use the `apply_patch` tool to inject the exact missing rules.
3. **Halt on Success**: If the file already complies 100%, DO NOT execute any write operations.

## Summary Phase
Upon completion, output a strict, formatted summary for the Manager:

### Agent Audit Summary
**Audit Status:** [PASSED | FIXED]
**Violations Found:** [List of missing/incorrect rules, or "None"]
**Actions Taken:** [Description of the patch applied, or "File already compliant"]