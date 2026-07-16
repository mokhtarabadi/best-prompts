# Task: Download Official Skills from officialskills.sh

**Type:** enhancement
**Status:** completed

## Goal

Download the `doc-coauthoring` (Anthropic) and `design-md` (Google Labs) agent skills from officialskills.sh and add them to the skill-templates/ directory, then update documentation.

## Manager's Notes

- Source: https://officialskills.sh/anthropics/skills/doc-coauthoring → GitHub: anthropics/skills
- Source: https://officialskills.sh/google-labs-code/skills/design-md → GitHub: google-labs-code/stitch-skills (plugins/stitch-design/skills/extract-design-md)
- The `design-md` SKILL.md was found under `extract-design-md` in the `stitch-skills` repo (the standalone `google-labs-code/design.md` repo is a spec/dsl, not the skill itself)

## Local TODOs

- [x] Fetch doc-coauthoring SKILL.md from raw.githubusercontent.com/anthropics/skills/main/
- [x] Locate design-md SKILL.md (found in google-labs-code/stitch-skills/plugins/stitch-design/skills/extract-design-md/)
- [x] Create skill-templates/doc-coauthoring/SKILL.md
- [x] Create skill-templates/design-md/SKILL.md
- [x] Update CHANGELOG.md with new entries under [Unreleased]
- [x] Create this task file

## Execution Log & Technical Changes

- Fetched doc-coauthoring SKILL.md from Anthropic's skills repo at `raw.githubusercontent.com/anthropics/skills/main/skills/doc-coauthoring/SKILL.md`
- Discovered that `google-labs-code/design-md` (404) was incorrect — the actual repo is `google-labs-code/design.md` (with dot), which is a DESIGN.md specification, not a skill
- Found the actual skill at `google-labs-code/stitch-skills/plugins/stitch-design/skills/extract-design-md/SKILL.md`
- Created `skill-templates/doc-coauthoring/SKILL.md` — 480-line workflow for structured doc co-authoring
- Created `skill-templates/design-md/SKILL.md` — 530-line workflow for frontend design system extraction
- Updated `CHANGELOG.md` under [Unreleased] with both new skill entries
