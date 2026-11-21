# Review checklist

Apply each section to the changed lines and the code they touch. Skip sections that do not apply.

## Correctness
- Off-by-one, wrong comparison, inverted condition, wrong default value.
- `None`/`null`/empty input, empty list, zero, negative numbers, very large input.
- Changed function signature or return type: are all callers updated?
- Mutable default arguments (Python `def f(x=[])`), shared state, accidental aliasing.
- Async code: missing `await`, unhandled promise, race on shared state.
- Resource leaks: files, sockets, DB connections not closed (prefer `with` / `try/finally`).

## Error handling
- Bare `except:` or `except Exception: pass` that hides failures.
- Errors swallowed without logging, or logged without context.
- External calls (network, disk, subprocess) with no timeout or failure path.

## Security
- Hardcoded secrets, tokens, passwords, or private URLs. Treat any as a Blocker.
- SQL, shell, or template strings built from user input (injection). Look for f-strings or `+` into `execute`, `subprocess(..., shell=True)`, `eval`, `exec`.
- Path traversal: user input joined into file paths without validation.
- Unsafe deserialization: `pickle.loads`, `yaml.load` without `SafeLoader`.
- Sensitive data (PII, account numbers, credentials) written to logs or error messages.
- New dependencies: pinned? Necessary? From a known source?

## Tests
- New logic without a test, or a bug fix without a regression test.
- Tests that only assert "no exception" or mirror the implementation.
- Tests that depend on time, network, randomness, or execution order without control.

## Maintainability
- Names that do not say what the thing is or does.
- Functions doing several unrelated things; deep nesting that an early return would flatten.
- Copy-pasted blocks that should share a helper.
- Dead code, commented-out code, leftover debug prints.
- Comments or docstrings that no longer match the code.
- Changes that contradict the repo's existing patterns (formatting, structure, error style).

## Docs and config
- README or usage docs not updated for changed behavior, commands, or setup.
- Config or environment variables added without a default or documentation.
