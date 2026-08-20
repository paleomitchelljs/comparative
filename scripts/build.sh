#!/usr/bin/env bash
# Reproducible data build.
#
# Every step is idempotent and non-destructive: a step fills a field the data
# does not have, derives one it can compute, or normalises one into its
# structured form. None of them overwrites curated content, and the whole run is
# a fixed point — CI runs it and fails if the committed data moves.
#
# Six normaliser steps were removed when data/observations/ became the source of
# truth. They edited data/muscles-*.json, which step 0 now GENERATES, so nothing
# they did could reach the source of truth -- the next build's join simply
# overwrote it. Four of them (migrate_attachments, migrate_attachment_rows,
# migrate_fusions, assign_hierarchy) had nothing left to do anyway and are
# deleted. seed_nerves, seed_actions and promote_landmarks still have work in
# them and are kept out of the build until they are ported to read and write
# data/observations/ -- promote_landmarks alone has 79 pending landmark
# refinements. See docs/MIGRATION-STATE.md.
#
# The seven single-source seed scripts that preceded them are also gone. They
# held a paper's rows as Python literals, and once the rows were committed the
# literal was a stale second copy the build replayed over later curation. What
# each argued lives in the reading note for its source.
#
#   ./scripts/build.sh          # report only
#   ./scripts/build.sh --write  # apply, then validate
set -euo pipefail
cd "$(dirname "$0")/.."

FLAG="${1:-}"

step() { printf '\n\033[1m== %s\033[0m\n' "$1"; }

# data/observations/ is the source of truth as of Task 5: one file per study per
# animal, with `record` naming the homology group each row was assigned to. The
# muscle files are rebuilt from it before anything else runs, and stay committed
# because the app fetches them directly and there is no build step between the
# repo and the page.
step "0. observations/ + mapping/ -> muscles-*.json"
python3 scripts/build_observations.py --join

step "1. whose homology scheme each record follows (most recent wins)"
python3 scripts/seed_homology_authority.py $FLAG

step "2. close the related-muscle graph"
python3 scripts/symmetrise_links.py $FLAG

# Before the counts, not after them: it was running unlabelled inside the
# validate step, so a build that changed an attribution reported figures from
# the state before the change, and a report-only run never exercised it at all.
# Step 9 was attribute_species.py -- 300 lines inferring which animal a row is
# about. The filename declares it now. Retired at Task 6; see docs/FILE-LEDGER.md.

step "3. measured counts in README.md and docs/STATUS.md"
python3 scripts/doc_counts.py $FLAG

if [ "$FLAG" = "--write" ]; then
  step "4. validate"
  python3 scripts/validate.py
fi
