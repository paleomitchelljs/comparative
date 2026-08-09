#!/usr/bin/env bash
# Reproducible data build.
#
# The migration and seeding scripts are idempotent, so this can be re-run at any
# time. Order matters: attachments must be resolved to skeleton ids before they
# can be structured into rows, and occurrence-level seeds must land before the
# row migration so they get structured too.
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

step "3. skeletal elements for the Taricha attachment sites"
python3 scripts/seed_walthall_skeleton.py $FLAG

step "4. Walthall & Ashley-Ross Caudata records and occurrences"
# Must precede the occurrence-attachment seed: it creates the pes records that
# seed's relocated anuran and crocodylian pedal rows land on.
python3 scripts/seed_walthall_taricha.py $FLAG

step "5. taxon-specific attachments for documented shifts"
python3 scripts/seed_occurrence_attachments.py $FLAG

step "6. attachments -> element / side / landmark rows"
python3 scripts/migrate_attachment_rows.py $FLAG

step "7. fused elements: fusedFrom, not partOf"
python3 scripts/migrate_fusions.py $FLAG

step "8. taxon-specific division into parts"
python3 scripts/seed_division.py $FLAG

step "9. innervation prose -> nerves.json ids"
python3 scripts/seed_nerves.py $FLAG

step "10. close the related-muscle graph"
python3 scripts/symmetrise_links.py $FLAG

if [ "$FLAG" = "--write" ]; then
  step "11. validate"
  python3 scripts/validate.py
fi
