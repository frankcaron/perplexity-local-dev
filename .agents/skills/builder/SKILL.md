---
name: builder
description: "End-to-end feature delivery: orchestrate the develop, code-review, and document skills to build a full feature, test it, review and improve it, then document it. Use when asked to 'build a feature end to end', 'ship X', or to take an instruction all the way from idea to tested, reviewed, documented code. Not for a single narrow task (use develop, code-review, or document directly)."
compatibility: "Requires bash on macOS or Linux. Orchestrates the develop, code-review, and document skills, which must be available (same repo or installed). Language-agnostic via the develop skill's discovery. Designed for Perplexity Local models running offline in this repository."
metadata:
  version: "1.0"
  author: frank-caron
  depends:
    - develop
    - code-review
    - document
---

# Builder

You take a feature instruction and drive it **all the way to done**: built,
tested, reviewed, improved, and documented. You are the orchestrator. You do not
re-implement the specialized work yourself — you sequence the three skills that
do it well, and you handle the transitions, verification, and reporting between
them.

## Prerequisite

Confirm the three skills are available before starting:
`develop`, `code-review`, and `document`. In this repo they live under
`.agents/skills/`. If one is missing, say so and either proceed with the ones
that are present (noting the gap) or stop and ask.

## The pipeline

Run these phases **in order**. Each phase is a skill; you provide the context and
verify its output before moving on. Do not skip a phase. If a phase reveals the
feature is infeasible or the instruction is ambiguous in a way that blocks it,
stop and surface that to the user rather than guessing.

### 1. Build — `develop`
Hand the feature instruction to the `develop` skill. It runs discovery (language,
tooling, conventions) and implements the feature with tests in the repo's own
language. **Wait for it to report a green test suite and working program** before
proceeding. Capture its report (files touched, decisions made, verification output).

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

**Feature:** <what was built>
**Language/tooling:** <as discovered by develop>

| Phase | Skill | Result |
|-------|-------|--------|
| Build | develop | <tests: N passed, files touched> |
| Verify | (you)   | <independent run: <result>> |
| Review | code-review | <findings: X blocker, Y major, Z minor; fixes applied> |
| Document | document | <comments added, README call-outs> |
| Final gate | (you) | <full suite: N passed; program: <output>> |

**Remaining recommendations:** <minor/nit items not applied>
**Status:** ✅ Done / ⚠️ Done with caveats / ⛔ Blocked at <phase> — <why>
```
