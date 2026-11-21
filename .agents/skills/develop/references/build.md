# Build & verify checklist

Apply during and after implementation. The bar is: it works, it's tested, it
matches the repo, and it's documented.

## Implement
- Write the smallest thing that fully satisfies the instruction — no speculative
  features, no "while I'm here" refactors of unrelated code.
- Follow the conventions discovered (naming, error handling, module layout, imports).
- Keep public API changes backward-compatible unless the instruction requires otherwise.
- Add a docstring/comment where behavior isn't obvious from the name.

## Test
- Add a test for every new behavior and for each edge case the instruction implies.
- **Every new public function/method gets at least one test** — no exceptions.
- **No test may assert only that no exception is thrown.** Each test must assert a
  concrete, expected value or state. A bare `f()` call or `assert not raised` is
  not a test; it is a smoke check and does not count toward coverage.
- Match the repo's existing test framework, naming, and assertion style.
- Cover at least: the happy path, one error/edge path, and (if it's a bug fix) a regression test.
- Run the suite. **Do not stop at "it compiles"** — run the actual tests and the program.

## Verify end-to-end
- Run the real entry point / command the way a user would, and confirm the expected output.
- If the repo has a linter/formatter, run it and fix what it flags in your changed files.
- Re-run after every edit until green.

## Document
- Update the README (or the relevant doc) for any new command, flag, or behavior.
- Keep inline docs consistent with the final code.

## Self-review before reporting
- Re-read the diff with fresh eyes: does it do exactly what was asked, nothing more?
- Would this pass the repo's `code-review` skill? (correctness, error handling, security, tests)
- If the diff is large, run the `code-review` skill on it and address Blocker/Major findings.
