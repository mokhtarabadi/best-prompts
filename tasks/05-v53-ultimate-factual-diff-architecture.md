# Task: V5.3 Ultimate Factual Diff Architecture

**Type:** improvement
**Status:** completed

## Goal

Upgrade the system to V5.3.0 Ultimate Architecture by introducing factual Git diff injection via MCP (`stage_and_inject_diff`), structural signature extraction (`extract_signatures`), strict execution guardrails (3-attempt bash failure limit, workspace security), and corresponding documentation updates across all system files.

## Manager's Notes

- Bump `<system_version>` in `system-prompt.md` from `5.2.0` to `5.3.0`.
- Add `import re` and `import subprocess` to `mcp-context-server/server.py`.
- Append two new MCP tools: `extract_signatures` and `stage_and_inject_diff`.
- Append Core File Locations and Mandatory End-Of-Task Sequence blocks to `AGENTS.md`.
- Update audit-agents, task-generator, and code-search SKILL.md templates.
- Apply 6 targeted edits to `system-prompt.md`.
- Sync `.opencode/skills/code-search/SKILL.md` with template changes.
- Add `[5.3.0]` entry to `CHANGELOG.md`.

## Local TODOs

- [x] Initial codebase exploration — read all target files
- [x] Update `mcp-context-server/server.py` — add imports + two new MCP tools
- [x] Update `AGENTS.md` — append anchor blocks
- [x] Update `skill-templates/audit-agents/SKILL.md` — replace Target Audit Criteria
- [x] Update `skill-templates/task-generator/SKILL.md` — replace Step 4 (new template)
- [x] Update `skill-templates/code-search/SKILL.md` — insert Step 2 in Discovery Workflow
- [x] Update `.opencode/skills/code-search/SKILL.md` — sync with template
- [x] Update `system-prompt.md` — 6 specific changes (version, constraint, CR2, doc_phase, summary_phase, reviewer persona)
- [x] Verify Python syntax of MCP server
- [x] Update `CHANGELOG.md` with V5.3.0 entry
- [x] Fix `re.sub` regex escape bug in `stage_and_inject_diff` (lambda instead of backreferences)
- [x] Demonstrate `stage_and_inject_diff` end-to-end on task 04, then clean up
- [x] Fix recursive diff injection — exclude task file from `git diff` via pathspec `:!`
- [x] Fix greedy regex match — use `.*` (greedy) instead of `.*?` (non-greedy) to match first BEGIN to LAST END, preventing corruption when injected diff contains `END_GIT_DIFF`

## OpenCode Execution Log & Reasoning

### Architectural Reasoning

The V5.3.0 upgrade introduces two new MCP tools on the custom context server:

1. **`extract_signatures`** — Uses regex to extract structural signatures (classes, functions, methods, interfaces, arrow functions) from source files. This prevents context bloat during codebase exploration by letting agents understand file structure without loading full file bodies. Targets Python, JS/TS, Go, and similar languages.

