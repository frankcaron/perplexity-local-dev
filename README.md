# Perplexity Local Dev

A minimal Python sample project that demonstrates a **Claude Code style, fully agentic SDLC** driven by **Perplexity Local Computer** — an on-device agent that reads, writes, and runs code directly in this repo, guided by **generalized skills**.

The point of this repo is not the code but the *workflow*: how a local agent can take a project from blank repo to tested, documented software end-to-end, with reusable skills doing the heavy lifting.

The entire repo was built progressively using Perplexity's local PPLX Pro (27B) model, tuned for Perplexity Computer. It peaked at about 72 tokens/sec on a 2026 Mac Studio with an M5 Max and 64GB of RAM.

## The Agentic SDLC

Perplexity Local Computer runs entirely on your machine. It has a workspace (this repo), a shell, and a set of skills in the spirit of PROSE that run the SDLC as follows:

1. **Plan** — you describe an outcome and a plan is produced
2. **Develop** — the plan is then used for test-driven development
3. **Review** — the code produced via TDD is then reviewed and hardened
4. **Document** — the approved code is then finalized with human-readable docs
5. **Repeat** — each new request continues from the current repo state, so the project compounds over time.

No cloud round-trips for the file/shell work: everything happens locally, and skills keep the agent's behavior consistent across sessions.

### The Skill Set

This repo ships five homebrew skills that drive the SDLC, under `.agents/skills/`. The first two would be the equivalent to Claude Agents (`agent.md`): 

- **`planner`** (`.agents/skills/planner/`) — The Product Manager of the pipeline. It takes a build instruction, runs discovery on the repo, and writes a **`plan.md`** that specs out how to approach the build: the approach, the files to touch, ordered steps, risks, and testable acceptance criteria. It writes a plan, not code — it is the feeder for `develop`/`builder`, keeping the build's context tight and deliberate.
- **`builder`** (`.agents/skills/builder/`) — The Engineer of the pipeline. It reads a **`plan.md`** and sequences the skills above to take the plan all the way to done: **build** (`develop`) → **verify** → **review & improve** (`code-review`) → **document** (`document`) → final gate. It requires a `plan.md` to exist — if there is none, it stops and redirects to the `planner` skill to produce one, rather than re-planning or running discovery itself. Use it to "ship the feature in `plan.md` end to end."

These "generalized" skills are not tied to the project — they travel with the repo (or your agent) and can apply to any codebase, the way Claude Code skills generalize across repos. Unfortunately, Perplexity as a platform requires you to upload these as skills into your account, and there is no automated pipeline for this today. Nevertheless, the local inference can reference them when present in a repo with the following prompts; it just eats the context window up, which can be problematic with verbose skills given the smaller local models.

## The Test One-Shot

You can build, as I did, with a prompt as follows:

> Use the planner skill to plan out a simple text-based RPG in python that can run via the command line

The `planner` skill will then build out a plan.md with the full spec for the game; essentially, the product requirements doc (PRD) and solution design doc (SDD) in one. It runs discovery on you if it needs to.

> Use the builder skill to execute the plan.md

The `builder` skill then drives the whole delivery in one pass: **develop** built the game and its tests, **code-review** caught and fixed issues, and **document** added the docstrings and call-outs you see here.

### The Output

Included for reference is the one-shot pass output, just as an example of what the local model produces:

- **`main.py`** — the game: a 5-floor dungeon crawl. Each floor holds one enemy (giant rat up to dark knight); you fight with `attack`, check `status`, open the `shop`, or `quit`. You gain XP for every kill, level up (with stat growth and a full heal), and can spend gold on potions and weapon upgrades. Clear the final floor to win; hit 0 HP and you fall.
- **`rpg.py`** — the rules: enemy selection, damage/counter resolution, gold and XP rewards, leveling math (XP thresholds, per-level stat growth), and the shop catalog (potion/weapon prices and effects). Deliberately side-effect-free so the game loop in `main.py` owns all state.
- **`test_main.py`** — 31 tests covering the combat math, leveling and shop rules, and the CLI game loop (fed through stdin, output captured).

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
