# plan.md template

`plan.md` is the contract the builder executes against. Write it at the repo root.
Keep it tight and concrete — a builder reading it cold should be able to start
implementing within a minute. Replace every `<...>`; if a section has no content,
write "N/A — <why>" rather than leaving it empty.

---

```markdown
# Plan: <one-line summary of the build>

## Goal
<1-2 sentences: the deliverable and what "done" looks like.>

## Assumptions
- <any interpretation you chose where the instruction was ambiguous>
- <state "none" if the instruction was unambiguous>

## Discovery summary
<5-10 lines copied from the develop skill's discovery: primary language,
tooling (package/build/test), module layout, linter/formatter, where tests
live, and the existing patterns you'll match. If the repo is greenfield, say so
and list the conventions you will establish.>

## Approach
<Short narrative: the strategy and why. e.g. "add a new module X that owns Y,
hang it off the existing entry point in main.py, keep it side-effect-free so the
loop in main.py keeps owning state." This orients the builder before the steps.>

## Files
| Action | Path | Purpose |
|--------|------|---------|
| create | <path> | <what it does> |
| modify | <path> | <what changes> |

## Steps
1. <concrete, ordered step — each one the builder can execute without re-planning>
2. <...>
3. <...>

Keep steps small and ordered. Each step names what it does and, where useful,
the file it touches. A step is too big if the builder must make a design
decision to complete it.

## Public API / interface
- <any new public function/class/CLI flag: signature and contract>
- <state "none" if internal-only>

## Tests to add
- <test for each new behavior, in the repo's test framework/style>
- <edge/error path and (if a fix) a regression test>

## Risks & open questions
- <anything that could break existing behavior, a backward-compat concern, or a
  decision that still needs the user>
- <state "none" if there are none>

## Acceptance criteria
- [ ] <testable, observable condition — what the builder verifies to call it done>
- [ ] <...>

## Out of scope
- <what this build deliberately does NOT do, so the builder doesn't drift>
```

---

## Checklist (run before handing off)

- [ ] **No code written.** The only file you created/modified is `plan.md`.
- [ ] **Every path is real or exact.** Each file in the Files table either exists
      (you read it) or is an exact path to create.
- [ ] **Steps are executable.** No step requires the builder to make a design
      decision — if one does, split it or resolve it in the plan.
- [ ] **Discovery is grounded.** The summary reflects files you actually read, not
      assumptions.
- [ ] **Acceptance criteria are testable.** Each one maps to something the
      builder can run and observe.
- [ ] **Scope is bounded.** Out of scope is explicit; the plan is the minimal
      path to the goal.