2. **`stage_and_inject_diff`** — Automates the end-of-task finalization sequence: stages all changes via `git add .`, extracts the factual `git diff --staged`, and injects it into the task file's `<!-- BEGIN_GIT_DIFF -->
```diff
diff --git a/.opencode/skills/code-search/SKILL.md b/.opencode/skills/code-search/SKILL.md
index cb592db..5fce73b 100644
--- a/.opencode/skills/code-search/SKILL.md
+++ b/.opencode/skills/code-search/SKILL.md
@@ -12,9 +12,10 @@ You are the Executor. Your job is to extract codebase context so the Manager can
 ## Discovery Workflow
 
 1. **Map the Structure:** Call the `get_directory_tree` MCP tool on the target directory (e.g., `.`, `src/`, `packages/`).
-2. **Target Files:** Analyze the ASCII tree to identify the exact files relevant to the Manager's request.
-3. **Compile Report:** Call the `read_source_files` MCP tool, passing the list of targeted file paths. This tool will safely read the files (respecting `.gitignore`) and compile them into a single Markdown file inside the `context-reports/` directory.
-4. **Halt and Handover:** Once the `read_source_files` tool returns the generated file path, **STOP**. Do NOT use your `read` tool to open the report.
-5. **Output Message:** Output the following exact message to the Manager:
+2. **Extract Signatures (Prevent Context Bloat):** Before reading full files, call the `extract_signatures` MCP tool on the target files to understand their structural map (classes/functions) without loading massive file bodies.
+3. **Target Files:** Analyze the ASCII tree to identify the exact files relevant to the Manager's request.
+4. **Compile Report:** Call the `read_source_files` MCP tool, passing the list of targeted file paths. This tool will safely read the files (respecting `.gitignore`) and compile them into a single Markdown file inside the `context-reports/` directory.
+5. **Halt and Handover:** Once the `read_source_files` tool returns the generated file path, **STOP**. Do NOT use your `read` tool to open the report.
+6. **Output Message:** Output the following exact message to the Manager:
    > "✅ Discovery complete. I have compiled the context report here: `[INSERT_FILE_PATH]`.
    > **Manager:** Please upload this file to AI Studio for the Orchestrator's review."
diff --git a/AGENTS.md b/AGENTS.md
index c8faa20..d037887 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -26,3 +26,16 @@ When modifying this repository, you must keep these files synchronized:
 2. `CHANGELOG.md` (Keep a Changelog format)
 3. `DESIGN.md` (UI/UX design system, if modified)
 4. Relevant `SKILL.md` files (if structural patterns were altered)
+
+## 🛑 CORE FILE LOCATIONS
+You MUST strictly adhere to these exact paths. Do not create duplicates elsewhere:
+- **Global Rules:** `AGENTS.md` (Root)
+- **UI/UX Specs:** `DESIGN.md` (Root)
+- **Agent Skills:** `.opencode/skills/<skill-name>/SKILL.md` (Local workspace)
+- **Active Tasks:** `tasks/<task-number>-<name>.md`
+
+## 🛑 MANDATORY END-OF-TASK SEQUENCE
+When finishing a task, you MUST execute these exact steps in order:
+1. **Write your Summary:** Manually write your architectural reasoning, local TODO checks, and execution notes into the active `tasks/XX-task.md` file under "OpenCode Execution Log".
+2. **Call MCP Tool:** Call the `stage_and_inject_diff` MCP tool passing the task file path to automatically `git add .` and inject the factual code diff.
+3. **Notify Manager:** Output exactly: "Task ready. Manager, please copy the contents of `tasks/XX-task.md` and send it back to the AI Studio Brain for review."
diff --git a/CHANGELOG.md b/CHANGELOG.md
index f857c92..b20048c 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -99,6 +99,27 @@ The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
 - Streamlined `AGENTS.md` into a concise Project Context Hub (<150 lines) with a strict guardrail against reading `context-reports/` directly.
 - Re-wrote the `code-search` skill to enforce the `read_source_files` MCP handover workflow, stopping OpenCode from polluting its own context window.
 
+## [5.3.0] — V5.3 Ultimate Factual Diff Architecture
+
+### Added
+
+- **`stage_and_inject_diff` MCP tool** — new MCP tool on the custom context server that stages all Git changes, extracts the factual `git diff --staged`, and injects it into the active task file's `<!-- BEGIN_GIT_DIFF -->` block.
+- **`extract_signatures` MCP tool** — new MCP tool that extracts structural signatures (classes, functions, methods, interfaces) from source files using regex, enabling context-bloat prevention during codebase exploration.
+- **Workspace Security constraint** — OpenCode is strictly forbidden from executing terminal commands that modify files outside the current project workspace. Destructive commands must only target known auto-generated directories.
+- **3-attempt bash failure limit** — CRITICAL RULE 2 now permits a maximum of 3 consecutive repair attempts before halting and outputting a `<failure_report>`.
+- **Core File Locations anchor** in `AGENTS.md` — explicitly lists exact paths for `AGENTS.md`, `DESIGN.md`, `tasks/`, and `.opencode/skills/`.
+- **Mandatory End-Of-Task Sequence** in `AGENTS.md` — mandates a 3-step completion process: write reasoning, call `stage_and_inject_diff`, notify Manager.
+
+### Changed
+
+- **`AGENTS.md`** — appended Core File Locations and Mandatory End-Of-Task Sequence blocks.
+- **Code-review audit criteria** — audit-agents SKILL.md now checks for Core File Locations and Mandatory End-Of-Task Sequence.
+- **Task template** — task-generator SKILL.md now uses `OpenCode Execution Log & Reasoning` and `Factual Git Diff` sections with MCP injection markers.
+- **Code-search workflow** — code-search SKILL.md now includes an `extract_signatures` step before full file reads to prevent context bloat.
+- **`summary_phase`** in `system-prompt.md` — replaced with exact `stage_and_inject_diff` finalization sequence.
+- **`documentation_phase`** in `system-prompt.md` — streamlined to manual logging in task file under `OpenCode Execution Log & Reasoning`.
+- **Code Reviewer persona** — now reviews based strictly on the "Factual Git Diff" block inside the task file, with iteration instructions for rejections.
+
 ## [Unreleased]
 
 ### Added
diff --git a/mcp-context-server/server.py b/mcp-context-server/server.py
index 4b9bacf..3735bc0 100755
--- a/mcp-context-server/server.py
+++ b/mcp-context-server/server.py
@@ -8,6 +8,8 @@
 # ///
 
 import os
+import re
+import subprocess
 import sys
 import time
 from pathlib import Path
@@ -209,5 +211,70 @@ def read_source_files(paths: list[str], max_size: int = 1048576, no_line_numbers
         f"Manager: You can now open `{report_file}` in your local editor to view the codebase context or copy/paste it directly for the AI."
     )
 
+@mcp.tool()
+def extract_signatures(file_path: str) -> str:
+    """Extracts structural signatures (classes, functions, methods) from source files using regex to prevent context bloat."""
+    try:
+        with open(file_path, 'r', encoding='utf-8') as f:
+            content = f.read()
+        
+        # Match class, function, def, interface exports
+        pattern = re.compile(r'^(?:export\s+)?(?:default\s+)?(?:class|func(?:tion)?|def|interface|type)\s+\w+.*$', re.MULTILINE)
+        matches = pattern.findall(content)
+        
+        # Match const/let arrow functions
+        arrow_pattern = re.compile(r'^(?:export\s+)?(?:const|let)\s+\w+\s*=\s*(?:async\s*)?(?:\([^)]*\)|[^=]*)\s*=>.*$', re.MULTILINE)
+        arrow_matches = arrow_pattern.findall(content)
+        
+        all_matches = matches + arrow_matches
+        if not all_matches:
+            return f"No standard structural signatures found in {file_path}."
+            
+        return f"### Signatures in {file_path}\n" + "\n".join(all_matches)
+    except Exception as e:
+        return f"Error extracting signatures from {file_path}: {str(e)}"
+
+@mcp.tool()
+def stage_and_inject_diff(task_file_path: str) -> str:
+    """Stages current changes via Git and intelligently injects the diff into the task file's Git Diff block."""
+    try:
+        # 1. Stage all changes
+        subprocess.run(["git", "add", "."], check=True, capture_output=True)
+        
+        # 2. Extract the diff (EXCLUDING the task file itself to prevent recursive diff bloat)
+        # Using git pathspec magic ':!path' with a RELATIVE path to ignore the task file
+        rel_path = os.path.relpath(task_file_path)
+        diff_cmd = ["git", "diff", "--staged", "--", ".", f":!{rel_path}"]
+        diff_process = subprocess.run(diff_cmd, capture_output=True, text=True)
+        diff_text = diff_process.stdout.strip()
+        
+        if not diff_text:
+            diff_text = "No code changes detected or staged."
+            
+        diff_block = f"\n```diff\n{diff_text}\n```\n"
+
+        # 3. Read the task file
+        with open(task_file_path, 'r', encoding='utf-8') as f:
+            content = f.read()
+
+        # 4. Smart Replacement using Regex (greedy match from first BEGIN to last END)
+        # Using greedy .* to consume everything between the first BEGIN and the LAST END marker,
+        # preventing corruption when injected diff content itself contains 'END_GIT_DIFF'
+        pattern = re.compile(r'<!-- BEGIN_GIT_DIFF -->.*<!-- END_GIT_DIFF -->', re.DOTALL)
+        
+        if not pattern.search(content):
+            return f"Error: Could not find the <!-- BEGIN_GIT_DIFF --> markers in {task_file_path}. Did you alter the template?"
+
+        new_content = pattern.sub(lambda m: f'<!-- BEGIN_GIT_DIFF -->{diff_block}<!-- END_GIT_DIFF -->', content)
+
+        # 5. Write back to the task file
+        with open(task_file_path, 'w', encoding='utf-8') as f:
+            f.write(new_content)
+
+        return f"✅ Success: Changes staged and factual diff intelligently injected into {task_file_path}."
+
+    except Exception as e:
+        return f"❌ Error staging or updating task file: {str(e)}"
+
 if __name__ == "__main__":
     mcp.run(transport="stdio")
diff --git a/skill-templates/audit-agents/SKILL.md b/skill-templates/audit-agents/SKILL.md
index f6e04ac..0ca71aa 100644
--- a/skill-templates/audit-agents/SKILL.md
+++ b/skill-templates/audit-agents/SKILL.md
@@ -12,9 +12,10 @@ description: Enforces decentralized task management, UI/UX design strictness, an
 
 ## Target Audit Criteria
 The `AGENTS.md` file MUST explicitly contain the following operational constraints, ideally within a `Task Management & OpenCode Rules` section:
-- **Decentralized Task Management**: Agents MUST strictly use decentralized, individual task files in the `tasks/` directory (e.g., `tasks/02-feature-name.md`) as their single source of truth.
-- **No Monolithic State**: Agents are strictly forbidden from creating, updating, or reading monolithic tracking files at the project root (e.g., `TODO.md`, `STATE.md`).
-- **Lifecycle Documentation**: Agents MUST read the active task file before modifying code. Upon completion, they MUST update the active task file and `CHANGELOG.md` to document final status, technical changes, and architectural reasoning.
+- **Core File Locations**: MUST explicitly list paths for `AGENTS.md`, `DESIGN.md`, `tasks/`, and `.opencode/skills/`.
+- **Decentralized Task Management**: Agents MUST strictly use decentralized, individual task files in the `tasks/` directory as their single source of truth.
+- **No Monolithic State**: Agents are strictly forbidden from creating `TODO.md` or `STATE.md`.
+- **Mandatory End-Of-Task Sequence**: MUST explicitly mandate a 3-step completion process: 1) Write manual reasoning in the task file. 2) Call the `stage_and_inject_diff` MCP tool. 3) Notify the Manager.
 - **UI/UX Enforcement**: Any UI/UX changes MUST enforce the guidelines defined in the project's `DESIGN.md`.
 
 ## Resolution Protocol
diff --git a/skill-templates/code-search/SKILL.md b/skill-templates/code-search/SKILL.md
index cb592db..5fce73b 100644
--- a/skill-templates/code-search/SKILL.md
+++ b/skill-templates/code-search/SKILL.md
@@ -12,9 +12,10 @@ You are the Executor. Your job is to extract codebase context so the Manager can
 ## Discovery Workflow
 
 1. **Map the Structure:** Call the `get_directory_tree` MCP tool on the target directory (e.g., `.`, `src/`, `packages/`).
-2. **Target Files:** Analyze the ASCII tree to identify the exact files relevant to the Manager's request.
-3. **Compile Report:** Call the `read_source_files` MCP tool, passing the list of targeted file paths. This tool will safely read the files (respecting `.gitignore`) and compile them into a single Markdown file inside the `context-reports/` directory.
-4. **Halt and Handover:** Once the `read_source_files` tool returns the generated file path, **STOP**. Do NOT use your `read` tool to open the report.
-5. **Output Message:** Output the following exact message to the Manager:
+2. **Extract Signatures (Prevent Context Bloat):** Before reading full files, call the `extract_signatures` MCP tool on the target files to understand their structural map (classes/functions) without loading massive file bodies.
+3. **Target Files:** Analyze the ASCII tree to identify the exact files relevant to the Manager's request.
+4. **Compile Report:** Call the `read_source_files` MCP tool, passing the list of targeted file paths. This tool will safely read the files (respecting `.gitignore`) and compile them into a single Markdown file inside the `context-reports/` directory.
+5. **Halt and Handover:** Once the `read_source_files` tool returns the generated file path, **STOP**. Do NOT use your `read` tool to open the report.
+6. **Output Message:** Output the following exact message to the Manager:
    > "✅ Discovery complete. I have compiled the context report here: `[INSERT_FILE_PATH]`.
    > **Manager:** Please upload this file to AI Studio for the Orchestrator's review."
diff --git a/skill-templates/task-generator/SKILL.md b/skill-templates/task-generator/SKILL.md
index 99926b2..5b1fe7d 100644
--- a/skill-templates/task-generator/SKILL.md
+++ b/skill-templates/task-generator/SKILL.md
@@ -32,12 +32,15 @@ You are the Task Generator. Your job is to create structured task files for the
 
    - [ ] Initial codebase exploration
    - [ ] [Specific step 1]
-   - [ ] [Specific step 2]
    - [ ] Verify functionality
 
-   ## Execution Log & Technical Changes
+   ## OpenCode Execution Log & Reasoning
+   _(OpenCode: Manually log your technical changes, file edits, and architectural reasoning here BEFORE calling the MCP tool)_
 
-   _(To be filled by OpenCode during implementation: log technical changes, file edits, and architectural reasoning here)_
+   ## Factual Git Diff
+   <!-- BEGIN_GIT_DIFF -->
+   *(Git diff will be automatically injected here by the MCP tool. Do not edit this block manually)*
+   <!-- END_GIT_DIFF -->
    ```
 
 5. **Halt and Handover:** DO NOT execute the task. Print the exact message: "✅ The task file has been created at `tasks/[filename]` and is ready to be sent to AI Studio." and STOP.
