# Migration state — read this first

**What is done, what is next, and what is blocked.** The plan is in
[`MIGRATION.md`](MIGRATION.md); file trust is in [`FILE-LEDGER.md`](FILE-LEDGER.md).

**Update this file in the same commit as the work.** Its only value is being
current.

---

## Next action

> **Task 3 — add the `after:` field for secondary attribution.** It is what
> unblocks the largest drop the audit found (Russell & Bauer's 22 genera, most of
> Burch's per-taxon prose). Tasks 1 and 2 are done and the round trip is proven
> byte-identical, so the model is no longer a hypothesis. The re-mine (Task 4) can
> start on any source at any time and is the long pole.

## Task board

| # | Task | State |
|---|---|---|
| 1 | `region` on occurrence names; kill the 25 ambiguous keys | **done** |
| 2 | Scaffold generator + lossless round-trip proof | **done** |
| 3 | `after:` field for secondary attribution | not started |
| 4 | Re-mine every cited source | **in progress — 2 of 79** |
| 5 | Flip source of truth to `observations/` + `mapping/` | not started |
| 6 | Retire `attribute_species.py` and friends | not started |
| 7 | `phylogeny.json` | not started |

## The model is proven

`scripts/build_observations.py --check` splits the 164 records into **220
observation files and 78 mapping files (2011 rows)**, rebuilds `muscles-*.json`
from them, and diffs. The round trip is **byte-identical** — `git diff` is empty
after a full split and join, and `build.sh` is still a fixed point.

That settles the only question the design could not answer on paper: the new shape
holds everything the old one holds. It settles nothing about completeness, which
is Task 4.

Three things had to be carried through the split for the round trip to close, and
they are worth knowing before anyone edits the generator: the occurrence's
**position** in its record (an occurrence with two sources becomes two rows and has
to merge back in the right place), its original **key order**, and its original
**source order** (the join reads files alphabetically, so a two-source occurrence
otherwise comes back with its citations swapped).

`data/observations/` and `data/mapping/` are git-ignored until Task 5. While
`muscles-*.json` is the source of truth, committing them would be committing a
second copy.

## Re-mine progress

<!-- counts:remine -->
| Status | Sources | Rows they carry |
|---|---:|---:|
| `remined` | 2 | 63 |
| `not-started` | 73 | 1868 |
| `blocked-no-source` | 4 | 80 |
| **total** | **79** | **2011** |

**2 of 79 cited sources re-mined** (2%).
<!-- /counts:remine -->

### What counts as done

A source is `remined` only when **every muscle it describes is either filed or
parked**, and the note states the arithmetic. Two sources have cleared that bar:

- **Fisher & Goodman (1955)** — 111 muscles with an origin paragraph: 43 filed,
  50 parked, the rest inside multi-muscle rows. Moved the Aves column further than
  any single pass so far; the figures are in `STATUS.md`.
- **Widrig et al. (2026)** — 38 blocks: 20 filed, 16 parked, 2 folded into
  existing rows.

### Sources that cannot be re-mined

<!-- counts:remine-blocked -->
| Source | Rows |
|---|---:|
| `walthall-ashley-ross-2006` | 63 |
| `pereyra-etal-2024` | 11 |
| `fritzsch-2023` | 3 |
| `navarro-etal-2023` | 3 |

**4 sources, 80 rows** that cannot be verified against a paper.
<!-- /counts:remine-blocked -->

These carry rows nobody can currently check against a paper. **Do not quietly
trust them** — they are the same class of claim the audit found wanting elsewhere,
minus the ability to test them.

**Four of the original eight were acquired on 2026-08-19** and are now
`not-started` rather than blocked: Cunningham (the whole Challenger part XVI, from
archive.org), Sefton et al. (eLife, gold OA), the Diogo et al. supplementary (gold
OA, and it is a `.docx`), and the Gest tables (eight region pages mirrored to
`papers/gest-anatomy-tables/`). That moved 419 of the 458 unverifiable rows back
into reach.

The four that remain are not paywalled in the ordinary sense, and none should be
worked around:

| Source | Why | How to get it |
|---|---|---|
| `walthall-ashley-ross-2006` | Bronze OA — free to read on Wiley, no open licence. Wiley serves a bot-check page to scripts | Browser |
| `pereyra-etal-2024` | In PMC but **not** in the PMC open-access subset, so there is no programmatic route | Browser |
| `fritzsch-2023` | Open on Preprints.org; the download endpoint blocks scripted requests | Browser |
| `navarro-etal-2023` | **Genuinely closed access** | Subscription or author copy |

Drop them in `papers/` under the filename the reading note already implies, add the
`pdf` field to `sources.json`, and set the status to `not-started`.

## Known-incomplete sources with a local copy

The audit of 2026-08-19 examined four and found drops in all four. Their reading
notes carry the detail; each is `not-started` until re-mined.

| Source | Held | Also contains |
|---|---|---|
| Russell & Bauer (2008) | 71 rows, 70 on *Iguana* | 558 statements across 22 lepidosaur genera. Mostly **secondary** — needs Task 3 |
| Walker (1973) | 22 rows, all *Trachemys* | 90 statements across 9 other turtle genera, **first-hand**. Best target |
| Osawa (1898) | 63 rows, all limb | The whole cranial and axial myology |
| Burch (2014) | 38 rows, all *Tawa* | A bracket table of 35 extant taxa, 7 already species here |

## Decisions taken, so they are not relitigated

- **Extraction is keyed on (species × study), not on homology group.** 2026-08-19.
- **Everything must be re-mined**, not migrated forward. The audit found drops in
  4 of 4 sources, so current rows are a partial extraction throughout.
- **The mapping is per source.** A global name table would destroy the
  disagreements the dataset exists to hold.
- **The key is (name, region), not name.** 25 collisions proved it.
- **Serial correspondence sources do not set `homology.authority`.** 2026-08-19.
- **Element correspondences exist** for "may be one element, undemonstrated".

## Open questions

- Ergonomics of 220 files at a median of 4 muscles, 58 of them singletons. Live
  with it, or group small studies?
- Cross-taxon review — seeing every animal's latissimus at once — becomes generated
  rather than authored. That is the one thing the current model does better, and
  the generated view has to be good enough to review from.
