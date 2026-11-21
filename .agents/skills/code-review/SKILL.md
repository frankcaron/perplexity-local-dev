---
name: code-review
description: "Review local git changes for bugs, security flaws, missing tests, and maintainability issues, reporting findings by severity with file and line references. Use when asked to review a diff, branch, commit, staged changes, or PR locally. Not for writing new features or fixing the code."
compatibility: "Requires git and bash on macOS or Linux. Designed for Perplexity Local models running offline in this repository."
metadata:
  version: "1.0"
  author: frank-caron
---

# Code Review

You are reviewing code, not changing it. Stay read-only.

## Hard rules

- Never run `git commit`, `git add`, `git push`, `git reset`, `git checkout`, `git stash`, or any command that edits files or history.
- Never edit source files. Put suggested fixes in the report as code blocks.
- Run tests or linters only if the user asks, or if a command is listed in the repo's README, `pyproject.toml`, `package.json`, or `Makefile`. Report their output; do not fix failures.
- Every finding must cite a real file and line you read. If you are unsure, say so and mark the confidence as low. Do not invent APIs, files, or behavior.

## Steps

1. **Pick the scope.** Use what the user named: a base branch, a commit range, `--staged`, or a file list. If nothing is named, review uncommitted changes; if there are none, review the current branch against its merge base with `main` or `master`.
2. **Collect the diff.** Run `bash .agents/skills/code-review/scripts/collect-diff.sh [scope]` from the repo root. Scope examples: no argument (auto), `--staged`, `main`, `HEAD~3`, `abc123..def456`. The script prints the scope it chose, the changed files, a diffstat, and the diff, including new untracked files.
3. **Read context.** For each changed file, read the surrounding code that the diff touches: the full changed function, its callers if the signature changed, and the matching test file if one exists. Skip lockfiles, generated files, and vendored code unless they are the point of the change.
4. **Check the change.** Walk through `references/checklist.md` for each file. Focus on what the diff introduces or breaks, not on pre-existing code.
5. **Write the report** in the format below. The review is complete when every changed, non-generated file appears in the report either with findings or under "Reviewed, no issues".

## Severity

- **Blocker**: will break behavior, lose data, expose secrets, or open a security hole. Must fix before merge.
- **Major**: likely bug, missing error handling on a real path, or missing test for new logic.
- **Minor**: readability, naming, small duplication, or style that the repo's own conventions contradict.
- **Nit**: optional polish. Keep these few.

## Report format

```markdown
## Code review: <scope>

**Verdict:** Approve | Approve with changes | Request changes
**Summary:** <2-3 sentences on what the change does and the main risk>

### Findings
1. **[Blocker] path/to/file.py:42** — <what is wrong and why it matters>
   Confidence: high | moderate | low
   Suggested fix:
   ```python
   <minimal replacement>
   ```

### Tests
<what is covered, what is missing, test commands run and their result>

### Reviewed, no issues
- path/to/other_file.py
```

Order findings by severity, then by file. If there are no findings, say so plainly and still list the reviewed files.

## When the diff is large

If the script reports the diff was truncated, review file by file: run `git diff <base> -- <path>` for each file in the changed-files list, and write findings as you go before moving to the next file.
