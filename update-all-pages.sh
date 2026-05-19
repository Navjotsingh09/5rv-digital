#!/usr/bin/env bash
# update-all-pages.sh
# Run all active patch scripts in the correct order after a Webflow re-export.
# Must be run from inside the 5rv-revamp.webflow/ directory.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

cd "$(dirname "$0")"

echo "═══════════════════════════════════════════════════════"
echo "  5RV Digital — Post-Export Update Pipeline"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════════════"

# ── Pre-flight checks ────────────────────────────────────────────────────────
echo ""
echo "[ PRE-FLIGHT ]"

if ! git -C . rev-parse --is-inside-work-tree &>/dev/null; then
  echo "ERROR: Not inside a git repository. Aborting."
  exit 1
fi

DIRTY=$(git status --porcelain)
if [ -n "$DIRTY" ]; then
  echo "WARNING: Uncommitted changes detected:"
  git status --short
  read -rp "Continue anyway? (y/N): " yn
  [[ "$yn" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 1; }
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "  Branch : $BRANCH"
echo "  Commit : $(git rev-parse --short HEAD)"

# ── Step 1: Rebuild rv-components.css ────────────────────────────────────────
echo ""
echo "[ STEP 1 ] Rebuild rv-components.css"
python3 _build_rv_components.py
echo "  ✓ Done"

# ── Step 2: Patch all pages (inject CSS link, remove inline blocks) ──────────
echo ""
echo "[ STEP 2 ] Patch pages — inject CSS link"
python3 _patch_pages.py
echo "  ✓ Done"

# ── Step 3: ARIA fixes ───────────────────────────────────────────────────────
echo ""
echo "[ STEP 3 ] ARIA / accessibility patches"
python3 _patch_aria.py
echo "  ✓ Done"

# ── Step 4: Fix invalid height="Auto" attributes ─────────────────────────────
echo ""
echo "[ STEP 4 ] Fix height=Auto attributes"
python3 fix_height_auto.py
echo "  ✓ Done"

# ── Verification ─────────────────────────────────────────────────────────────
echo ""
echo "[ VERIFY ]"
TOTAL=$(find . -maxdepth 1 -name "*.html" | wc -l | tr -d ' ')
PATCHED=$(grep -l 'rv-components.css' *.html 2>/dev/null | wc -l | tr -d ' ')
echo "  Pages total    : $TOTAL"
echo "  Pages patched  : $PATCHED"
if [ "$TOTAL" -ne "$PATCHED" ]; then
  echo "  WARNING: $((TOTAL - PATCHED)) page(s) missing rv-components.css link:"
  grep -rL 'rv-components.css' *.html | sed 's/^/    /'
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Pipeline complete. Review changes then commit:"
echo "    git add -A"
echo "    git commit -m \"chore: post-export patch \$(date +%Y-%m-%d)\""
echo "    git push origin $BRANCH"
echo "═══════════════════════════════════════════════════════"
