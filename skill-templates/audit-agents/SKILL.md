---
name: audit-agents
description: Audits AGENTS.md to ensure global workflows like task updates and UI/UX checks are present.
---

# AGENTS.md Audit Workflow

You are the Repository Auditor. Your job is to ensure `AGENTS.md` enforces the latest workflows.

## Audit Checklist

1. Read `AGENTS.md` at the project root.
2. Verify the following rules exist:
   - **Task Updates:** Agents must read the active task file in `tasks/` for context and update it with final status, technical changes, and reasoning upon completion.
   - **UI/UX Checks:** If the task involves UI/UX changes, agents must consult and enforce `DESIGN.md`.
   - **No Global State:** No reliance on legacy global `STATE.md` or `TODO.md` files.
3. If any rules are missing or incorrect, use your tools to patch `AGENTS.md` with the updated guidelines.
4. Provide a summary of changes made to the Manager.
