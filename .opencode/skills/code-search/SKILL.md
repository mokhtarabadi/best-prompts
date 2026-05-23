---
name: code-search
description: Rules for navigating the codebase and exploring files.
---

# Code Search Strategy

When exploring the codebase, use the custom context MCP tools to prevent context bloat and respect `.gitignore` rules.

## Workflow
1. Start by calling the `get_directory_tree` tool on the root directory (`.`) or a specific subfolder to map out the structure of the project.
2. Analyze the ASCII tree returned to identify which files are most relevant to your task.
3. Call the `read_source_files` tool passing in a list of specific file paths. The tool will write the code contents to a local Markdown report inside `context-reports/` and return the file path instead of dumping thousands of lines of code into our conversation.
4. Instruct the Manager to open the generated report file from their local editor to inspect the codebase context or copy/paste it as needed.
