---
name: builder
description: "End-to-end feature delivery from a plan: read a plan.md, then orchestrate the develop, code-review, and document skills to build the feature, test it, review and improve it, then document it. Use when asked to 'build the feature in plan.md', 'ship X', or to take a plan all the way to tested, reviewed, documented code. Requires a plan.md to exist — if there is none, redirect to the planner skill. Not for a single narrow task (use develop, code-review, or document directly)."
compatibility: "Requires bash on macOS or Linux. Orchestrates the develop, code-review, and document skills, which must be available (same repo or installed). Requires a plan.md at the repo root as input; discovery is the planner skill's job, not the builder's. Language-agnostic via the plan's discovery summary. Designed for Perplexity Local models running offline in this repository."
metadata:
  version: "1.1"
  author: frank-caron
  feeds:
    - develop
  depends:
    - develop
    - code-review
    - document
  requires:
    - plan.md
---

# Builder

You take a **`plan.md`** and drive it **all the way to done**: built, tested,
reviewed, improved, and documented. You are the orchestrator. You do not
re-implement the specialized work yourself — you sequence the skills that do it
well, and you handle the transitions, verification, and reporting between them.

You build *from the plan*. The approach, files, steps, and acceptance criteria
already live in `plan.md` (produced by the `planner` skill). Your only
discovery is confirming that plan exists and is usable — you do not re-derive
the approach, re-run language/tooling discovery, or second-guess the plan.

## Prerequisite: a plan.md must exist

Before doing anything, confirm a `plan.md` exists at the repo root.

- **If it exists:** read it. Confirm it is a usable plan — it names the goal,
  the files to touch, ordered steps, and testable acceptance criteria (the
  structure from `.agents/skills/planner/references/plan-template.md`). If it is
  malformed or clearly incomplete (empty sections, unresolved "TBD", no
  acceptance criteria), stop and surface that to the user rather than guessing.
- **If it does not exist:** **do not proceed with the build.** Do not invent a
  plan, and do not run discovery yourself. Redirect to the `planner` skill so it
  writes the `plan.md` first, then hand the resulting plan back to this builder
  skill to run the pipeline. Report the hand-off: "No `plan.md` found — running
  the `planner` skill to produce one; will resume the build once it exists."

Also confirm the three downstream skills are available: `develop`, `code-review`,
and `document`. In this repo they live under `.agents/skills/`. If one is
missing, say so and either proceed with the ones that are present (noting the
gap) or stop and ask.

## The pipeline

Only run these phases once a usable `plan.md` is confirmed (see the
prerequisite above). Run them **in order**. Each phase is a skill; you provide
the context and verify its output before moving on. Do not skip a phase. If a
phase reveals the feature is infeasible or the plan is wrong in a way that
blocks it, stop and surface that to the user rather than guessing.

### 1. Build — `develop`
Hand the **`plan.md`** to the `develop` skill as its instruction. The plan's
discovery summary already carries the language, tooling, and conventions, so
`develop` implements straight from the plan: the files, steps, and tests it
specs out. **Wait for it to report a green test suite and working program**
before proceeding. Capture its report (files touched, decisions made,
verification output). Do not re-plan — if `develop` says the plan is
inexecutable, stop and surface it rather than improvising a new approach.

### 2. Verify the build
Independently confirm the `develop` skill's claims: run the test suite and the
program yourself and check the output matches what was reported. If it does not,
send the specific failure back to `develop` and repeat until green. Do not let a
phase pass on its own word alone.

### 3. Review & improve — `code-review`
Run the `code-review` skill on the new/changed code (the diff from the build).
It is read-only and reports findings by severity. Then:
- **Blocker / Major findings:** apply the suggested fixes (you may edit code here —
  this is the "improve" step), then re-run the tests to confirm still green.
- **Minor / Nit:** apply the clear, safe ones; list the rest as recommendations.
- If the review finds nothing, say so.
Repeat review→fix→re-test until there are no remaining Blocker/Major findings.

### 4. Document — `document`
Run the `document` skill on the finished feature: add targeted comments/docstrings
and update the README with key call-outs (commands, architecture, where to look
first). Confirm it did not change behavior (its own verification).

### 5. Final gate
- Run the full test suite one last time — it must be green.
- Run the program end-to-end the way a user would and confirm the feature works.
- Confirm the README and code docs are consistent with the final behavior.

## Hard rules

- **No plan, no build.** The builder never starts without a `plan.md`. If there
  is none, redirect to the `planner` skill and stop — do not invent a plan or
  run discovery yourself.
- **You do not discover; the planner did.** Your only discovery is confirming
  `plan.md` exists and is usable. Do not re-run language/tooling discovery or
  re-derive the approach — the plan's discovery summary is the source of truth.
- **Sequence is fixed:** build → verify → review/improve → document → final gate.
  Never document unreviewed code, and never review code that does not yet pass its tests.
- **Delegate, don't duplicate.** Let each skill do its job; your value is the
  orchestration, verification between phases, and the transitions.
- **Every phase must actually run and be verified** — not just "look right."
- **Keep the feature in scope.** No speculative features or unrelated refactors.
- **If a phase fails irrecoverably, stop and report** exactly where and why, with
  what was completed so far. Do not silently skip a phase.

## Report format

```markdown
## Feature delivery: <one-line summary>

**Plan:** plan.md (<goal, one line>)
**Language/tooling:** <from the plan's discovery summary>

| Phase | Skill | Result |
|-------|-------|--------|
| Plan check | (you) | <plan.md confirmed present & usable> |
| Build | develop | <tests: N passed, files touched> |
| Verify | (you)   | <independent run: <result>> |
| Review | code-review | <findings: X blocker, Y major, Z minor; fixes applied> |
| Document | document | <comments added, README call-outs> |
| Final gate | (you) | <full suite: N passed; program: <output>> |

**Remaining recommendations:** <minor/nit items not applied>
**Status:** ✅ Done / ⚠️ Done with caveats / ⛔ Blocked at <phase> — <why>
```
