---
name: telegram-message-export
description: Intelligently exports a range of Telegram messages (text, media, voice notes) into a numbered folder, capturing reply hierarchies, and packing them into a ZIP archive.
---

# Telegram Message Export Skill

## Purpose

Extracts a highly contextual range of Telegram messages. It automatically resolves dynamic starting/ending points, extracts text and media files side-by-side, explicitly documents reply relationships to preserve conversation trees, and packages the result into a ZIP file.

## Input Methods

Accept the boundaries of the export dynamically based on the Manager's prompt:

1. **Start & End Bounds**: Can be explicit Message IDs, Message Links (`t.me/c/CHAT_ID/MSG_ID`), or exact text snippets (which you will search for to resolve the ID).
2. **Start Point + Context Window**: A starting link/ID and a request like "and the next 50 messages".

## Output

A ZIP file at the path: `<workspace>/telegram-exports/telegram-export-{unix_timestamp}.zip`
Inside, files are numbered sequentially by ascending message ID:

- `1.txt` (Contains sender, date, reply metadata, and text content)
- `1.jpg` (If the message included an image)
- `2.txt`
- `2.ogg` (If the message was a voice note)

## Detailed Workflow

### Phase 1: Input Parsing & Boundary Resolution

All Telegram calls in this skill pass `account` if the user provides one.

1. Determine `chat_id` and the `from_id` / `to_id` bounds.
2. If the user provides a link:
   - `t.me/c/CHAT_ID/MSG_ID` — parse the numeric `CHAT_ID` and `MSG_ID`. Prepend `-100` to `CHAT_ID` to form the full chat_id.
   - `t.me/username/MSG_ID` — call `telegram_resolve_username(username=username, account=account)` to get the `chat_id`, then extract `MSG_ID`.
3. If the user provides a text snippet as a boundary, use `telegram_search_messages(chat_id=chat_id, query=snippet, limit=5, account=account)` to locate the exact `msg_id`.
4. Establish the final `[from_id, to_id]` range. If the user requested a context size instead of an end bound, calculate `to_id = from_id + context_size`.

### Phase 2: Contextual Message Fetching

1. Call `telegram_get_history(chat_id=chat_id, limit=200, account=account)` to retrieve recent messages. If the range extends beyond the returned batch, paginate by calling again with a larger limit or using the last returned message ID.
2. Filter the returned list to keep only messages where `id >= from_id` and `id <= to_id`.
3. Sort the filtered messages strictly by `id` in ascending order.
4. If the filtered list is empty, abort with a clear message. Do not create an empty ZIP.
5. **Range guard:** If the range spans more than 200 messages, warn the Manager via the `question` tool and ask for confirmation before proceeding. This skill is designed for focused extraction, not bulk archiving.

### Phase 3: Intelligent File Extraction & Reply Mapping

1. Create directory: `mkdir -p <workspace>/telegram-exports/telegram-export-{unix_timestamp}/`
2. Set counter `n = 1`.
3. For each message in the sorted list:

   **Step A: Text & Metadata Sidecar (`{n}.txt`)**
   - You MUST create a `{n}.txt` file for _every_ message, even if it's just media or an unsupported type.
   - Extract `reply_to_message_id`. If it exists, explicitly document it so the LLM can reconstruct the thread later.
   - Format of `{n}.txt`:

     ```text
     Message ID: {message.id}
     From: {sender_name_or_id}
     Date: {date}
     Reply To Message ID: {reply_to_message_id | 'None'}
     Message Type: {text | photo | voice | video | document | sticker | poll | service | unsupported}

     [Content]
     {message_text_or_caption | '[No text content]'}
     ```

   - For polls, write the poll question and options as the content.
   - For service messages (member joined, title changed, etc.), write the service action description.
   - If the message has no extractable content, write `[No extractable content]`.

   **Step B: Media Extraction**
   - If the message contains media (photo, voice note, video, document):
     - Call `telegram_get_media_info(chat_id=chat_id, message_id=message.id, account=account)` to determine the file extension.
     - Call `telegram_download_media(chat_id=chat_id, message_id=message.id, file_path="<export_dir>/{n}.{ext}", account=account)` to save the file.
     - Note: Voice notes download as `.ogg` automatically.

   **Step C:** Increment `n = n + 1`.

### Phase 4: Archiving and Cleanup

1. Run the bash zip command:
   ```bash
   cd <workspace>/telegram-exports && zip -r telegram-export-{unix_timestamp}.zip telegram-export-{unix_timestamp}/
   ```
2. Delete the temporary directory:
   ```bash
   rm -rf <workspace>/telegram-exports/telegram-export-{unix_timestamp}/
   ```

### Phase 5: Notification

Output EXACTLY:
"✅ Contextual Telegram export complete.
Range: {from_id} to {to_id}
Total items processed: {n-1}
Archive path: <workspace>/telegram-exports/telegram-export-{unix_timestamp}.zip"
