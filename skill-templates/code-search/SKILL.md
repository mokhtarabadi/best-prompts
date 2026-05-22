---
name: code-search
description: Rules for navigating the codebase and exploring files.
---

# Code Search Strategy

When exploring the codebase, use the custom context MCP tools to prevent context bloat and respect `.gitignore` rules.

## Workflow
1. Start by calling the `get_directory_tree` tool on the root directory (`.`) or a specific subfolder to map out the structure of the project.
2. Analyze the ASCII tree returned to identify which files are most relevant to your task.
3. Call the `read_source_files` tool passing in a list of specific file paths (or specific directories) you identified in step 2. This will return the exact file contents with line numbers prefixed.
4. Only load the files you absolutely need.
