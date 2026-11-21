# Discovery checklist

Run this **before** writing any code. The goal is to learn the repo's existing
conventions so the new code blends in rather than standing out. Answer each item
by reading the repo, not by assuming.

## Language & tooling
- What is the primary language? (manifests + file counts — see `detect-language.sh`)
- Which package/build/test tooling does it use? (pip, npm, go, cargo, bundler, maven…)
- What is the module/package layout? (flat, `src/`, single module, multiple packages)
- Is there a linter/formatter configured? (ruff, black, eslint, gofmt, rustfmt, rubocop) — match its style.

## Existing patterns (the most important part)
- How is the code organized? Pick one real file that does something similar to the task and study it:
  - module/package naming and file placement
  - how functions/classes are declared and exported
  - how errors are raised, returned, or handled
  - how logging and config/env vars are read
  - import style and any import-ordering convention
- What is the public API surface? Is there a `main`/entry point, a CLI, an app factory?
- How does the repo expose things (a package, a script, a library)? New code should hang off the same surface.

## Tests
- Where do tests live and what framework/runner? (pytest, jest, go test, cargo test, rspec)
- What's the test naming and assertion style? Copy it.
- Is there a test for the area you're touching? Extend it rather than starting a new pattern.

## Docs & config
- Does the README document usage/setup? Mirror that structure for anything new.
- Are there config files, env vars, or constants files where new settings belong?

## Constraints & boundaries
- What must NOT change? (public API signatures, data formats, committed interfaces)
- What's the minimum that satisfies the instruction without over-building?

Write a 5-10 line **discovery summary** capturing the answers. It becomes the
contract the implementation follows. If the repo is empty or greenfield, say so
explicitly and state the conventions you will establish.
