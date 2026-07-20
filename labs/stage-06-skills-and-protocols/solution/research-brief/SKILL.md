---
name: research-brief
description: Build a concise research brief from explicitly provided local Markdown notes, preserving source paths and separating evidence from inference. Use when asked to synthesize two or more local notes into a sourced brief without web access or external side effects.
---

# Research Brief

1. Confirm every input is an explicitly provided local Markdown file. Do not discover unrelated files.
2. Run `scripts/collect_notes.py <paths...>` to produce deterministic source records.
3. Group claims by topic. Label unsupported synthesis as inference.
4. Use `assets/brief-template.md` for the final structure.
5. Cite each factual paragraph with one or more source paths.
6. Stop with a missing-evidence section when the notes do not support a requested claim.

Never modify source notes, browse the web, or send the brief externally.
