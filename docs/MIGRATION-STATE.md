# Migration state — read this first

**What is done, what is next, and what is blocked.** The plan is in
[`MIGRATION.md`](MIGRATION.md); file trust is in [`FILE-LEDGER.md`](FILE-LEDGER.md).

**Update this file in the same commit as the work.** Its only value is being
current.

---

## Next action

> **Task 4 — re-mine.** Pick the next source with the ranking in
> [`MINING.md`](MINING.md#then-divide-by-the-rows-the-source-already-carries):
> attachment density per page divided by rows already filed. A dense paper holding
> almost no rows is a source that was read badly, and it found both re-mines of
> 2026-08-20.
>
> Mining works end to end now. It did not before: `--join` read `_occ` and `_keys`
> off every filed row, which only `--split` writes, so the first hand-written row
> crashed step 0 of the build. Rows written the way `MINING.md` documents now
> join, two studies of one animal merge by union, and a second dissection no
> longer has to be recorded by copying the first one's prose into a new file.
>
> **Still half-done from the flip**: `seed_nerves`, `seed_actions` and
> `promote_landmarks` read and write `muscles-*.json`, which is now generated, so
> their output cannot reach the source of truth. They are out of `build.sh` until
> ported to `data/observations/`. **`promote_landmarks` has 79 pending
> refinements** — `ribs → true-ribs`, `mandible → retroarticular-process` — and is
> the one worth doing first.

## Task board

| # | Task | State |
|---|---|---|
| 1 | `region` on occurrence names; kill the 25 ambiguous keys | **done** |
| 2 | Scaffold generator + lossless round-trip proof | **done** |
| 3 | `after:` field for secondary attribution | **done** |
| 4 | Re-mine every cited source | **in progress — 5 of 79 to exhaustion, 3 more partly** |
| 5 | Flip source of truth to `observations/` + `mapping/` | **done** |
| 6 | Retire what the flip made defunct | **done — 7 scripts deleted** |
| 7 | `phylogeny.json` | not started |

## The model is proven

`scripts/build_observations.py --check` rebuilds `muscles-*.json` from the **248
observation files and 78 mapping files (2740 rows)** and diffs. The round trip
is **byte-identical** — `git diff` is empty after a full split and join, and
`build.sh` is still a fixed point.

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
| `remined` | 5 | 105 |
| `not-started` | 70 | 1892 |
| `blocked-no-source` | 4 | 80 |
| **total** | **79** | **2077** |

**5 of 79 cited sources re-mined** (6%).
<!-- /counts:remine -->

### What counts as done

A source is `remined` only when **every muscle it describes is either filed or
parked**, and the note states the arithmetic. Five sources have cleared that bar:

- **Fisher & Goodman (1955)** — 111 muscles with an origin paragraph: 43 filed,
  50 parked, the rest inside multi-muscle rows. Moved the Aves column further than
  any single pass so far; the figures are in `STATUS.md`.
- **Widrig et al. (2026)** — 38 blocks: 20 filed, 16 parked, 2 folded into
  existing rows.
- **Liparini & Schultz (2013)** — 16 muscles in its Table 2: 16 filed, 0 parked,
  merging into 13 occurrences. It had been carrying **one** row, and its note
  recorded why: the two-column layout interleaved under `pdftotext`, so only
  claims verifiable from context were scored. That note also named the fix —
  plain `pdftotext`, which `MINING.md` documents — and **nobody ran it**. The
  paper carries a table of origin, insertion and inference level for every muscle.
  *Prestosuchus* went from 1 occurrence to 13, the first real body of pseudosuchian
  stem myology here.
- **Springer & Johnson (2015)** — **6 animals of 6**, all filed. It had one, and
  unlike the others its note said so plainly: "five more species available from
  this paper when the fish end of the record is worth widening". An honest note,
  and still one column from a six-animal paper. `branchial-constrictors` now
  carries six eels, *Simenchelys* the most divided occurrence on the record at 27
  parts. Two published errors corrected on the rows, and *Serrivomer*'s gill-arch
  muscles had **never been described before this paper**.
- **Freitas et al. (2017)** — 21 muscles: 20 filed, 1 parked. It had been carrying
  **one** row, on the reasoning that Russell & Bauer already covered the same
  animal at higher resolution and this source therefore "confirms rather than opens
  new ground". Both halves were wrong, and the pass is worth reading as a pattern:
  the two dissections **disagree on eight of the twenty muscles**, including which
  bone the deltoideus clavicularis arises from, and the paper's own headline — a
  tendinous-arc origin for the caudal triceps head, previously known only in
  crocodilians — was not in the dataset at all.

**Both passes found the same shape of failure, and it is not in the papers.** Each
source was left nearly unmined for a stated reason, recorded in its reading note,
which did not survive being checked:

| Source | The reason given | What was true |
|---|---|---|
| Freitas et al. | Russell & Bauer already cover this animal better | The two dissections **disagree on eight of twenty muscles** |
| Liparini & Schultz | The PDF's columns interleave under `pdftotext` | Plain `pdftotext` reads it cleanly, and the note said so itself |

So: **"already covered by a better paper" is not a reason** — an attachment is an
observation, and two workers who each opened an animal do not compete. And **a
tooling verdict expires** — one cost 15 of 16 muscles. Where a reading note explains
why a source yielded little, treat that explanation as the least-checked claim in
the repository and check it first.

**Přikryl et al. (2009) is the third instance and a different variety.** Nothing in
its note was wrong; it was incomplete in a way the note could not show. It listed
four records as "not scored" when thirteen of the paper's twenty-five muscles were
missing, and it did not mention that the paper **dissects thirteen animals**, of
which the dataset holds one. *Discoglossus* is now complete at 25 of 25. So the
check to run on a reading note is not only "is this true?" but "**does the paper
describe more animals than the file does?**" — `MINING.md` already says a paper
describing N animals should produce N columns, and it is the rule most often
broken.

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
| Přikryl et al. (2009) | 53 rows on **three** frogs; *Discoglossus* complete at 25 of 25 | **Six more dissected frogs and three caudates.** Each written as differences from the *Discoglossus* baseline, so the expensive part is done. Best target |
| Russell & Bauer (2008) | 71 rows, 70 on *Iguana* | 558 statements across 22 lepidosaur genera. Mostly **secondary** — needs Task 3 |
| Walker (1973) | 22 rows, all *Trachemys* | 90 statements across 9 other turtle genera, **first-hand**. Best target |
| Osawa (1898) | 63 rows, all limb | The whole cranial and axial myology |
| Burch (2014) | 38 rows, all *Tawa* | A bracket table of 35 extant taxa, 7 already species here |

## Parked material, by where it came from

Extracted and waiting for a record. Nothing here has coverage weight; all of it is
reading that will not have to be done again.

<!-- counts:parked-detail -->
| Source | Species | Rows | Blocked on |
|---|---|---:|---|
| `russell-bauer-2008` | *sphenodon-punctatus* | 84 | partial 84 |
| `russell-bauer-2008` | *varanus-exanthematicus* | 78 | partial 78 |
| `russell-bauer-2008` | *gekko-gecko* | 66 | partial 66 |
| `fisher-goodman-1955` | *grus-americana* | 50 | no-record 20, nomenclature 19, division 11 |
| `russell-bauer-2008` | *lacerta-sp* | 46 | partial 46 |
| `russell-bauer-2008` | *chamaeleo-calyptratus* | 43 | partial 43 |
| `russell-bauer-2008` | *phrynosoma-sp* | 34 | partial 34 |
| `walker-1973` | *pelomedusa-subrufa* | 30 | partial 30 |
| `russell-bauer-2008` | *tupinambis-sp* | 28 | partial 28 |
| `walker-1973` | *testudo-graeca* | 25 | partial 25 |
| `walker-1973` | *trionyx-spiniferus* | 24 | partial 24 |
| `russell-bauer-2008` | *crotaphytus-sp* | 23 | partial 23 |
| `walker-1973` | *chelodina-longicollis* | 23 | partial 23 |
| `russell-bauer-2008` | *ameiva-sp* | 19 | partial 19 |
| `russell-bauer-2008` | *heloderma-sp* | 19 | partial 19 |
| `widrig-etal-2026` | *chauna-torquata* | 16 | no-record 8, nomenclature 7, homology 1 |
| `walker-1973` | *chelydra-serpentina* | 14 | partial 14 |
| `walker-1973` | *caretta-caretta* | 12 | partial 12 |
| `russell-bauer-2008` | *plestiodon-sp* | 10 | partial 10 |
| `russell-bauer-2008` | *tarentola-sp* | 10 | partial 10 |
| `russell-bauer-2008` | *anolis-sp* | 9 | partial 9 |
| `walker-1973` | *geochelone-elephantopus* | 9 | partial 9 |
| `russell-bauer-2008` | *sceloporus-sp* | 8 | partial 8 |
| `prikryl-etal-2009` | *ascaphus-truei* | 6 | homology 3, no-record 2, division 1 |
| `prikryl-etal-2009` | *discoglossus-pictus* | 6 | homology 3, no-record 3 |
| `russell-bauer-2008` | *ctenosaura-pectinata* | 6 | partial 6 |
| `russell-bauer-2008` | *ophisaurus-sp* | 6 | partial 6 |
| `russell-bauer-2008` | *dipsosaurus-sp* | 5 | partial 5 |
| `osawa-1898` | *sphenodon-punctatus* | 4 | occupied 4 |
| `prikryl-etal-2009` | *rana-esculenta* | 3 | no-record 3 |
| `russell-bauer-2008` | *cnemidophorus-sp* | 2 | partial 2 |
| `russell-bauer-2008` | *uroplatus-sp* | 2 | partial 2 |
| `walker-1973` | *lepidochelys-kempii* | 2 | partial 2 |
| `freitas-etal-2017` | *iguana-iguana* | 1 | nomenclature 1 |
| `russell-bauer-2008` | *eumeces-sp* | 1 | partial 1 |
| `russell-bauer-2008` | *xantusia-sp* | 1 | partial 1 |
<!-- /counts:parked-detail -->

## Decisions taken, so they are not relitigated

- **Extraction is keyed on (species × study), not on homology group.** 2026-08-19.
- **Everything must be re-mined**, not migrated forward. The audit found drops in
  4 of 4 sources, so current rows are a partial extraction throughout.
- **The mapping is per source.** A global name table would destroy the
  disagreements the dataset exists to hold.
- **The key is (name, region), not name.** 25 collisions proved it.
- **Serial correspondence sources do not set `homology.authority`.** 2026-08-19.
- **Element correspondences exist** for "may be one element, undemonstrated".

## The mapping layer, settled

**`data/mapping/` is a generated view.** The homology assignment lives on each
observation row as `record`; the join regenerates the view from those rows, and
`validate.py` treats it as a fixed point — a stale or hand-edited file is an
error, because one that looked authoritative and was ignored would be worse than
none.

It answers the question that made the layer worth having: **if I move this name to
another record, what does it touch?** Each key carries the species it covers.
Cunningham's `abductor hallucis|foot` covers fourteen.

```jsonc
"abductor hallucis|foot": {
  "record": "abductor-et-extensor-digiti-i-pes",
  "species": ["bradypus-tridactylus", "castor-fiber", … 14 in all]
}
```

Writing a new row therefore touches one file, not two, and the eventual UI build
can read the homology layer on its own. **To re-homologise, change `record` on the
rows** — the view follows.

## Open questions

- Ergonomics of 220 files at a median of 4 muscles, 58 of them singletons. Live
  with it, or group small studies?
- Cross-taxon review — seeing every animal's latissimus at once — becomes generated
  rather than authored. That is the one thing the current model does better, and
  the generated view has to be good enough to review from.
