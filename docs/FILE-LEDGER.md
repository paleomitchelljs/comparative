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

### Live — run by `build.sh`, in order

| Path | Class | Notes |
|---|---|---|
| `build.sh` | authoritative | The entry point. Normalises, derives, validates; exits non-zero on any of them |
| `validate.py` | authoritative | Survives the migration and grows with it. Also enforces this ledger |
| `doc_counts.py` | authoritative | Owns every measured figure in `docs/`. Rejects a hand-written percentage anywhere else under `docs/` |
| `symmetrise_links.py` | authoritative | Closes `related` and `serial`. Operates on the mapping layer after Task 5 |
| `seed_homology_authority.py` | authoritative | Writes `homology.authority`. Moves to the mapping layer |
| `assign_hierarchy.py` | authoritative | Normaliser |
| `seed_actions.py` · `seed_nerves.py` | authoritative | Normalisers; fill rather than sync |
| `migrate_attachments.py` · `migrate_attachment_rows.py` · `migrate_fusions.py` | authoritative | Badly named — these are **idempotent normalisers**, not one-shot migrations. They stay |
| `attribute_species.py` | **defunct** | 300 lines inferring which animal a row is about. The filename declares it now, so it is out of `build.sh` as of Task 5. Kept unrun until the `speciesBasis` evidence it computed has a home in the new files. **Do not invest in it** |

### Live — utilities, not in `build.sh`

| Path | Class | Notes |
|---|---|---|
| `speciesmap.py` | authoritative | Species → clade. Imported by six scripts |
| `jointgraph.py` | authoritative | Joints a muscle spans, from its attachments. Shared with `validate.py` |
| `export_matrix.py` | authoritative | Tidy CSVs to `export/`, which is git-ignored and derived |
| `promote_landmarks.py` | authoritative | Promotes landmarks named in prose into structured rows. Re-run after any mining pass |
| `build_observations.py` | authoritative | The migration's engine. `--split` writes `data/observations/` and `data/mapping/`; `--join` rebuilds `muscles-*.json`; `--check` proves the round trip is lossless. **The round trip is byte-identical**, so the new shape holds everything the old one holds |

### One-shots that have already run

| Path | Class | Notes |
|---|---|---|
| `fix_skeleton_homology.py` | **defunct** | Merged hyomandibula/stapes and restructured the axial series. Done; kept for the record of what it argued |
| `seed_klinkhamer_crocodylus.py` | **defunct** | A single-source seed script of the kind `CLAUDE.md` says never to write again — its rows are committed, so the literal inside it is a stale second copy. **Delete at Task 6** |
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
