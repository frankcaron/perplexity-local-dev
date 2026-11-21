# Perplexity Local Dev

A minimal Python sample project that demonstrates a **Claude Code–style, fully agentic SDLC** driven by **Perplexity Local Computer** — an on-device agent that reads, writes, and runs code directly in this repo, guided by **generalized skills**.

The point of this repo is not the code (it's a hello world) but the *workflow*: how a local agent can take a project from blank repo to tested, documented software end-to-end, with reusable skills doing the heavy lifting.

## The agentic SDLC

Perplexity Local Computer runs entirely on your machine: it has a workspace (this repo), a shell, and a set of **skills** — reusable, natural-language instruction packs it loads on demand. The loop looks like:

1. **Plan** — you describe an outcome ("add a greeting function", "write tests", "do a code review"). The agent inspects the repo and decides the steps.
2. **Scaffold** — it creates files, project config, and structure directly in the workspace.
3. **Code** — it writes and edits source, running it to confirm behavior.
4. **Test** — it adds tests, runs the suite, and fixes failures.
5. **Review** — it applies the `code-review` skill to catch issues, then iterates.
6. **Document** — it keeps the README and inline docs in sync with the code.
7. **Repeat** — each new request continues from the current repo state, so the project compounds over time.

No cloud round-trips for the file/shell work: everything happens locally, and skills keep the agent's behavior consistent across sessions.

## Generalized skills

Skills are plain-text instruction files the agent loads when a task matches. This repo ships two, under `.agents/skills/`:

- **`code-review`** (`.agents/skills/code-review/`) — a language-agnostic, read-only review pass: it collects the diff, reads the changed code and its context, walks a checklist, and reports findings by severity with file/line references and concrete suggested fixes.
- **`develop`** (`.agents/skills/develop/`) — takes a set of instructions, runs discovery on the repo (detecting its language, tooling, and conventions), then implements the change in the repo's own language with tests, and verifies it end-to-end.

Skills are the unit of reuse. A "generalized" skill is not tied to one project — it travels with the repo (or your agent) and applies to any codebase, the way Claude Code skills generalize across repos.

## Run it

```bash
# create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install the project (the dev extra brings in pytest)
pip install -e ".[dev]"

# run the program
python main.py

# run the tests
pytest
```

## Ask the agent

Examples of prompts that drive the loop:

- "Instantiate a basic Python hello-world project."
- "Add a test for `main`."
- "Do a code review on this repo." → loads the `code-review` skill
- "Add a `greet(name)` function with tests."

## License

See [LICENSE](LICENSE).
