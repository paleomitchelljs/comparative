# File ledger — what you can trust

Every path under `data/` and `scripts/` is classified here. **`validate.py` errors
if a file exists and is not listed, or is listed and does not exist**, so this
cannot drift silently.

Update it in the same commit that changes a file's standing. State is in
[`MIGRATION-STATE.md`](MIGRATION-STATE.md); the plan is in
[`MIGRATION.md`](MIGRATION.md).

| Class | Means |
|---|---|
| **authoritative** | Hand-curated source of truth. Edit directly |
| **derived** | Generated. Never edit; edit its inputs and rebuild |
| **partial** | Usable but known incomplete or mid-migration. Read the caveat before trusting it |
| **defunct** | Superseded. Do not add to it. Kept until its replacement is proven |

---

## `data/`

| Path | Class | Notes |
|---|---|---|
| `species.json` | authoritative | The unit of observation. Survives the migration unchanged; becomes half of every extraction filename |
| `sources.json` | authoritative | Survives unchanged; the other half of every filename |
| `skeleton.json` | authoritative | **This is already the "skeletal feature file" the migration wants.** 274 elements, `partOf` containment, per-taxon presence, landmarks validated inside their element. One subtlety to preserve: `fusedFrom` is deliberately *not* containment, which is why an avian cnemial crest is reached through `tibia` and not `tibiotarsus` |
| `nerves.json` | authoritative | Homology groups, like elements. Unchanged |
| `joints.json` | authoritative | Unchanged. `jointgraph.py` derives which joints a muscle spans |
| `taxa.json` | derived | Clade rollups computed from species. Also carries topology, so it is the seed for `phylogeny.json` |
| `muscles-*.json` | **derived** | **Generated** from `observations/` + `mapping/` by `build_observations.py --join`, which `build.sh` runs first. **Stays committed** — the app fetches it directly and there is no build step between the repo and the page. Also still **known incomplete**: the audit found drops in 4 of 4 sources examined, so treat any source's rows as partial until `remine-status.json` says `remined` |
| `remine-status.json` | authoritative | Per-source re-mine status. Drives the tables in `MIGRATION-STATE.md` |
| `raw/` | ignored | Verbatim extractions. Git-ignored for copyright. Never commit or quote into `data/` |

| `observations/` | **authoritative** | **The source of truth as of Task 5.** 248 files, one per (species × study). A row's `record` names the homology group it was assigned to; `null` means unassigned and `blockedBy` says why |
| `mapping/` | **authoritative** | 78 files, one per source: `name\|region` → muscle record. Per source deliberately, so two authors can disagree |

### Not yet created

| Path | Class | Task |
|---|---|---|
| `phylogeny.json` | authoritative *(will be)* | 7 |

## `scripts/`

**Six normalisers left `build.sh` when `data/observations/` became the source of
truth.** They edited `data/muscles-*.json`, which step 0 now *generates*, so
nothing they did could reach the source of truth — the next build's join simply
overwrote it. Four had nothing left to do and are deleted; three are kept out of
the build until they are ported. See the table below.

### Live — run by `build.sh`, in order

| Path | Class | Notes |
|---|---|---|
| `build.sh` | authoritative | The entry point. Normalises, derives, validates; exits non-zero on any of them |
| `validate.py` | authoritative | Survives the migration and grows with it. Also enforces this ledger |
| `doc_counts.py` | authoritative | Owns every measured figure in `docs/`. Rejects a hand-written percentage anywhere else under `docs/` |
| `symmetrise_links.py` | authoritative | Closes `related` and `serial`. Operates on the mapping layer after Task 5 |
| `seed_homology_authority.py` | authoritative | Writes `homology.authority`. Moves to the mapping layer |

### Live — utilities, not in `build.sh`

| Path | Class | Notes |
|---|---|---|
| `speciesmap.py` | authoritative | Species → clade. Imported by six scripts |
| `jointgraph.py` | authoritative | Joints a muscle spans, from its attachments. Shared with `validate.py` |
| `export_matrix.py` | authoritative | Tidy CSVs to `export/`, which is git-ignored and derived |
| `promote_landmarks.py` | **needs porting** | Promotes landmarks named in prose into structured rows. Reads and writes `muscles-*.json`, which is generated, so its output cannot reach the source of truth. **It has 79 pending refinements** — `ribs → true-ribs`, `mandible → retroarticular-process`. Port it to `data/observations/` and run it |
| `seed_nerves.py` · `seed_actions.py` | **needs porting** | Same problem, less urgent: both report 0 rows to apply today, but they will have work as soon as new mining lands, and 86 nerve strings and 23 action clauses are still unclaimed |
| `build_observations.py` | authoritative | The migration's engine. `--split` writes `data/observations/` and `data/mapping/`; `--join` rebuilds `muscles-*.json`; `--check` proves the round trip is lossless. **The round trip is byte-identical**, so the new shape holds everything the old one holds |

### One-shots that have already run

| Path | Class | Notes |
|---|---|---|
| — | — | All deleted on 2026-08-20. `fix_skeleton_homology.py` merged hyomandibula/stapes; `seed_klinkhamer_crocodylus.py` was a single-source seed of the kind `CLAUDE.md` forbids; `migrate_attachments`, `migrate_attachment_rows`, `migrate_fusions` and `assign_hierarchy` were normalisers with nothing left to normalise, and edited a file that is now generated. `attribute_species.py` went with them — the filename declares the species now. git holds all seven |
| `extract_werneburg_appendix.py` | authoritative | Regenerates a git-ignored working file from a local PDF. Keep — it is an extractor, not a seeder |

## `docs/` and `papers/`

| Path | Class | Notes |
|---|---|---|
| `SCHEMA.md` | authoritative | The only definition of any field |
| `METHODS.md` | authoritative | The only statement of any interpretive rule. No numbers |
| `MINING.md` | authoritative | How to mine. **Read before every mining pass** — it carries the extract-everything rule and the multilingual density triage |
| `MIGRATION.md` · `MIGRATION-STATE.md` · `FILE-LEDGER.md` | authoritative | This migration |
| `WORKLIST.md` | authoritative | What to do next in the *data*, and the open decisions |
| `ROADMAP.md` | authoritative | Where the interface is going |
| `homology-system-guide.md` | authoritative | What the four correspondence relations mean |
| `STATUS.md` | derived | Entirely generated |
| `papers/*.md` | authoritative | What one source says and what one pass found. **Where history lives** — a re-mine writes its accounting here |
| `papers/extracted/` | ignored | Git-ignored. Regenerate with `pdftotext` |
