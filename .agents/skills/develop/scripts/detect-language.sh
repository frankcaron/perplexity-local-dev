#!/usr/bin/env bash
# Detect the repository's primary language and tooling so the develop skill can
# build in the right idiom. Read-only: only inspects, never modifies anything.
# Usage: detect-language.sh   (run from anywhere inside the repo)
set -u

cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" || exit 1

echo "=== REPO ROOT ==="
pwd
echo

echo "=== MANIFESTS ==="
for f in pyproject.toml setup.py setup.cfg package.json go.mod Cargo.toml Gemfile composer.json pom.xml build.gradle build.sbt Makefile; do
  [ -e "$f" ] && echo "found: $f"
done
echo

echo "=== FILE EXTENSION COUNTS (top 12, excluding vendored) ==="
find . -type f \
  -not -path './.git/*' -not -path './.venv/*' -not -path './node_modules/*' \
  -not -path './vendor/*' -not -path './dist/*' -not -path './build/*' \
  -not -name '*.lock' 2>/dev/null \
  | sed -E 's/.*\.([A-Za-z0-9]+)$/\1/' \
  | grep -E '^[A-Za-z0-9]+$' \
  | sort | uniq -c | sort -rn | head -12
echo

echo "=== TOP-LEVEL LAYOUT ==="
ls -1 | grep -v '^\.' | head -30
echo

echo "=== TEST DISCOVERY ==="
for d in tests test src/tests spec; do [ -d "$d" ] && echo "dir: $d"; done
find . -maxdepth 2 -type f \( -name 'test_*.py' -o -name '*_test.go' -o -name '*.test.js' -o -name '*.test.ts' -o -name '*_test.rb' -o -name '*Test.java' \) \
  -not -path './.venv/*' -not -path './node_modules/*' 2>/dev/null | head -15
echo

echo "=== INFERRED PRIMARY LANGUAGE ==="
count_py=0; count_js=0; count_go=0; count_rs=0; count_rb=0
count_py=$(find . -name '*.py' -not -path './.venv/*' -not -path './.git/*' 2>/dev/null | wc -l | tr -d ' ')
count_js=$(( $(find . \( -name '*.js' -o -name '*.ts' \) -not -path './node_modules/*' -not -path './.git/*' 2>/dev/null | wc -l | tr -d ' ') ))
count_go=$(find . -name '*.go' -not -path './.git/*' 2>/dev/null | wc -l | tr -d ' ')
count_rs=$(find . -name '*.rs' -not -path './.git/*' 2>/dev/null | wc -l | tr -d ' ')
count_rb=$(find . -name '*.rb' -not -path './.git/*' 2>/dev/null | wc -l | tr -d ' ')
echo "py=$count_py js/ts=$count_js go=$count_go rs=$count_rb rb=$count_rb"
echo "(infer the dominant one from the counts and the manifests above; a manifest like pyproject.toml or package.json usually wins over raw file counts)"