diff --git a/system-prompt.md b/system-prompt.md
index b0de517..b3395ba 100644
--- a/system-prompt.md
+++ b/system-prompt.md
@@ -1,4 +1,4 @@
-<system_version>5.2.0</system_version>
+<system_version>5.3.0</system_version>
 
 <role>
 You are the Cognitive Lead AI running inside Google AI Studio (powered by Gemini), acting as an elite software agency orchestrator.
@@ -48,7 +48,7 @@ CRITICAL INSTRUCTION: The Manager will often send informal, raw text. Before tak
   <persona name="Code Reviewer">
     <trigger>Manager pastes OpenCode's completed Task Summary, PRs are submitted, or Manager requests.</trigger>
     <duty>Audit OpenCode's completed work against the Architect's blueprint, the Designer's UI specs, and the project's conventions.</duty>
-    <behavior>Provide rigorous review formatting: Strengths, Issues, Severity, Recommendations. Output status: APPROVED, APPROVED_WITH_CHANGES, or REJECTED_NEEDS_FIXES.</behavior>
+    <behavior>Read the "OpenCode Execution Log" to understand the agent's logic, but base your strict review ONLY on the "Factual Git Diff" block inside the task file. Provide rigorous formatting: Strengths, Issues, Severity, Recommendations. Output status: APPROVED, APPROVED_WITH_CHANGES, or REJECTED_NEEDS_FIXES. If rejected, explicitly state what OpenCode must fix in the next iteration.</behavior>
   </persona>
 </personas>
 
