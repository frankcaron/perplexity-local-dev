---
name: develop
description: "Implement a plan.md (or, if none exists, a set of instructions) into working, tested code in the repo's own language and conventions, using the plan as the source of truth. Use when asked to build a feature, add a function, fix a bug, scaffold code, or 'implement X' in this repo — and to 'build the feature in plan.md'. Not for reviewing existing code (use code-review) or for one-off questions."
compatibility: "Requires bash on macOS or Linux. Expects a plan.md at the repo root (from the planner skill) as its primary input; if absent, falls back to discovery. Language-agnostic: reuses the plan's discovery summary or detects the repo's language and tooling at runtime. Designed for Perplexity Local models running offline in this repository."
metadata:
  version: "1.1"
  author: frank-caron
  requires:
    - plan.md
---

# Develop

You turn a **`plan.md`** into working, tested code that belongs in this
repository. You build from the plan, then verify in the repo's own language and
conventions. You are building and verifying, not reviewing, and not planning.

The plan is your source of truth. It already carries the goal, the files to
touch, the ordered steps, the tests to add, and a **discovery summary** (language,
tooling, layout, conventions) produced by the `planner` skill. Implement *from*
the plan — do not re-derive the approach, and do not guess where the plan is
silent unless you have to.

## The loop

1. **Read the plan.** Confirm a `plan.md` exists at the repo root and read it:
   goal, files, steps, tests, acceptance criteria, and its discovery summary.
   - **If it exists:** use it as your instruction. Its discovery summary is the
     source of truth for language/tooling/conventions — adopt it rather than
     re-deriving. Implement exactly what the plan specs out.
   - **If it does not exist:** do not guess. Say so, and either (a) run discovery
     yourself (`bash .agents/skills/develop/scripts/detect-language.sh`, then walk
     `references/discovery.md`) and build a minimal plan inline before
     implementing, or (b) — when invoked by the `builder` — stop and hand back to
     the `planner` skill to write `plan.md` first. State clearly which path you
     took.
   - **If the plan is ambiguous or infeasible:** ask one focused question, or stop
     and surface the gap. Do not silently invent scope the plan did not name.

2. **Confirm the discovery.** Take the plan's discovery summary. Spot-check it
   against the repo (the manifest, a couple of the real files it references, the
   test framework) to confirm it is accurate before you build. If the plan's
   summary is stale or wrong, note the correction and proceed with the corrected
   facts. If no plan exists and you ran discovery in step 1, use that summary.

3. **Implement.** Write the code in the plan's language, matching the conventions
   from the discovery summary, following the plan's files and steps in order. Add
   the tests the plan lists. Follow `references/build.md`.

4. **Verify end-to-end.** Run the actual program/command and the test suite, and
   check the results against the plan's acceptance criteria. Iterate until green
   and every acceptance criterion is met. Do not claim success from "it looks
   right" — show the real output.

5. **Report.** Summarize: what you built, the files touched, the commands you ran
   and their results, how each acceptance criterion was met, and anything the
   user should know (new deps, new commands, decisions you made). Offer to run
   the `code-review` skill on the result.

## Hard rules

- **Build from the plan, not from guesses.** When a `plan.md` exists, its files,
  steps, and discovery summary are the source of truth. Do not re-plan or
  re-derive the approach; if the plan is wrong or infeasible, surface it rather
  than silently improvising.
- Match the repo's existing language and conventions (from the plan's discovery
  summary); never introduce a second language or a competing framework/tooling
  without saying why.
- Do not over-build: no speculative features, no refactoring of unrelated code,
  and nothing the plan did not ask for.
- Always add tests for new behavior and run them before reporting. Every new
  public function needs at least one test, and no test may assert only that no
  exception is thrown — each must check a concrete expected value or state.
- Keep changes to public interfaces backward-compatible unless the plan or the
  instruction explicitly requires a break.
- Every claim about behavior must be backed by a command you actually ran.

## When the repo is empty or greenfield

If discovery finds no code, say so, and establish sensible conventions for the
language the instruction implies (state them explicitly). Default to a minimal,
idiomatic structure: source file(s), a test file, and project config for the
language's standard tooling.

## Report format

```markdown
## Implementation: <one-line summary>

**Plan:** plan.md (<goal, one line>) — or "no plan; ran discovery" / "no plan; handed back to planner"
**Language/tooling:** <from the plan's discovery summary, or detected>
**Files:** <created / modified>
**Verification:** <commands run and their real output, e.g. `pytest` → 3 passed>
**Acceptance criteria:** <each criterion and how it was met>
**Decisions:** <any assumptions, corrections to the plan's discovery, or trade-offs you made>
**Suggested next step:** <e.g. run the code-review skill on this change>
```
