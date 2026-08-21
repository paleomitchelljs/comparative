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
> **Winterbottom (1973) is the next job and fifteen parked rows point at it.**
> Jayaram et al.'s palatal and opercular muscles have no records here, and
> Winterbottom's 93-page teleost synonymy carries every one of those names. It is
> cited already, for the fin muscles, and `not-started`.
>
> **Bauer (1997) is done: 12 animals of 12, where the file had one.** Re-run the
> ranking fresh — four sources came off it today.
>
> **Widrig et al. (2023) is done too**, and the way it opened is the thing to carry
> forward: a reading note's tooling verdict was retested and failed. Before planning
> around any note that says a paper cannot be extracted, retest it — three of those
> have now fallen.
>
> **Molnar et al. (2017) on chameleon limbs is done** — it was the top of the
> density ranking with zero rows filed, and both tables are now mined: 78 muscle
> entries across *Chamaeleo calyptratus*, *Trioceros melleri* and *Aspidoscelis
> uniparens*, 227 rows in three new extraction files. Run the ranking again before
> picking the next one; it has changed.
>
> **The Gest pass left one gap open and closed the other.** `lumbricales-pes` now
> exists and carries five species; it was created because Gest's four human pedal
> lumbricals had to be parked on `no-record` while every other intrinsic group of
> the autopod was already doubled with a `-pes` counterpart. **The human perineum
> still has no record**: six cloacal-sphincter derivatives are parked, and the
> reason is not that nothing is described but that nothing joins the descriptions
> — Osawa (1898) has *Sphenodon*'s sphincter cloacae and transversus perinei,
> Ercoli et al. (2012) has *Galictis*'s ischiocavernosus and bulbospongiosus, and
> no cited source derives one from the other. It needs a comparative treatment
> before it needs a record.
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

## Five schema limits closed, 2026-08-20

Both were costing yield on every mining round, and both are now derived rather
than authored — see [`SCHEMA.md`](SCHEMA.md).

**`parts[].attachments`.** An occurrence held one union of attachment rows, so a
record that is one muscle in a salamander and six in a human could say that six
sites were used and never which muscle used which. Every named part in the dataset
carried a name and nothing else. The detail was never missing — it was in
`observations/` as one row per muscle and `--join` was flattening it — so the join
now carries each row's attachments onto the part of that name. No paper reopened.

Two rules keep it honest: only rows from **one source** become parts, because rows
from different sources are one muscle described twice; and it **never invents
`division`**, because how far a group has split is a judgement. Where the
occurrence declares nothing, `validate.py` warns and names the rows.

**`spans`.** `region` says where a record is filed and must stay a single value —
it is half the extraction key. It cannot also say where the muscle goes. `spans`
is the second pair of region columns, computed from the elements at each end:
identical for a muscle that stays put, and the point of the pair for a boundary
crosser. The app has a facet for it and `presence.csv` has three columns.

**`stage`.** An occurrence is now one per (record, species, **stage**). It was one
per (record, species), which is why a source describing both stages of one animal
could not be scored: Bauer (1997) gives the salamandrid depressor mandibulae as one
muscle in the adult and two separate muscles in the larva, and the two collided on
`division`. Six rows were parked for want of the field; they are filed, and
*Salamandra salamandra* now carries `larval / divided` beside `adult / heads`.
Absent is its own value and **does not mean adult** — nearly every row in the
dataset says nothing, because nearly every source does not distinguish.

**`fusedWith`.** `present` had five states and none said *fused with its
neighbour*. That is not an absence — `present: "no"` says the record is empty and a
fused muscle is not — and not a division either, because the two may be different
records. It came up four times in Molnar et al. (2017) alone and each time the claim
went to prose. An entry naming a record is symmetric and the join closes it; an
entry naming a muscle this dataset has no group for stays on the one row. `present`
stays `yes`, because fusing and losing are different events on a branch.