@@ -115,25 +115,20 @@ You are a very strong reasoner and planner. Before taking any action (either gen
   <bash_phase>
     OPENCODE INSTRUCTION: Run the necessary terminal commands to install dependencies, build, and verify changes.
     CRITICAL RULE 1: ALL bash commands MUST use non-interactive flags (e.g., `npm install -y`, `git commit -m "msg"`, `pytest --no-header`). Do NOT run interactive commands like `vim`, `less`, or `nano`.
-    CRITICAL RULE 2: You MUST run the project's test suite and type-checker. Do not proceed to the summary if tests fail; fix them first.
+    CRITICAL RULE 2: You MUST run the project's test suite and type-checker. If tests fail, you are permitted a MAXIMUM of 3 consecutive repair attempts. If the error persists after 3 attempts, HALT immediately and output a `<failure_report>` for the Manager. Do NOT proceed to the summary phase.
     [List explicit bash commands here]
   </bash_phase>
 
   <documentation_phase>
-    OPENCODE INSTRUCTION: Update the local project documentation files:
-    - Update the active task file in `tasks/` (e.g., `tasks/XX-task-name.md`). Document the final status, technical changes made, local TODOs checked off, and architectural reasoning.
-    - Update `CHANGELOG.md` following the Keep a Changelog format.
+    OPENCODE INSTRUCTION: Update the local project documentation: 1) Open the active task file in `tasks/`. 2) Under "OpenCode Execution Log & Reasoning", manually write your architectural notes, what you changed, and why. Check off any local TODOs. 3) Update `CHANGELOG.md` if necessary.
   </documentation_phase>
 
   <summary_phase>
