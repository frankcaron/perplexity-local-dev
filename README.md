# Perplexity Local Dev

A minimal Python sample project that demonstrates a **Claude Code–style, fully agentic SDLC** driven by **Perplexity Local Computer** — an on-device agent that reads, writes, and runs code directly in this repo, guided by **generalized skills**.

The point of this repo is not the code but the *workflow*: how a local agent can take a project from blank repo to tested, documented software end-to-end, with reusable skills doing the heavy lifting.

## The Agentic SDLC

Perplexity Local Computer runs entirely on your machine: it has a workspace (this repo), a shell, and a set of **skills** — reusable, natural-language instruction packs it loads on demand. Three skills power the loop: **`develop`** builds, **`code-review`** checks, and **`document`** clarifies. The cycle looks like:

1. **Plan** — you describe an outcome ("add a greeting function", "write tests"). The agent inspects the repo and decides the steps.
2. **Develop** — the `develop` skill runs discovery (detecting the repo's language, tooling, and conventions), then implements the change in that language with tests.
3. **Review** — the `code-review` skill catches issues; the agent iterates until clean.
4. **Document** — the `document` skill adds targeted comments and docstrings and updates the README with key call-outs.
5. **Repeat** — each new request continues from the current repo state, so the project compounds over time.

No cloud round-trips for the file/shell work: everything happens locally, and skills keep the agent's behavior consistent across sessions.

## Generalized skills

Skills are plain-text instruction files the agent loads when a task matches. This repo ships four, under `.agents/skills/`:

- **`develop`** (`.agents/skills/develop/`) — takes a set of instructions, runs discovery on the repo (detecting its language, tooling, and conventions), then implements the change in the repo's own language with tests, and verifies it end-to-end.
- **`code-review`** (`.agents/skills/code-review/`) — a language-agnostic, read-only review pass: it collects the diff, reads the changed code and its context, walks a checklist, and reports findings by severity with file/line references and concrete suggested fixes.
- **`document`** (`.agents/skills/document/`) — improves human readability: it adds targeted comments and docstrings to the code (the *why*, not the *what*) and updates the README with key call-outs, then verifies nothing broke.
- **`builder`** (`.agents/skills/builder/`) — the orchestrator. It sequences the three skills above to take a feature instruction all the way to done: **build** (`develop`) → **verify** → **review & improve** (`code-review`) → **document** (`document`) → final gate. Use it to "ship a feature end to end."

Skills are the unit of reuse. A "generalized" skill is not tied to one project — it travels with the repo (or your agent) and applies to any codebase, the way Claude Code skills generalize across repos.

## The Test One-Shot

It started as a hello world. That was replaced with a one-shot game — a text-based dungeon crawler — using the prompt:

> use the builder skill to replace the hello world app with a simple text-based RPG in python that can run via the command line

The `builder` skill drove the whole delivery in one pass: **develop** built the game and its tests, **code-review** caught and fixed issues, and **document** added the docstrings and call-outs you see here.

The entire repo was built progressively using Perplexity's local PPLX Pro (27B) model, tuned for Perplexity Computer. It peaked at about 72 tokens/sec on a 2026 Mac Studio with an M5 Max and 64GB of RAM.

### The Output

- **`main.py`** — the game: a 5-floor dungeon crawl. Each floor holds one enemy (giant rat up to dark knight); you fight with `attack`, check `status`, or `quit`. Clear the final floor to win; hit 0 HP and you fall.
- **`rpg.py`** — the combat rules: enemy selection, damage/counter resolution, and gold rewards. Deliberately side-effect-free so the game loop in `main.py` owns all state.
- **`test_main.py`** — 11 tests covering the combat math and the CLI game loop (fed through stdin, output captured).

## Usage

```bash
# create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install the project (the dev extra brings in pytest)
pip install -e ".[dev]"

# play the game
python main.py

# run the tests
pytest
```

## License

See [LICENSE](LICENSE).
