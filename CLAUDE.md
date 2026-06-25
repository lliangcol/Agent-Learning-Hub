# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a documentation-only repository — a curated AI Agent learning roadmap. There is no build system, no test suite, and no runnable code. The primary artifact is `README.md`.

## Structure

- `README.md` — the canonical learning roadmap: Stages 0–8 todo list, Project Ladder, and Curated Resources. This is the single source of truth for the roadmap content.
- `index.html` — static web presentation of the roadmap.
- `learning-notes/` — personal learning notes that track one learner's progress through the roadmap. Not part of the public roadmap itself.
- `CONTRIBUTING.md` — contribution guidelines.

## Learning Notes System

The `learning-notes/` directory has a specific workflow:

- **Entry point**: always start by reading `learning-notes/PROGRESS.md`. It records the current stage, resume anchor, and pending tasks.
- **Stage notes**: `learning-notes/stage-N-*.md` files hold the full learning content, answers, corrections, and deliverables for each stage. Each note has a `## 当前进度` section with its own checklist — this is the working tracker for that stage.
- **Template**: `learning-notes/templates/stage-note-template.md` is reused for each new stage note.

**Completion rule**: any checklist item (in a stage note or in `README.md`) may only be marked complete when all of these are true:
1. The learner has answered the checkpoint questions or completed the practice task.
2. The answers have been reviewed and any misunderstandings corrected.
3. The correction is written into the corresponding stage note.
4. `PROGRESS.md` is updated to the next resume anchor.

**Update workflow** (follow this order when updating learning notes):
1. Update the stage note — record concepts, user answers, corrections, and validation.
2. Update `PROGRESS.md` — write the current item, status, resume anchor, pending questions, and next action.
3. Only update `learning-notes/README.md` when adding a new note, template, or learning artifact.

## Contributing

Contributions are README-first. Preferred additions: official docs, official engineering blogs, papers, benchmarks, and runnable open-source repos. Avoid social platform reposts, paid course ads, paywalled content, and link dumps. Resource format:

```markdown
| [Title](https://example.com) | One sentence explaining why it matters. |
```
