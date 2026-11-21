---
name: document
description: "Improve human readability by adding comments and docstrings to code and updating the README with key call-outs. Use when asked to document, add comments, explain the code, improve readability, or update the README/docs for a change. Not for implementing new features (use develop) or reviewing for bugs (use code-review)."
compatibility: "Requires bash on macOS or Linux. Language-agnostic: matches the repo's existing comment and doc conventions. Designed for Perplexity Local models running offline in this repository."
metadata:
  version: "1.0"
  author: frank-caron
---

# Document

You make code and docs easier for a human to read. You add targeted comments and
docstrings to the code, and you keep the README (and other human-facing docs) in
sync with key call-outs. You are clarifying, not rewriting behavior.

## The loop

1. **Scope the target.** Decide what to document: the whole repo, a specific file,
   or the code changed in a recent diff. If the user named a scope, use it. If
   they said "the code" or "the repo," document the most important parts, not every line.

2. **Find the high-value targets.** Run
   `bash .agents/skills/document/scripts/doc-targets.sh` from the repo root. It
   lists source files by size, files with many definitions, entry points, and a
   rough doc-coverage count. Prioritize: entry points, public API, complex logic,
   and any code that currently has **no** documentation.

3. **Learn the conventions.** Read a couple of already-documented files (if any)
   to match the repo's comment style, docstring format, and tone. Follow
   `references/style.md` — document the *why*, not the *what*.

4. **Annotate the code.** Add docstrings/comments where they earn their place per
   `references/style.md`: purpose, non-obvious decisions, gotchas, magic numbers,
   public API, complex logic. Remove or fix any stale comments you find. Do not
   change behavior — comments only.

5. **Update the docs.** Update the README (and any relevant doc) with key call-outs:
   new commands/flags with runnable examples, a short "how it works" note, and
   explicit pointers to the files/functions a reader should look at first.

6. **Verify nothing broke.** Because you only added comments, run the test suite
   (and the program, if quick) to confirm the edits didn't accidentally change
   behavior. Report the result.

7. **Report.** Summarize what you documented, which files you touched, the key
   call-outs you added to the README, and the verification result.

## Hard rules

- **Comments only — never change code behavior.** No logic, no signatures, no
  reformatting beyond what a comment requires. If a change needs a code edit,
  stop and say so instead of doing it silently.
- **Document the why, not the what.** No comments that merely restate the code.
- **Match the repo's existing style.** If there's an established convention, follow
  it; if not, establish a light, consistent one.
- **Keep docs accurate.** Every README claim must match the actual code. Never
  document behavior that doesn't exist.
- **Stay in scope.** Don't "improve" unrelated code or docs while you're at it.

## Report format

```markdown
## Documentation: <one-line summary>

**Scope:** <whole repo / file / diff>
**Code annotated:** <files + what you documented>
**README/docs updated:** <key call-outs added>
**Verification:** <test/program run and result, e.g. `pytest` → 1 passed>
**Notes:** <any stale comments fixed, or code changes you recommended but did NOT make>
```
