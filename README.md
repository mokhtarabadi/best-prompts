# Cognitive Lead AI — V5 Decentralized Task Architecture

This repository is the **V5 evolution** of the Cognitive Lead AI multi-agent system. It has been restructured around decentralized task files, Agent Skills, and Google's official Agentic Workflow constraints, maximizing OpenCode's native context management and reasoning capabilities.

## Purpose

- **Unified Agent Instruction** — `system-prompt.md` is the single source of truth for agent behavior, role definitions, Google-aligned Agentic Reasoning, and the `<opencode_task>` protocol.
- **Agent Skills (`SKILL.md`)** — Instead of a monolithic `AGENTS.md` or flat `stacks/` directory, the system now uses OpenCode's native **Agent Skills** framework for progressive disclosure: `.opencode/skills/*/SKILL.md` for repository rules and `skill-templates/*/SKILL.md` for reusable stack blueprints.
- **Progressive Disclosure** — OpenCode's `skill` tool loads only the relevant `SKILL.md` at the moment it is needed, optimizing context usage and keeping the system prompt lean.

## How to Use This Repository

| File / Directory                            | When to Consult                                                                                                            |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `system-prompt.md`                          | At the start of every session; this is the V5 multi-agent prompt defining all 5 personas and the Agentic Reasoning matrix. |
| `.opencode/skills/sop-maintenance/SKILL.md` | When an AI agent needs to modify this repository itself.                                                                   |
| `skill-templates/*/SKILL.md`                | Before writing code in a specific stack (Node.js, Spring Boot, Flask, Next.js, Android Kotlin/Java).                       |
| `CHANGELOG.md`                              | To review what has changed between versions.                                                                               |
| `tasks/`                                    | To see the active task files and current work items.                                                                       |

## How to Operate: The Brain & The Hands

This system relies on a strict separation of concerns:

- **The Brain (Google AI Studio):** You paste the `system-prompt.md` here. It acts as the Orchestrator. It has _no_ direct access to your files or terminal. It thinks, plans, and generates XML task blocks.
- **The Hands (OpenCode):** Runs locally on your machine. You paste the XML task blocks here. It executes file changes, runs bash commands, triggers Agent Skills, and generates task summaries to feed back to the Brain.

### Scenario A: Phase 0 for a Brand New Project

1. Initialize an empty repository on your machine and start OpenCode.
2. In AI Studio, paste the `system-prompt.md` and say: _"This is a new project. Start Phase 0."_
3. Tell the AI your desired tech stack (e.g., Next.js, Node.js).
4. The AI will generate an implementation task instructing OpenCode to:
   - Copy the relevant stack `SKILL.md` template from your global skills directory.
   - Create `opencode.json` with the required schema.
   - Set up the `tasks/` directory and use the `task-generator` skill to create your first `01-initial-setup.md` task.

### Scenario B: Phase 0 for an Existing Project (Never used this workflow)

1. Open your existing project in OpenCode.
2. In AI Studio, paste the `system-prompt.md` and say: _"This is an existing project. Start Phase 0."_
3. The AI will immediately output an `<opencode_discovery_task>`. Paste this into OpenCode.
4. OpenCode will use its MCP tools to map the directory tree and read core files into a `context-reports/` markdown file.
5. Copy the contents of that report and paste it back into AI Studio.
6. The AI will analyze your existing architecture and design, then generate an implementation task to create `AGENTS.md` (<150 lines), `DESIGN.md` (if UI exists), `opencode.json`, and the `tasks/` directory, locking in your current conventions.

### Scenario C: Migrating a V4 Project to V5

If you have an older project using global `STATE.md` and `TODO.md` files:

1. Open the project locally. Delete `STATE.md` and `TODO.md`.
2. Create a `tasks/` directory.
3. In AI Studio, paste the **new V5 `system-prompt.md`**.
4. Tell the AI: _"Migrate this project from V4 to V5. Generate a task to update `AGENTS.md` and move existing roadmap items into `tasks/01-v5-migration.md`."_
5. Ensure the `task-generator` and `audit-agents` skills are imported into `.opencode/skills/` (or installed globally).

## Repository Structure

```
/
├── README.md                           # This file
├── system-prompt.md                    # V5 Multi-Agent System Prompt
├── CHANGELOG.md                        # Version history
├── tasks/                              # Decentralized task files
├── mcp-context-server/
│   └── server.py                       # FastMCP server for .gitignore-aware file reading & tree
├── .opencode/
│   └── skills/
│       └── sop-maintenance/
│           └── SKILL.md                # Native OpenCode skill for repo rules
    └── skill-templates/                    # Reusable stack blueprints (Agent Skills)
        ├── nodejs-express/
        │   └── SKILL.md
        ├── spring-boot/
        │   └── SKILL.md
        ├── flask-python/
        │   └── SKILL.md
        ├── nextjs/
        │   └── SKILL.md
        ├── android-kotlin/
        │   └── SKILL.md
        ├── android-java-xml/
        │   └── SKILL.md
        └── code-search/
            └── SKILL.md
```

