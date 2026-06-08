---
name: telegram-issue-sync
description: Optional, pure agentic sync of Telegram supergroup topics into local task files and GitHub issues, featuring non-tagged conversation crawling.
---

# Telegram Issue Sync & Discussion Crawler SOP

## Purpose

Provides an optional, highly advanced workflow for syncing actionable Telegram supergroup messages into GitHub Issues and local task files without custom Python scripts, utilizing existing Telegram MCP and `gh` CLI tools. It features "Thread Crawling" to pull in non-tagged messages for discussion context.

## Activation (Strictly Optional)

- This skill is **OPTIONAL**. Do NOT execute or force setup unless:
  - A `telegram-sync.json` file already exists at the project root.
  - **OR** the Manager explicitly commands a sync (e.g., "sync telegram", "@explore search telegram issues").
  - If neither condition is met, silently skip this skill entirely during initialization or normal tasks.

## Local State Schema (`telegram-sync.json`)

Stored at project root to track local configuration and message states:

```json
{
  "config": {
    "project_name": "[Name]",
    "chat_id": "[Chat ID]",
    "topic_id": [Topic ID],
    "target_hashtags": ["bug", "feature", "improve"]
  },
  "last_processed_message_id": 0,
  "processed_ids": [],
  "sync_registry": {}
}
```

## Detailed Workflow

### Phase 1: Verification & Optional Onboarding

1. Check for `telegram-sync.json` at project root.
2. If missing AND the command was explicitly requested:
   - Run the `question` tool to interactively ask the Manager for: `project_name`, `chat_id`, `topic_id`, and `target_hashtags`.
   - Create the `telegram-sync.json` file with the collected config, setting `last_processed_message_id` to `0` and initializing `processed_ids` and `sync_registry`.
3. If missing and NOT explicitly requested:
   - Abort this skill immediately. Do not prompt the user.

### Phase 2: Candidate Fetch & Discussion Crawling

1. **Fetch Message History:** Call the Telegram MCP `telegram_get_history` (or equivalent tool) using the `chat_id` and `topic_id` from the config.
2. **Primary Filter (Actionable Items):** Filter for messages where:
   - Message ID > `last_processed_message_id`
   - Message text contains any of the target hashtags (e.g., `#bug`, `#feature`, `#improve`).
3. **Secondary Filter (Discussion & Non-tagged Replies):** For each matched candidate:
   - Retrieve all replies and subsequent discussions. Use the Telegram tools to search for messages replying to this candidate (`reply_to_message_id` matching candidate's `id`).
   - Fetch neighboring messages around the candidate's timestamp (+/- 10 minutes) in the same topic. Extract the non-tagged dialogue, questions, and decisions made by teammates to capture the full context.
4. **Translation & Title Generation:**
   - Translate any Persian messages (and their crawl-extracted replies) into clear English.
   - **Rule 8 Compliance:** Generate a professional, concise title (<60 chars) prefixed with 'Bug: ', 'Feature: ', or 'Improve: '.
5. **Codebase Correlation:** Scan the workspace using `custom_context_extract_signatures` with keywords from the translated discussion to identify target files.

### Phase 3: Manager Approval & Multi-Sync

1. Present the candidates and their crawled discussions to the Manager using the `question` tool.
2. For each approved candidate:
   - **Local Task:** Generate `tasks/XX-slug.md` (using your task template) with a dedicated `## Telegram Discussion Context` section containing the crawled non-tagged discussion.
   - **GitHub Issue:** Run the non-interactive `gh` CLI:
     `gh issue create --title "[Sync] Generated Title" --body "Detailed Body with Crawled Discussion"`
     Extract the generated GitHub issue number from the output URL.
   - **State Save:** Update `telegram-sync.json` local state (append to `processed_ids`, update `last_processed_message_id`, and add msg ID to `sync_registry` mapping).

### Phase 4: Closing the Loop (Completion Telegram Reply)

1. When a task file inside `tasks/` is marked as completed or successfully approved by the Code Reviewer:
2. Read `telegram-sync.json` to check if the completed task file path exists in `sync_registry`.
3. If a match is found:
   - Extract the corresponding Telegram `msg_id` from the registry map.
   - Call your Telegram MCP tools (`telegram_send_message` or equivalent) to reply directly to the original `msg_id` inside the supergroup topic.
   - **Notification Template:**
     _"The bug/feature reported in this thread has been successfully resolved and committed under Local Task XX (GitHub Issue #YY). Thank you!"_
