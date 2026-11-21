#!/usr/bin/env bash
# Collect a reviewable diff. Read-only: never modifies the index, worktree, or history.
# Usage: collect-diff.sh [--staged | <base-branch> | <commit> | <a>..<b>]
# Env: MAX_DIFF_LINES (default 1500) caps the printed diff.
set -u
MAX_LINES="${MAX_DIFF_LINES:-1500}"
ARG="${1:-}"

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "ERROR: not inside a git repository" >&2; exit 1; }
cd "$(git rev-parse --show-toplevel)" || exit 1

UNTRACKED=""
if [ "$ARG" = "--staged" ]; then
  SCOPE="staged changes"; RANGE=(--cached)
elif [ -n "$ARG" ]; then
  case "$ARG" in
    *..*) SCOPE="range $ARG"; RANGE=("$ARG") ;;
    *)
      if git rev-parse --verify --quiet "$ARG^{commit}" >/dev/null; then
        BASE="$(git merge-base "$ARG" HEAD 2>/dev/null || echo "$ARG")"
        SCOPE="HEAD and working tree vs $ARG (merge base ${BASE:0:9})"; RANGE=("$BASE")
        UNTRACKED="$(git ls-files --others --exclude-standard)"
      else
        echo "ERROR: '$ARG' is not a known branch, commit, or range" >&2; exit 1
      fi ;;
  esac
else
  UNTRACKED="$(git ls-files --others --exclude-standard)"
  if ! git diff --quiet HEAD -- 2>/dev/null || [ -n "$UNTRACKED" ]; then
    SCOPE="uncommitted changes (staged + unstaged + untracked) vs HEAD"; RANGE=(HEAD)
  else
    UNTRACKED=""
    DEFAULT=""
    for b in main master; do
      git rev-parse --verify --quiet "$b" >/dev/null && { DEFAULT="$b"; break; }
    done
    CUR="$(git rev-parse --abbrev-ref HEAD)"
    if [ -n "$DEFAULT" ] && [ "$CUR" != "$DEFAULT" ]; then
      BASE="$(git merge-base "$DEFAULT" HEAD)"
      SCOPE="branch $CUR vs $DEFAULT (merge base ${BASE:0:9})"; RANGE=("$BASE")
    elif git rev-parse --verify --quiet HEAD~1 >/dev/null; then
      SCOPE="last commit $(git log -1 --format='%h %s')"; RANGE=(HEAD~1 HEAD)
    else
      echo "Nothing to review: clean tree and no base to compare against."; exit 0
    fi
  fi
fi

echo "=== SCOPE ==="
echo "$SCOPE"
echo
echo "=== CHANGED FILES (status path) ==="
git diff --name-status "${RANGE[@]}"
[ -n "$UNTRACKED" ] && echo "$UNTRACKED" | sed 's/^/A?\t/'
echo
echo "=== DIFFSTAT ==="
git diff --stat "${RANGE[@]}"
echo
echo "=== DIFF ==="
{
  git diff --no-color -U5 "${RANGE[@]}"
  if [ -n "$UNTRACKED" ]; then
    echo "$UNTRACKED" | while IFS= read -r f; do
      [ -f "$f" ] || continue
      if grep -Iq . "$f" 2>/dev/null; then
        git diff --no-color --no-index -- /dev/null "$f"
      else
        echo "(binary or empty untracked file: $f)"
      fi
    done
  fi
} > "${TMPDIR:-/tmp}/code-review-diff.$$" 2>/dev/null
TOTAL=$(wc -l < "${TMPDIR:-/tmp}/code-review-diff.$$" | tr -d ' ')
head -n "$MAX_LINES" "${TMPDIR:-/tmp}/code-review-diff.$$"
rm -f "${TMPDIR:-/tmp}/code-review-diff.$$"
if [ "$TOTAL" -gt "$MAX_LINES" ]; then
  echo
  echo "=== TRUNCATED: showed $MAX_LINES of $TOTAL diff lines. Review remaining files one at a time with: git diff ${RANGE[*]} -- <path> ==="
fi
