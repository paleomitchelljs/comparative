# Migration state — read this first

**What is done, what is next, and what is blocked.** The plan is in
[`MIGRATION.md`](MIGRATION.md); file trust is in [`FILE-LEDGER.md`](FILE-LEDGER.md).

**Update this file in the same commit as the work.** Its only value is being
current.

---

## Next action

> **Task 1 — add `region` to occurrence names and resolve the 25 collisions.**
> Nothing else is blocked on anything. Task 2 needs Task 1; the re-mine (Task 4)
> can start on any source at any time and is the long pole.

## Task board

| # | Task | State |
|---|---|---|
| 1 | `region` on occurrence names; kill the 25 ambiguous keys | **not started** |
| 2 | Scaffold generator + lossless round-trip proof | not started |
| 3 | `after:` field for secondary attribution | not started |
| 4 | Re-mine every cited source | **in progress — 2 of 79** |
| 5 | Flip source of truth to `observations/` + `mapping/` | not started |
| 6 | Retire `attribute_species.py` and friends | not started |
| 7 | `phylogeny.json` | not started |

## Re-mine progress

<!-- counts:remine -->
| Status | Sources | Rows they carry |
|---|---:|---:|
| `remined` | 2 | 63 |
| `not-started` | 69 | 1490 |
| `blocked-no-source` | 8 | 458 |
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
| `cunningham-1882` | 243 |
| `gest-anatomy-tables` | 119 |
| `walthall-ashley-ross-2006` | 63 |
| `diogo-etal-2016-si` | 13 |
| `pereyra-etal-2024` | 11 |
| `fritzsch-2023` | 3 |
| `navarro-etal-2023` | 3 |
| `sefton-etal-2016` | 3 |

**8 sources, 458 rows** that cannot be verified against a paper.
<!-- /counts:remine-blocked -->

These carry rows nobody can currently check against a paper. Cunningham, Gest and
Walthall & Ashley-Ross are the large ones. **Do not quietly trust these rows** —
they are the same class of claim the audit found wanting elsewhere, minus the
ability to test them.

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
