#!/usr/bin/env bash
# Reproducible data build.
#
# Every step is idempotent and non-destructive: a step fills a field the data
# does not have, derives one it can compute, or normalises one into its
# structured form. None of them overwrites curated content, and the whole run is
# a fixed point — CI runs it and fails if the committed data moves.
#
# The seven single-source seed scripts that used to run between steps 2 and 3
# are gone. They held a paper's rows as Python literals, and once the rows were
# committed the literal was a stale second copy that the build replayed over
# later curation. What each one argued is now in the reading note for its
# source, which is where a statement about a paper belongs; `data/` holds the
# rows; git holds the history. See docs/SCHEMA.md for how to add rows by hand.
#
#   ./scripts/build.sh          # report only
#   ./scripts/build.sh --write  # apply, then validate
set -euo pipefail
cd "$(dirname "$0")/.."

FLAG="${1:-}"

step() { printf '\n\033[1m== %s\033[0m\n' "$1"; }

step "1. free-string attachments -> skeleton.json ids"
python3 scripts/migrate_attachments.py $FLAG

step "2. segment + layer (layer inherited via derivatives where sourced)"
python3 scripts/assign_hierarchy.py $FLAG

step "3. attachments -> element / side / landmark rows"
python3 scripts/migrate_attachment_rows.py $FLAG

step "4. fused elements: fusedFrom, not partOf"
python3 scripts/migrate_fusions.py $FLAG

step "5. innervation prose -> nerves.json ids"
python3 scripts/seed_nerves.py $FLAG

step "6. action prose -> joints.json {joint, motion}"
python3 scripts/seed_actions.py $FLAG

step "7. whose homology scheme each record follows (most recent wins)"
python3 scripts/seed_homology_authority.py $FLAG

step "8. close the related-muscle graph"
python3 scripts/symmetrise_links.py $FLAG

# Before the counts, not after them: it was running unlabelled inside the
# validate step, so a build that changed an attribution reported figures from
# the state before the change, and a report-only run never exercised it at all.
step "9. species attribution from each row's own prose"
python3 scripts/attribute_species.py $FLAG

step "10. measured counts in README.md and docs/STATUS.md"
python3 scripts/doc_counts.py $FLAG

if [ "$FLAG" = "--write" ]; then
  step "11. validate"
  python3 scripts/validate.py
fi
