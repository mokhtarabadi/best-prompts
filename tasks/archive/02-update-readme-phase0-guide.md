# Task: Update README with Phase 0 & Migration Guides

**Type:** improvement
**Status:** completed

## Goal

Add clear instructions to the README on how to use the Brain/Hands split, execute Phase 0 for new/existing projects, and migrate V4 projects to V5.

## Manager's Notes

- Emphasize that AI Studio is the Brain (gets the prompt) and OpenCode is the Hands (gets file access).
- Document the V5 migration path.

## Local TODOs

- [x] Update README.md with the operational guide
- [x] Run Prettier on README.md
- [x] Update this task status to completed

## Execution Log & Technical Changes

- Inserted "How to Operate: The Brain & The Hands" section above Repository Structure with three scenarios (New Project, Existing Project, V4 Migration)
- Updated README title from V4 to V5
- Replaced stale `TODO.md` references in the table and file tree with `tasks/`
- Updated `Key V4 Changes` to `Key V5 Changes` with accurate V5 feature listing
- Ran `npx prettier --write "README.md"` — formatting confirmed
