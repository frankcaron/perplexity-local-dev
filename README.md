# Perplexity Local Dev

A minimal Python sample project that demonstrates a **Claude Code–style, fully agentic SDLC** driven by **Perplexity Local Computer** — an on-device agent that reads, writes, and runs code directly in this repo, guided by **generalized skills**.

The point of this repo is not the code but the *workflow*: how a local agent can take a project from blank repo to tested, documented software end-to-end, with reusable skills doing the heavy lifting.

## The Agentic SDLC

Perplexity Local Computer runs entirely on your machine: it has a workspace (this repo), a shell, and a set of **skills** — reusable, natural-language instruction packs it loads on demand. The PROSE-like cycle is implemented as follows:

1. **Plan** — you describe an outcome ("add a greeting function", "write tests"). The `planner` skill inspects the repo and writes a `plan.md` that specs out the approach, files, steps, and acceptance criteria.
2. **Develop** — the `builder` skill runs a squence, starting with `develop` skill runs discovery (detecting the repo's language, tooling, and conventions), then implements the change in that language with tests.
3. **Review** — the `code-review` skill catches issues; the agent iterates until clean.
4. **Document** — the `document` skill adds targeted comments and docstrings and updates the README with key call-outs.
5. **Repeat** — each new request continues from the current repo state, so the project compounds over time.

No cloud round-trips for the file/shell work: everything happens locally, and skills keep the agent's behavior consistent across sessions.

## Generalized skills

Skills are plain-text instruction files the agent loads when a task matches. This repo ships five, under `.agents/skills/`.

The first two would be the equivalent to Claude Agents (`agents.md`), but Perplexity currently doesn't support the concept in the same way (albeit this is changing with the new Teammates feature): 

- **`planner`** (`.agents/skills/planner/`) — the Product Manager of the pipeline. It takes a build instruction, runs discovery on the repo, and writes a **`plan.md`** that specs out how to approach the build: the approach, the files to touch, ordered steps, risks, and testable acceptance criteria. It writes a plan, not code — it is the feeder for `develop`/`builder`, keeping the build's context tight and deliberate.
- **`builder`** (`.agents/skills/builder/`) — the Engineer of the pipeline. It reads a **`plan.md`** and sequences the skills above to take the plan all the way to done: **build** (`develop`) → **verify** → **review & improve** (`code-review`) → **document** (`document`) → final gate. It requires a `plan.md` to exist — if there is none, it stops and redirects to the `planner` skill to produce one, rather than re-planning or running discovery itself. Use it to "ship the feature in `plan.md` end to end."

There are also a handful of supporting skills for the agentic "Engineering" team:

- **`develop`** (`.agents/skills/develop/`) — takes a **`plan.md`** (or, if none exists, a set of instructions) and implements the change in the repo's own language with tests, using the plan's discovery summary as its source of truth rather than re-deriving the approach, then verifies it end-to-end against the plan's acceptance criteria.
- **`code-review`** (`.agents/skills/code-review/`) — a language-agnostic, read-only review pass: it collects the diff, reads the changed code and its context, walks a checklist, and reports findings by severity with file/line references and concrete suggested fixes.
- **`document`** (`.agents/skills/document/`) — improves human readability: it adds targeted comments and docstrings to the code (the *why*, not the *what*) and updates the README with key call-outs, then verifies nothing broke.

These "generalized" skills are not tied to the project — they travels with the repo (or your agent) and applies to any codebase, the way Claude Code skills generalize across repos. 

Perplexity as a platform requires you to upload these as skills into your account, and there is no automated pipeline for this today, but the local inference can reference them when present in a repo with the following prompts.

## The Test One-Shot

It started as a hello world. That was replaced with a one-shot game — a text-based dungeon crawler — using the prompt:

> Use the planner skill to plan out a simple text-based RPG in python that can run via the command line

The `planner` skill builds out a plan.md file with the full spec for the game; essentially, the product requirements doc (PRD) and solution design doc (SDD) in one. It does discovery if it needs to.

> use the builder skill to execute the plan.md

The `builder` skill then drives the whole delivery in one pass: **develop** built the game and its tests, **code-review** caught and fixed issues, and **document** added the docstrings and call-outs you see here.

The entire repo was built progressively using Perplexity's local PPLX Pro (27B) model, tuned for Perplexity Computer. It peaked at about 72 tokens/sec on a 2026 Mac Studio with an M5 Max and 64GB of RAM.

### The Output

- **`main.py`** — the game: a 5-floor dungeon crawl. Each floor holds one enemy (giant rat up to dark knight); you fight with `attack`, check `status`, open the `shop`, or `quit`. You gain XP for every kill, level up (with stat growth and a full heal), and can spend gold on potions and weapon upgrades. Clear the final floor to win; hit 0 HP and you fall.
- **`rpg.py`** — the rules: enemy selection, damage/counter resolution, gold and XP rewards, leveling math (XP thresholds, per-level stat growth), and the shop catalog (potion/weapon prices and effects). Deliberately side-effect-free so the game loop in `main.py` owns all state.
- **`test_main.py`** — 31 tests covering the combat math, leveling and shop rules, and the CLI game loop (fed through stdin, output captured).

### How it works

- **Leveling** — every kill grants 20 XP. The threshold to the next level is `20 * level` (20, 40, 60, ...), so a single kill can push you up several levels if you're behind. On each level up your max HP grows by 10, your weapon damage by 3, and you are fully healed.
- **Shop** — available any time with the `shop` command. A **health potion** costs 15 gold and immediately heals 25 HP (capped at max HP). A **weapon upgrade** starts at 20 gold, rises by 15 per prior upgrade, and permanently adds +5 damage. `use potion` spends a held potion (none are ever held — shop purchases apply immediately).

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
