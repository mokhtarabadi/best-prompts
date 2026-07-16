---
name: project-memory
description: Smart note-taking and persistent project memory. Automatically saves Manager constraints and proactively retrieves context to prevent hallucinations.
---

# Project Memory Skill

## Purpose

This skill provides persistent, long-term memory for the project. It prevents the Manager from having to repeat project-specific rules, quirks, test commands, or architectural decisions. It uses the `mcp-memory-server` to slice notes into logical namespaces, preventing context bloat.

## When to STORE Memory (Trigger)

Whenever the Manager explicitly states a rule, preference, or architectural constraint (e.g., "For this project, always use flag X" or "Never use Prisma push"), you MUST proactively save this context.

1. Choose a logical `namespace` (e.g., `testing`, `database`, `deployment`, `quirks`).
2. Choose a concise, snake_case `key` (e.g., `prisma_migration_rule`).
3. Call the `store_memory` MCP tool with the content. Ensure `overwrite=True` if updating an existing rule.

## When to RETRIEVE Memory (Trigger)

At the start of EVERY new implementation task (during the Context Phase):

1. Identify the domain of the task (e.g., are we modifying Docker? Writing Jest tests? Editing Auth?).
2. Call `search_memory` using keywords related to that domain, OR call `list_namespaces` and then `read_memory` for specific keys.
3. Inject these retrieved constraints into your reasoning log to ensure you do not violate established project rules.
