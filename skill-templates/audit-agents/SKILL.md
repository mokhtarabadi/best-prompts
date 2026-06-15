---
name: audit-agents
description: Enforces decentralized task management, UI/UX design strictness, and global state constraints within AGENTS.md.
---

# OpenCode Skill: Agent Protocol Auditor

Use this skill in two modes:

- **Phase 0 (Generation):** When `AGENTS.md` does not exist yet — generate it from the template below.
- **Audit Mode (Existing):** When `AGENTS.md` already exists — audit and patch it against the Target Audit Criteria.

---

## Mode 1: Phase 0 — Generate AGENTS.md

Use this when a project has no `AGENTS.md` yet (new project onboarding).

### Workflow

1. Read the project's existing context (package configs, README, tech stack files) to determine the project name, description, and relevant tech stack skills.
2. Generate `AGENTS.md` at the project root using the template below.
3. Fill in the `[bracketed]` placeholders with the actual project details.
4. Confirm the file was created.

### AGENTS.md Template

```markdown
# [Project Name] — Project Context Hub

## Project Overview

[Brief description of the project, its purpose, and tech stack]

## Setup & Dev Commands

- Build: [build command, e.g., npm run build]
- Test: [test command, e.g., npm test]
- Lint: [lint command, e.g., npm run lint]
- Dev: [dev server command, e.g., npm run dev]

## Actionable Guardrails (Do's & Don'ts)

- **Don't** [common anti-pattern to avoid]
  -> **Do** [preferred alternative]
- **Don't** [another anti-pattern]
  -> **Do** [preferred alternative]

## Documentation Sync Rules

When modifying this repository, you must keep these files synchronized:

1. Active task file in `tasks/` (single source of truth for current work items)
2. `CHANGELOG.md` (Keep a Changelog format)
3. `DESIGN.md` (UI/UX design system, if modified)
4. Relevant `SKILL.md` files (if structural patterns were altered)

## 🛑 CORE FILE LOCATIONS

You MUST strictly adhere to these exact paths. Do not create duplicates elsewhere:

- **Global Rules:** `AGENTS.md` (Root)
- **UI/UX Specs:** `DESIGN.md` (Root)
- **Agent Skills:** `.opencode/skills/<skill-name>/SKILL.md` (Local workspace)
- **Active Tasks:** `tasks/<task-number>-<name>.md`

## 🛑 SKILL LOADING RULES

You MUST follow these skill loading rules in every session:

- **Task-Generator Skill:** Before creating any new task file, you MUST load the `task-generator` skill using the `skill` tool to ensure the correct template format with `<!-- BEGIN_GIT_DIFF -->` / `<!-- END_GIT_DIFF -->` markers.
- **Project Skills:** Before implementing any task, you MUST load every available skill matching the project's tech stack (e.g., `[android-kotlin]`, `[spring-boot]`, `[react-vite]`). If a relevant skill exists, it MUST be loaded — this enforces framework-specific conventions and architectural rules.

## 🛑 MANDATORY END-OF-TASK SEQUENCE

When finishing a task, you MUST execute these exact steps in order:

1. **Write your Summary:** Manually write your architectural reasoning, local TODO checks, and execution notes into the active `tasks/XX-task.md` file under "OpenCode Execution Log".
2. **Call MCP Tool:** Call the `custom_context_stage_and_inject_diff` MCP tool passing the task file path to automatically `git add .` and inject the factual code diff.
3. **Notify Manager:** Output exactly: "Task ready. Manager, please copy the contents of `tasks/XX-task.md` and send it back to the AI Studio Brain for review."
```

---

## Mode 2: Audit & Patch Existing AGENTS.md

### 🛑 STRICT EXECUTION RULES (Priority 1)

1. **Primary Source of Truth**: You MUST read `AGENTS.md` at the project root using local file read tools.
2. **Read-Only First**: Evaluate the contents of `AGENTS.md` against the Target Audit Criteria before attempting any file modifications.
3. **Immutable Formatting**: If patching is required, maintain the exact Markdown list structure, headers, and spacing of the existing file.

### Target Audit Criteria

The `AGENTS.md` file MUST explicitly contain the following operational constraints, ideally within a `Task Management & OpenCode Rules` section:

- **Core File Locations**: MUST explicitly list paths for `AGENTS.md`, `DESIGN.md`, `tasks/`, and `.opencode/skills/`.
- **Decentralized Task Management**: Agents MUST strictly use decentralized, individual task files in the `tasks/` directory as their single source of truth.
- **No Monolithic State**: Agents are strictly forbidden from creating `TODO.md` or `STATE.md`.
- **Mandatory End-Of-Task Sequence**: MUST explicitly mandate a 3-step completion process: 1) Write manual reasoning in the task file. 2) Call the `custom_context_stage_and_inject_diff` MCP tool. 3) Notify the Manager.
- **UI/UX Enforcement**: Any UI/UX changes MUST enforce the guidelines defined in the project's `DESIGN.md`.
- **Task-Generator Skill Loading**: `AGENTS.md` MUST explicitly instruct OpenCode to load the `task-generator` skill before creating new task files.
- **Project Skill Loading**: `AGENTS.md` MUST explicitly instruct OpenCode to load every available skill matching the project's tech stack before task implementation.

### Resolution Protocol

1. **Evaluation**: Compare the active `AGENTS.md` text against the Target Audit Criteria.
2. **Patching**: If any constraints are missing, ambiguous, or incorrect, use the `apply_patch` tool to inject the exact missing rules.
3. **Halt on Success**: If the file already complies 100%, DO NOT execute any write operations.

### Summary Phase

Upon completion, output a strict, formatted summary for the Manager:

### Agent Audit Summary

**Audit Status:** [PASSED | FIXED]
**Violations Found:** [List of missing/incorrect rules, or "None"]
**Actions Taken:** [Description of the patch applied, or "File already compliant"]
