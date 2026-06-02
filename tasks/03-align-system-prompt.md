# Task: Align System Prompt with Google Guidelines

**Type:** improvement
**Status:** completed

## Goal

Integrate Google's official Gemini prompt design strategies, including robust user input processing, strict grounding, and the 9-point agentic reasoning template.

## Manager's Notes

- Must clean up spelling/grammar internally.
- Must HALT and ask clarifying questions if the request is ambiguous.
- Utilize XML tags and best prompting practices.

## Local TODOs

- [x] Rewrite `system-prompt.md` with new blocks.
- [x] Update `CHANGELOG.md` to v5.1.0.
- [x] Run prettier.
- [x] Mark this task as completed.

## Execution Log & Technical Changes

- Rewrote `system-prompt.md` with new `<user_input_processing>` block for input sanitization and clarification halts
- Updated `<agentic_reasoning>` to Google's official 9-point template (added outcome evaluation, persistence, renumbered)
- Added "Input Processing & Clarification" as Step 1 in `<execution_workflow>`
- Inserted `[5.1.0] — Prompt Optimization & Input Processing` into CHANGELOG.md
- Ran `npx prettier --write` on both files — formatting confirmed