## Custom Code Context MCP

This system uses a local **FastMCP** Python server (`mcp-context-server/server.py`) that runs via `uv run` with zero-install dependency management. It provides deterministic, `.gitignore`-aware file reading and directory tree exploration, using far fewer tokens than raw `grep`/`glob` operations.

### Setup Instructions

This server can be installed locally per-project, or globally for all OpenCode sessions on your machine.

#### Option A: Project-Level Setup (New or Existing Projects)

Best for keeping project dependencies isolated.

1. Copy `mcp-context-server/server.py` into your project root.
2. Ensure it is executable: `chmod +x mcp-context-server/server.py`.
3. Add the following to your project's `./opencode.json`:

```json
{
  "mcp": {
    "custom_context": {
      "type": "local",
      "command": ["uv", "run", "mcp-context-server/server.py"],
      "enabled": true
    }
  },
  "permission": {
    "custom_context_*": "allow",
    "get_directory_tree": "allow",
    "read_source_files": "allow"
  }
}
```

#### Option B: Global Setup (System-wide)

Best if you want this codebase exploration tool available in _every_ terminal directory automatically.

1. Create a global directory for the server: `mkdir -p ~/.config/opencode/mcp-context-server`
2. Copy the `server.py` script into that directory.
3. Make it executable: `chmod +x ~/.config/opencode/mcp-context-server/server.py`.
4. Open your global config at `~/.config/opencode/opencode.json` and add the absolute path:

```json
{
  "mcp": {
    "custom_context": {
      "type": "local",
      "command": [
        "uv",
        "run",
        "/Users/<YOUR_USER>/.config/opencode/mcp-context-server/server.py"
      ],
      "enabled": true
    }
  },
  "permission": {
    "custom_context_*": "allow",
    "get_directory_tree": "allow",
    "read_source_files": "allow"
  }
}
```

_(Note: Replace `/Users/<YOUR_USER>` with your actual home directory path)._

### How It Works

1. `opencode.json` configures the custom context server as a local MCP server.
2. When OpenCode needs to explore code, it uses `get_directory_tree` and `read_source_files` tools.
3. All file reads respect `.gitignore` rules and skip binary/large files automatically.
4. The strategy is documented in `skill-templates/code-search/SKILL.md`.

### Available Tools

- `get_directory_tree` — Generates an ASCII tree of the directory structure, respecting `.gitignore`.
- `read_source_files` — Reads multiple source files or directories and saves their contents into a local Markdown report inside the `context-reports/` directory, returning the file path to prevent context bloat.

## Global Skills Deployment

To make the `code-search` skill (or any other reusable skill) available in _every_ terminal directory on your machine automatically, copy the skill folder into your global OpenCode configuration path.

### Step-by-Step Global Installation:

1. **Create the global skills directory** (if it does not exist yet):

   ```bash
   mkdir -p ~/.config/opencode/skills
   ```

2. **Copy the desired skill folder** into the global skills directory:
   For example, to install our custom `code-search` skill globally:

   ```bash
   cp -r skill-templates/code-search ~/.config/opencode/skills/
   ```

3. **Verify the installation:**
   In any folder on your machine, start OpenCode and run:
   ```bash
   /help
   ```
   Under the available skills list, you will see `code-search` listed. You can now use it in any project by asking:
   ```plaintext
   @explore find the main router using the code-search skill
   ```

## Key V5 Changes

- **Decentralized task architecture** — global `STATE.md` and `TODO.md` replaced by isolated task files in `tasks/` directory.
- **Brain/Hands separation codified** — `system-prompt.md` explicitly declares AI Studio as the text-only Orchestrator and OpenCode as the local execution agent.
- **New Agent Skills** — `task-generator` for creating numbered task files and `audit-agents` for enforcing `AGENTS.md` workflows.
- **Phase 0 UI/UX traversal** — Project Planner now instructs OpenCode to perform deep source code analysis for `DESIGN.md` generation.
- **Runtime model updated** — Gemini 3.5 Flash renamed to Gemini throughout the system prompt.

## Contributing

See `.opencode/skills/sop-maintenance/SKILL.md` for the rules that AI agents must follow when modifying this repository.

## Future Architectural Roadmap (TODOs)

1. **Automated Pull Request Integration:** Upgrade the final Code Reviewer step to automatically branch, commit, and open a PR via GitHub CLI (`gh pr create`) instead of committing locally to `main`.
2. **Epic and Milestone Tracking:** Create an `epics/` directory and update the `task-generator` skill to link individual tasks to parent epics for better macro-level project tracking.
3. **Dedicated `testing-strategy` Skill:** Create a template enforcing Test-Driven Development (TDD) or strict coverage thresholds, ensuring OpenCode writes tests before or alongside implementation code.
4. **Database Migration Management:** Create a `database-migration` skill to strictly forbid direct schema alterations, forcing the use of standard migration tools (Prisma, Alembic, Flyway) for safe, repeatable deployments.
