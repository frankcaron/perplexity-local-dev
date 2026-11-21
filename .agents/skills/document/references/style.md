# What to document, and how

The goal is **human readability for a newcomer**, not exhaustive annotation.
Prefer a few high-value explanations over noise. If you find yourself adding a
comment that just restates the code ("// increment i"), delete it.

## What earns a comment / docstring

Document the **why**, not the **what**. Add a comment or docstring where:

- **A function's purpose or contract isn't obvious from its name.** One-line
  docstring: what it does, key inputs, what it returns, and any side effects.
- **There's a non-obvious decision or trade-off.** "We use X instead of Y because Z."
- **A workaround or gotcha exists.** Reference the issue/PR or the reason, so a
  future reader doesn't "fix" it and break something.
- **Magic numbers / constants have meaning.** Name them and note the source.
- **A public API or entry point** — the thing a user or caller actually touches.
- **Complex logic** — a short paragraph or inline note explaining the algorithm
  or invariant, especially loops and conditionals that encode a rule.

## What does NOT earn a comment

- Obvious statements (`i += 1`, `return x`).
- Narration of the code (`# set the variable`, `# call the function`).
- Stale comments that describe old behavior — **fix or delete** them.

## Style rules (match the repo)

- Use the language's native doc convention: docstrings in Python, KDoc/`/** */`
  in Java, `///` in Go, `//` block comments in Rust, etc.
- Match the existing tone, tense, and punctuation of the repo's comments.
- Keep each comment short; break a long explanation into a few sentences, not a wall.
- If the repo has zero comments, establish a light, consistent convention rather
  than over-annotating.

## README / docs updates

Update the human-facing docs for anything a user or contributor needs to know:

- **New commands / CLI flags** — add to the usage section with a runnable example.
- **New behavior or capability** — one clear sentence, not a paragraph.
- **Setup / dependencies** — keep the "Run it" / install steps accurate and current.
- **Key call-outs** — a short "How it works" or "Architecture" note when the
  structure isn't self-evident (entry point, main modules, data flow).
- **Call out the important parts explicitly** — name the files/functions a reader
  should look at first, and what each is responsible for.

Keep the README skimmable: short sections, concrete examples, and a pointer to
where the interesting code lives. Don't let it drift out of sync with the code.
