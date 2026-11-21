---
name: develop
description: "Take a set of instructions, run discovery on the repository, then implement the change in the repo's own language and conventions. Use when asked to build a feature, add a function, fix a bug, scaffold code, or 'implement X' in this repo. Not for reviewing existing code (use code-review) or for one-off questions."
compatibility: "Requires bash on macOS or Linux. Language-agnostic: detects the repo's language and tooling at runtime. Designed for Perplexity Local models running offline in this repository."
metadata:
  version: "1.0"
  author: frank-caron
---

# Develop

You turn a set of instructions into working, tested code that belongs in this
repository. You discover first, then build in the repo's own language and
conventions. You are building and verifying, not reviewing.

## The loop

1. **Understand the instruction.** Restate the requested outcome in one or two
   sentences. Identify the deliverable (a function, a CLI command, a module, a
   fix) and the acceptance criteria — what "done" looks like. If the instruction
   is ambiguous in a way that changes the design, ask **one** focused question
   before proceeding; otherwise pick the most reasonable interpretation and state it.

2. **Run discovery.** Run `bash .agents/skills/develop/scripts/detect-language.sh`
   from the repo root to identify the primary language and tooling. Then walk
   `references/discovery.md`: read the real files that are closest to what you're
   about to write and learn the repo's layout, naming, error handling, import
   style, test framework, and docs structure. Produce a short discovery summary.

3. **Plan.** From the discovery summary, list the files you will create or edit,
   the public API you'll expose, and the tests you'll add. Keep it minimal — the
   smallest thing that fully satisfies the instruction.

4. **Implement.** Write the code in the detected language, matching the
   conventions you found. Add the tests. Follow `references/build.md`.

5. **Verify end-to-end.** Run the actual program/command and the test suite.
   Iterate until green. Do not claim success from "it looks right" — show the
   real output.

6. **Report.** Summarize: what you built, the files touched, the commands you ran
   and their results, and anything the user should know (new deps, new commands,
   decisions you made). Offer to run the `code-review` skill on the result.

## Hard rules

- Match the repo's existing language and conventions; never introduce a second
  language or a competing framework/tooling without saying why.
- Do not over-build: no speculative features, no refactoring of unrelated code.
- Always add tests for new behavior and run them before reporting. Every new
  public function needs at least one test, and no test may assert only that no
  exception is thrown — each must check a concrete expected value or state.
- Keep changes to public interfaces backward-compatible unless the instruction
  explicitly requires a break.
- Every claim about behavior must be backed by a command you actually ran.

## When the repo is empty or greenfield

If discovery finds no code, say so, and establish sensible conventions for the
language the instruction implies (state them explicitly). Default to a minimal,
idiomatic structure: source file(s), a test file, and project config for the
language's standard tooling.

## Report format

```markdown
## Implementation: <one-line summary>

**Deliverable:** <what was built>
**Language/tooling:** <detected, e.g. Python 3.12, pytest>
**Files:** <created / modified>
**Verification:** <commands run and their real output, e.g. `pytest` → 3 passed>
**Decisions:** <any assumptions or trade-offs you made>
**Suggested next step:** <e.g. run the code-review skill on this change>
```