**`covers`.** The extraction key must resolve to exactly one record, which is
right and cost a source's umbrella terms any row at all: `deltoid`, `quadriceps
femoris`, `epicranius`, `occipitofrontalis` and `digastric` were filed as their
halves and unfindable by the name a reader would actually use. A row can now carry
`covers` instead of `record` — a third state beside filed and parked, holding no
observation, existing so the word resolves. `data/aliases.json` is generated from
them and the app searches it, so `deltoid` returns both deltoid records and each
card names the other.

**Nothing on the list is open now.** The five limits audited on 2026-08-20 are all
closed. What is left is not schema but coverage: 639 rows parked on `partial` from
Russell & Bauer and Walker, and 69 sources still `not-started`.

## Task board

| # | Task | State |
|---|---|---|
| 1 | `region` on occurrence names; kill the 25 ambiguous keys | **done** |
| 2 | Scaffold generator + lossless round-trip proof | **done** |
| 3 | `after:` field for secondary attribution | **done** |
| 4 | Re-mine every cited source | **in progress — 7 of 79 to exhaustion, 2 more partly** |
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
| `remined` | 11 | 819 |
| `not-started` | 64 | 1731 |
| `blocked-no-source` | 4 | 80 |
| **total** | **79** | **2630** |

**11 of 79 cited sources re-mined** (13%).
<!-- /counts:remine -->

### What counts as done

A source is `remined` only when **every muscle it describes is either filed or
parked**, and the note states the arithmetic. Eleven sources have cleared that bar:

- **Jayaram, Dhanze & Singh (1983)** — cranial muscles of three *Arius* catfishes.
  **20 muscles, three animals, 59 rows: 44 filed, 15 parked.** It had held **three
  rows on *Arius* sp. with no attachments at all**, scored to the genus because "the
  shared condition is what was taken" — which threw away the paper's entire point,
  since it was written to test whether cranial myology separates species that are
  hard to separate, and nine of eighteen muscles differ. Fifteen new skeletal
  elements, the teleost opercular, palatal and hyoid series, which this file had none
  of despite carrying four fish sources. The parks are the palatal and opercular
  muscles and they point at **Winterbottom (1973)**, whose 93-page teleost synonymy
  carries every one of those names and is `not-started` — the obvious next job.

- **Bauer (1997)** — urodele jaw openers. **12 animals of 12**: 10 adults filed in 12
  rows, 3 larval columns parked, nine species added. The file held **one**. Its
  reading note had named what was left and the answer was most of the paper, which is
  the *does the paper describe more animals than the file does?* failure again — the
  second in two days. **Four of the muscles had never been described by anyone**, and
  three of the four *Triturus* take occipito-otic fibres that Özeti & Wake (1969), the
  standard reference, do not mention. The larvae are parked on `occupied` because an
  occurrence carries no ontogenetic stage; a stage field settles it.

- **Widrig et al. (2023)** — tinamou pectoral atlas. **All 44 muscle sections: 38
  filed, 6 parked.** It held 3 rows, and the reading note said the rest could not be
  read because the two-column PDF interleaves under `pdftotext`. It does not: the
  `-layout` output already holds both columns side by side, and slicing each page at
  the column boundary gives every section cleanly. **Third expired tooling verdict**,
  after Liparini & Schultz and Fisher & Goodman. Nothing in the distal wing was
  mapped by eye — Abdala & Diogo (2010) carries the avian synonymies, and two of them
  matter because the names lie: the avian *pronator superficialis* is the flexor
  carpi radialis and the avian *pronator profundus* is the pronator teres.

- **Molnar et al. (2017)** — chameleon limbs. **78 muscle entries, three animals,
  227 rows, and the source had never been mined at all.** It topped the
  attachment-density ranking with zero rows filed, which is the signal `MINING.md`
  describes, and its own reading note had already scoped the pass. Two new records
  fell out of it or ran beside it: `dorsometatarsales`, the second missing `-pes`
  counterpart found in two days. The paper's headline reads as rows — flexores breves
  profundi, dorsometacarpales and contrahentes keep their counts in an autopodium
  rebuilt around a digital cleft, and the flexores breves superficiales change job
  without changing origin, insertion or name.

- **Gest, Anatomy Tables (2001)** — **239 distinct muscles: 221 filed, 18 parked.**
  The human column, which was the largest single gap in the dataset and is now the
  best-attached one. It held 105 rows, every one of them a *group* row carrying a
  lumped name — `Masseter, temporalis, the pterygoids and the tensors` — and the
  union of a group's attachments, so no individual muscle had an origin and an
  insertion of its own. 187 per-muscle rows were added under those group rows and
  the join merges them: the mapping layer gains a key per human muscle name, the
  occurrence gains the attachment rows, and each muscle's reading sits under the name
  Gest used. It moved the cranial region further than any pass so far, on both
  attachment coverage and the number of records carrying any attachment at all; the
  figures are in `STATUS.md`. Sixteen new skeletal elements. **Eleven facial-muscle
  records had no attachments for any species** before this pass. See the reading note for the region-by-region
  breakdown; the parks are the human perineum, which has no record here at all, and
  the smooth muscles, which no record here can hold.
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
- **Přikryl et al. (2009)** — **13 animals of 13**, 138 rows: 109 filed, 29 parked.
  Held one frog and 9 rows at the start of the day. The nine frogs get a file each;
  the three caudates get one, because the paper describes them as a clade rather
  than as specimens, so they sit on `caudata-generalised`. *Pyxicephalus* appears
  only in a stimulation experiment and correctly yields nothing. **The largest
  single body of comparative anuran hindlimb myology here**, and the caudate file
  is the outgroup that makes the anuran departures legible.
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

**The human column is the biggest single gap.** `gest-anatomy-tables` holds **272
muscles** with origin, insertion, action, innervation and arterial supply; this
dataset carries **116 rows under 94 names**, and 199 of the table's muscles match
no record by name. The reading note has the measured breakdown and the diff recipe.
Most will map on inspection — `deltoid`, the two `extensor carpi radialis`, the
suboccipital group — but each is a homology call, and the table is finer than these
records in the hand, foot, perineum and larynx, so expect to park a real fraction.
Worth doing next: the human column is the baseline every other column is read
against.


The audit of 2026-08-19 examined four and found drops in all four. Their reading
notes carry the detail; each is `not-started` until re-mined.

| Source | Held | Also contains |
|---|---|---|
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
| `gest-anatomy-tables` | *homo-sapiens* | 20 | no-record 13, assigned 5, homology 2 |
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
| `widrig-etal-2023` | *nothoprocta-pentlandii* | 6 | homology 4, no-record 1, nomenclature 1 |
| `jayaram-etal-1983` | *arius-arius* | 5 | no-record 5 |
| `jayaram-etal-1983` | *arius-caelatus* | 5 | no-record 5 |
| `jayaram-etal-1983` | *arius-thalassinus* | 5 | no-record 5 |
| `russell-bauer-2008` | *dipsosaurus-sp* | 5 | partial 5 |
| `osawa-1898` | *sphenodon-punctatus* | 4 | occupied 4 |
| `prikryl-etal-2009` | *barbourula-busuangensis* | 4 | no-record 2, homology 2 |
| `prikryl-etal-2009` | *rana-esculenta* | 3 | no-record 3 |
| `prikryl-etal-2009` | *xenopus-laevis* | 3 | no-record 2, homology 1 |
| `prikryl-etal-2009` | *bombina-orientalis* | 2 | no-record 1, homology 1 |
| `prikryl-etal-2009` | *bufo-guttatus* | 2 | homology 1, no-record 1 |
| `prikryl-etal-2009` | *pipa-pipa* | 2 | no-record 2 |
| `russell-bauer-2008` | *cnemidophorus-sp* | 2 | partial 2 |
| `russell-bauer-2008` | *uroplatus-sp* | 2 | partial 2 |
| `walker-1973` | *lepidochelys-kempii* | 2 | partial 2 |
| `freitas-etal-2017` | *iguana-iguana* | 1 | nomenclature 1 |
| `prikryl-etal-2009` | *pelobates-fuscus* | 1 | homology 1 |
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
