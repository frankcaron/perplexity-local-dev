#!/usr/bin/env bash
# Surface the code that most needs documentation, so the document skill focuses
# on high-value targets instead of commenting every line. Read-only.
# Usage: doc-targets.sh [max-files]   (default 15)
set -u
MAX="${1:-15}"

cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" || exit 1

# Primary source extensions to consider (language-agnostic set).
find_src() {
  find . -type f \
    \( -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.go' \
       -o -name '*.rs' -o -name '*.rb' -o -name '*.java' \) \
    -not -path './.venv/*' -not -path './node_modules/*' -not -path './.git/*' \
    -not -path './vendor/*' -not -path './dist/*' 2>/dev/null
}

echo "=== SOURCE FILES BY SIZE (largest first, top $MAX) ==="
find_src | xargs wc -l 2>/dev/null | sort -rn | head -n "$MAX"
echo

echo "=== FUNCTIONS / CLASSES DEFINED (top-level definitions per file) ==="
find_src \
  | while read -r f; do
      n=$(grep -cE '^\s*(def |class |func |fn |func\w+ |public |private |export )' "$f" 2>/dev/null || echo 0)
      [ "$n" -gt 0 ] && printf '%s\tdefs=%s\n' "$f" "$n"
    done | sort -t$'\t' -k2 -rn | head -n "$MAX"
echo

echo "=== PUBLIC ENTRY POINTS ==="
for f in main.py main.go main.rs index.js index.ts src/main.py src/main.go app.py; do
  [ -e "$f" ] && echo "found: $f"
done
echo

echo "=== EXISTING DOC COVERAGE (rough) ==="
echo "files with any docstring/comment lines:"
find_src \
  | while read -r f; do
      d=$(grep -cE '^\s*("""|/\*\*|#|//)' "$f" 2>/dev/null)
      [ -n "$d" ] && printf '%s\tdoc-lines=%s\n' "$f" "$d"
    done | head -n "$MAX"