-    OPENCODE INSTRUCTION: Once you have finished all file edits, verified tests, and updated documentation, you MUST generate a final summary for the Manager.
-
-    ### Task Summary for Reviewer
-    **What was changed:** <OpenCode: Describe the features/fixes you just implemented>
-    **Files modified/created:** <OpenCode: Bullet list of files you actually touched>
-    **Verification run:** <OpenCode: State the exact non-interactive test/build/lsp commands you ran and confirm they succeeded>
-    **Architecture/UI notes:** <OpenCode: Note any design/technical decisions you made during implementation>
-    **Remaining TODOs:** <OpenCode: Note any caveats, limitations, or next steps>
+    OPENCODE INSTRUCTION: You MUST follow this exact finalization sequence:
+    1. Call the `stage_and_inject_diff` MCP tool, providing the exact path to the active task file (e.g., `tasks/XX-task-name.md`). This will securely stage your code and overwrite the diff block without duplicating text.
+    2. Once the tool returns success, you are DONE.
+    3. Output EXACTLY this message to the Manager:
+       "✅ Task implemented, reasoning logged, and Git diff injected. **Manager:** Please copy the entire contents of `[path/to/task.md]` and send it back to the AI Studio Brain for the final Code Review."
   </summary_phase>
 </opencode_implementation_task>
 ```
@@ -159,6 +154,7 @@ You are a very strong reasoner and planner. Before taking any action (either gen
   2. **Inline comments** on non-obvious blocks (e.g., regex patterns, state mutations, performance optimizations, error-recovery paths).
   3. **README or internal docs** when the task adds a new module, endpoint, public API, or changes architecture. A single sentence describing purpose, usage, and constraints suffices.
   Be specific in the `<execution_phase>` about which files need documentation and at what level (module docs, function docs, inline). The default expectation is: **every public function/class gets a docstring; every complex block gets a comment; every new module gets a brief README or header comment.**
+- **Workspace Security:** OpenCode is STRICTLY FORBIDDEN from executing terminal commands that modify files outside the current project workspace. Destructive commands (like `rm -rf`) must ONLY target specific, known auto-generated directories (e.g., `dist/`, `build/`, `target/`).
 </constraints>
 
 <initialization>
```
<!-- END_GIT_DIFF -->
