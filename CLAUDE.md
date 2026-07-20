# CLAUDE.md

## Repository overview

Agent Learning Hub is an offline-first, runnable learning lab. Its four boundaries are:

- `curriculum/`: public course, projects, resources, schemas and generated navigation data.
- `src/agent_learning_hub/`: tested reference implementation.
- `labs/`: progressive exercises and executable templates.
- `workbook/`: public templates/examples plus ignored local learner data.

The static site is built with MkDocs Material and small JavaScript modules. README and site summaries are generated from curriculum data; do not maintain a second course list by hand.

## Required validation

```powershell
uv sync --all-extras --dev
uv run ruff format --check .
uv run ruff check .
uv run mypy src tools
uv run pytest --cov=agent_learning_hub --cov-branch --cov-report=term-missing
uv run python tools/validate_content.py
uv run python tools/build_readme.py --check
npm ci
npm test
npm run build
uv run mkdocs build --strict
```

Never run live Provider tests in the default gate. Never commit `.env`, personal progress exports, `workbook/local/`, browser notes, or memory databases.

## Safety boundaries

- Do not use `eval()` or `exec()` on model or user input.
- A subprocess with a timeout is not a sandbox.
- Side-effecting tools require explicit approval and an idempotency key.
- Preserve structured tool results; redact external errors before returning them to a model.
- Treat imported progress, Markdown, search text, retrieved web content and model arguments as untrusted.
