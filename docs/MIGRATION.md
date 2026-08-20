# The migration: extraction-first storage

**Read [`MIGRATION-STATE.md`](MIGRATION-STATE.md) first.** It says what is done and
what to do next. This file says *what the plan is* and changes rarely.

For which files you can trust while this is in progress, see
[`FILE-LEDGER.md`](FILE-LEDGER.md).

---

## Why

A muscle record is a homology group, and an occurrence lives inside one. So the
paper is not a unit the data knows about, and three questions cannot be asked:

1. **Is this source fully mined?** Answering it means scanning 164 records for
   occurrences citing that source. The audit of 2026-08-19 had to do exactly that,
   which is why 70 *Iguana* rows sitting beside 22 dropped genera went unnoticed.
2. **Whose observation is this?** Russell & Bauer reporting Miner (1925) has no
   slot. That blocks roughly 650 statements across two sources.
3. **Do two authors assign this muscle to different groups?** Collapses to one
   assignment plus prose. That is the tensor tympani, and it had to be decided
   rather than recorded.

All three have one cause: the observation is stored inside the interpretation.

## The target

```
data/observations/<species>__<source>.json    PRIMARY. One file per species per study.
data/mapping/<source>.json                    (name, region) -> muscle record, attributed
data/muscles-*.json                           GENERATED from the two above
data/skeleton.json  species.json  sources.json  nerves.json  joints.json
                                              Authoritative, unchanged
data/taxa.json                                Derived (already)
data/phylogeny.json                           Later. Nothing blocks on it
```

**The extraction file is what a person reading a paper writes.** Every muscle the
study describes for that animal, with the study's own name for it, its region, its
attachments as structured rows, innervation, architecture, and prose. Nothing about
homology.

**The mapping file is the interpretation.** It says which record each of that
study's names belongs to, and it is **per source**, because two authors disagreeing
is the thing this dataset exists to preserve. A single global name table would
destroy it.

## Three facts the data forced, before you design anything

**Name is not a key.** 25 of 1840 (species, source, name) triples map to two
records, and they are all one pattern: the same author uses one name for a forelimb
and a hindlimb muscle in the same animal — Osawa's "M. extensor digitorum communis
longus", Russell & Bauer's "M. pronator profundus", Fisher & Goodman's "flexor
digitorum longus". **The key is (name, region).**

**The mapping file is not a synonymy list.** The group-level content is the
substantive half of this dataset: `consensus` on 164 records, `developmental` 164,
`mass` 164, `homology` 164 (correspondences, authority, teaching, related),
`synonyms` 101, `layer` 73, `arch` 49. None of it is derivable from observations.

**Everything must be re-mined.** The audit found drops in four of four sources
examined, so the current rows are a partial extraction throughout. Generating
extraction files from them would carry that incompleteness forward *and make it
look complete*. The generated files are a **scaffold and a checklist**, never a
result.

## Tasks

Each has a definition of done. Do them in order; 1 and 2 are independent of the
re-mine and unblock it.

### 1. Add `region` to occurrence names, resolving the 25 collisions

Needed either way — it is the one genuine gap in the current data. Without it the
mapping key is ambiguous.

**Done when** `validate.py` errors on any (species, source, name) that resolves to
two records, and the count is zero.

### 2. Build the scaffold generator and prove the schema is lossless

`scripts/build_observations.py`: read `data/muscles-*.json`, emit
`data/observations/` and `data/mapping/`. Then the reverse: rebuild
`muscles-*.json` from them and diff.

**Done when** the round trip is byte-identical after `build.sh --write`. That
proves the new shape can hold everything the old one holds. It proves **nothing**
about completeness — every generated file is written with `"status":
"scaffolded"`.

### 3. Add `after:` for secondary attribution

A row recording another worker's observation as reported by this study. Unlocks
the largest single drop the audit found — Russell & Bauer's 22 genera, most of
Burch's per-taxon prose.

**Done when** the field validates (must name a real source or a free-text citation
when the underlying work is not in the bibliography) and Russell & Bauer's
*Sphenodon* rows carry it.

### 4. Re-mine every cited source

79 cited sources. The per-source ledger and progress table are in
[`MIGRATION-STATE.md`](MIGRATION-STATE.md), driven by `data/remine-status.json`.

Follow [`MINING.md`](MINING.md): extract everything the source states, file what
maps cleanly, park the rest with `blockedBy`. **A source is `remined` only when
every muscle it describes is either filed or parked** — the accounting must close,
as it did for Fisher & Goodman (111 = 43 filed + 50 parked + 18 in multi-muscle
rows) and Widrig et al. (38 = 20 + 16 + 2).

8 sources have no local copy and are `blocked-no-source`. Three of them are large —
Cunningham (243 rows), Gest (119), Walthall & Ashley-Ross (63) — so about 425 rows
cannot be verified until those are acquired. Record that; do not quietly trust them.

### 5. Flip the source of truth

`data/observations/` and `data/mapping/` become authoritative; `muscles-*.json`
becomes a build artefact and is git-ignored.

**Done when** `build.sh` regenerates `muscles-*.json` from scratch, CI passes, and
the app is unchanged.

### 6. Retire what the flip makes defunct

Chiefly `attribute_species.py`. Its whole job is inferring which animal a row is
about; under per-species files the filename declares it. The *evidence* for the
attribution survives as a header field, not as 300 lines of rules.

### 7. Phylogeny

`data/phylogeny.json` plus a script. Nothing blocks on it. `taxa.json` already
carries topology, so this is an upgrade rather than a new capability.

## Rules that outlive the migration

**Update the state files in the same commit as the work.** Not afterwards.
`MIGRATION-STATE.md` and `FILE-LEDGER.md` exist so that a session starting cold
does not have to re-derive the position, and they are worthless the moment they
lag. `validate.py` enforces what it can: every cited source must appear in
`remine-status.json`, and every file under `data/` and `scripts/` must appear in
`FILE-LEDGER.md`.

**Never mark a source `remined` without the accounting.** State the number the
paper describes and show it equals filed plus parked. "I read it and took what was
there" is what produced the drops the audit found.

**A scaffolded file is not evidence.** It is the previous pass's incompleteness in
a new shape.
