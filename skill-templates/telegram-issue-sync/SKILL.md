---
name: telegram-issue-sync
description: Optional, pure agentic sync of Telegram supergroup topics into local task files and GitHub issues, featuring intelligent intent parsing and reply-tree crawling.
---

# Telegram Issue Sync & Discussion Crawler SOP

## Purpose

Syncs actionable Telegram supergroup messages into GitHub Issues and local `tasks/` files. It features deep "Intent Parsing" — if a Manager tags a message with `#bug` while _replying_ to an older message, this skill autonomously fetches the parent message to construct a complete, contextual narrative.

## Telegram MCP Tool Behavior

All Telegram MCP tool calls accept an optional `account` parameter for multi-account setups. If `account` is set in your config, it is passed to every Telegram call.

### Forum Topic Targeting (Critical)

This MCP implementation does **NOT** expose a `topic_id` parameter. All messages belong to the same flat chat (`chat_id`). Forum topics are identified by the `reply_to` field on messages. To correctly scope operations:

- **Reading messages from a specific topic:** Call `telegram_get_history` with `chat_id`. It returns messages from all topics. Filter the results by `reply_to` — messages belonging to your target topic have `reply_to` matching your `topic_id`.
- **Discovering topics:** Call `telegram_list_topics` with `chat_id`. Returns all forum topics with their `id` and `title`.
- **Sending a message to a specific topic:** You MUST use `telegram_reply_to_message` with `message_id` set to the Topic ID (not `telegram_send_message` — that always lands in the General topic).
- **Reading messages:** `telegram_get_history` returns all messages. Filter by `reply_to == topic_id` to get messages scoped to your topic.

Always use `telegram_list_topics` first to verify the target topic exists before posting.

## Activation & State Management

- **OPTIONAL**: Only run if `telegram-sync.json` exists at the workspace root, or if explicitly invoked by the Manager.
- **State Schema Compliance**: You must strictly adhere to the `telegram-sync.json` format. The `sync_registry` maps a string `msg_id` to an object containing `task_file`, `gh_issue`, and `type`.

## Local State Schema (`telegram-sync.json`)

Stored at project root to track local configuration and message states:

```json
{
  "config": {
    "project_name": "[Name]",
    "chat_id": "[Chat ID]",
    "topic_id": null,
    "account": null,
    "target_hashtags": ["bug", "feature", "improve"]
  },
  "last_processed_message_id": 0,
  "processed_ids": [],
  "sync_registry": {}
}
```

## Detailed Workflow

### Phase 1: Verification & Onboarding

1. Check for `telegram-sync.json` at project root.
2. If missing AND the command was explicitly requested by the Manager:
   - Run the `question` tool to ask for: `project_name`, `chat_id`, `target_hashtags`, optional `topic_id`, optional `account`.
   - Create `telegram-sync.json` with the collected config. Set `last_processed_message_id` to `0`, initialize `processed_ids` and `sync_registry`.
3. If missing and NOT explicitly requested: abort silently.
4. If config exists, extract `config.chat_id`, `config.topic_id`, `config.account`, and `config.target_hashtags`.

### Phase 2: Candidate Fetch & Deep Intent Crawling

All Telegram calls in this phase pass `account` from config if set.

1. **Fetch History:** Call `telegram_get_history(chat_id=chat_id, limit=200, account=account)`. If more messages are needed, paginate with higher limits. Filter by `reply_to == config.topic_id` if forum routing is used.
2. **Identify Actionable Items:** Find messages where `id > last_processed_message_id` containing any `target_hashtags`.
3. **Deep Intent & Reply Crawling (CRITICAL):**
   - For each tagged message, check its `reply_to_message_id`.
   - If the Manager replied to an older message, you MUST fetch that parent message using `telegram_get_message_context(chat_id=chat_id, message_id=reply_to_message_id, context_size=2, account=account)`. This returns the parent with surrounding context.
   - Merge the parent message's context (the "what") with the Manager's tagged message (the "intent/instruction").
   - Also fetch neighboring messages (+/- 5 messages) via `telegram_get_message_context` to capture unstructured discussion around the decision.
4. **Translation & Blueprinting:**
   - Translate Persian text to English.
   - Synthesize the exact intent of the Manager based on the reply chain.

### Phase 3: Task Generation & Multi-Sync

1. Present the parsed candidates to the Manager for approval using the `question` tool.
2. For each approved candidate:
   - **Local Task Generation:** Use the `task-generator` skill to create `tasks/XX-title.md`. Inject the deep intent context:

     ```markdown
     **Msg ID:** {NNN}

     ## Telegram Discussion Context

     **Context/Parent Message:** {parent_text_translated}
     **Manager's Instruction:** {manager_tagged_text_translated}

     ## Codebase Correlation

     {Autonomous analysis of which files likely need changes based on the context}
     ```

   - **GitHub Issue:** Create the issue using the `gh issue create` CLI tool.
   - **State Update:** Update `telegram-sync.json`. Append to `processed_ids`, update `last_processed_message_id`. Add the entry to `sync_registry` using the exact schema:
     `"{msg_id}": { "task_file": "tasks/...", "gh_issue": 123, "type": "BUG" }`

### Phase 4: Non-Actionable Message Tracking

All seen messages with IDs between `last_processed_message_id` and the max candidate ID that do NOT have target hashtags must also be added to `processed_ids` to prevent re-fetching.

### Phase 5: Closing the Loop (Completion Notification)

When a task implementation is completed and the Git diff was injected:

1. Read `telegram-sync.json` -> `sync_registry`.
2. If the completed `task_file` matches an entry, extract the `msg_id`.
3. Call `telegram_reply_to_message(chat_id=chat_id, message_id=msg_id, text="✅ The bug/feature reported in this thread has been resolved and committed under Local Task XX.", account=account)` to reply directly in the correct thread.
