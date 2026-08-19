# Coverage, measured

**Every figure in this file is generated.** Run `python3 scripts/doc_counts.py
--write` after any change under `data/`; CI fails if it is stale. Nothing here is
hand-written, so nothing here can drift.

For what these numbers *mean* — how to read a thin column, why a percentage can
fall because rows arrived — see [`METHODS.md`](METHODS.md#reading-the-coverage-figures).
For what to do about them, see [`WORKLIST.md`](WORKLIST.md).

Definitions, because earlier versions of this file used at least two:

| Term | Means |
|---|---|
| occurrence row | any entry in a record's `occurrences` |
| present occurrence | one whose `present` is not `no` — `variable`, `uncertain` and `inferred` all count |
| scored occurrence | a present occurrence carrying its own `attachments` |
| `%att` | scored / present, per region or per taxon |
| observed row | an attachment row on an occurrence. Consensus rows are excluded from the resolution figures: one consensus row is inherited by up to twenty taxa, and counting it once per taxon inflates `side` and `landmark` coverage |

---

## The dataset

<!-- counts:headline -->
129 muscle records · 1308 present occurrences · 268 skeletal elements · 116 sources · 20 operational taxa
<!-- /counts:headline -->

<!-- counts:summary -->
Taxon-specific attachments cover **83%** of 1308 present occurrences. The thinnest columns of any size are Chondrichthyes at 48%, Anura at 53%, Aves at 63%; the thinnest regions are fin, hand, axial. `side` is on 55% of observed rows and `landmark` on 28%; `layer` resolves for 58 of 98 appendicular muscles; architecture data covers 21 muscle–taxon pairs across 2 taxa.
<!-- /counts:summary -->

## By region

<!-- counts:regions -->
| Region | Muscles | Present occurrences | Scored | %att |
|---|---:|---:|---:|---:|
| foot | 12 | 148 | 138 | 93% |
| leg | 10 | 88 | 82 | 93% |
| thigh | 10 | 82 | 74 | 90% |
| arm | 5 | 99 | 85 | 86% |
| pectoral | 16 | 261 | 223 | 85% |
| pelvic | 8 | 61 | 51 | 84% |
| forearm | 19 | 268 | 221 | 82% |
| cranial | 16 | 101 | 78 | 77% |
| axial | 15 | 42 | 29 | 69% |
| hand | 9 | 119 | 80 | 67% |
| fin | 9 | 39 | 23 | 59% |
| **all** | 129 | 1308 | 1084 | **83%** |
<!-- /counts:regions -->

## By taxon

<!-- counts:taxa -->
| Taxon | Present occurrences | Scored | %att |
|---|---:|---:|---:|
| Dipnoi | 7 | 7 | 100% |
| Pseudosuchia (stem) | 1 | 1 | 100% |
| Crocodylomorpha (stem) | 3 | 3 | 100% |
| Crocodyliformes (stem) | 7 | 7 | 100% |
| Monotremata | 114 | 112 | 98% |
| Theria | 378 | 359 | 95% |
| Theropoda (stem) | 38 | 34 | 89% |
| Actinistia | 7 | 6 | 86% |
| Crocodylia | 75 | 64 | 85% |
| Lepidosauria | 257 | 217 | 84% |
| Tetrapodomorpha (stem) | 42 | 33 | 79% |
| Caudata | 92 | 70 | 76% |
| Testudines | 57 | 41 | 72% |
| Aves | 111 | 70 | 63% |
| Anura | 72 | 38 | 53% |
| Actinopterygii | 14 | 7 | 50% |
| Synapsida (stem) | 4 | 2 | 50% |
| Chondrichthyes | 23 | 11 | 48% |
| Myxini | 3 | 1 | 33% |
| Petromyzontida | 3 | 1 | 33% |
<!-- /counts:taxa -->

## The gap that gates the roadmap

Phases 3 and 4 both compute per-taxon; both degrade to showing the consensus
repeated twenty times where occurrences are empty. A shift is only computable
where **two** taxa are scored for the same muscle, so the distribution matters
more than the total.

<!-- counts:scored -->
**Taxon-specific attachments: 1084 of 1308 present occurrences (83%).**
<!-- /counts:scored -->

<!-- counts:unscored -->
224 present occurrences still have no attachment rows.
<!-- /counts:unscored -->

### Observed attachment rows, by region

<!-- counts:holes -->
| Region | Muscles | Observed attachment rows |
|---|---:|---:|
| pectoral | 16 | 697 |
| forearm | 19 | 593 |
| foot | 12 | 451 |
| cranial | 16 | 354 |
| leg | 10 | 272 |
| arm | 5 | 252 |
| thigh | 10 | 237 |
| hand | 9 | 235 |
| pelvic | 8 | 183 |
| axial | 15 | 109 |
| fin | 9 | 57 |
<!-- /counts:holes -->

## The skeleton

Element *inventory* is healthy; *resolution* is the weaker half — how many rows
name a side or a landmark rather than the bare bone.

<!-- counts:skeleton -->
| | |
|---|---|
| Elements | 268, of which 248 (93%) carry at least one attachment |
| Observed attachment rows | 3440 |
| Rows naming a **landmark** | 956 (28%) |
| Rows naming a **side** | 1880 (55%) |
| Osteological correlates | 122 flagged, 114 carry a muscle |
<!-- /counts:skeleton -->

### Elements per muscle, by region

A parity check on whether the ontology is thick enough to carry the musculature
hung off it. Cranial runs high — a coarse adductor mandibulae complex sitting over
a finely divided skull. The pelvis, fin and forelimb run low.

<!-- counts:parity -->
| Region | Muscles | Elements | Elements per muscle |
|---|---:|---:|---:|
| cranial | 25 | 70 | 2.8 |
| hindlimb | 43 | 48 | 1.1 |
| pectoral | 34 | 31 | 0.9 |
| axial | 37 | 32 | 0.9 |
| forelimb | 59 | 46 | 0.8 |
| fin | 8 | 5 | 0.6 |
| pelvic | 31 | 16 | 0.5 |
<!-- /counts:parity -->

## Whose homology scheme each record follows

Recency governs homology and does not govern attachment; `homology.authority`
records the answer per record, derived from the most recent source cited on it
that was written to settle homology across more than one taxon. The rule is in
[`METHODS.md`](METHODS.md#recency-governs-homology-and-does-not-govern-attachment).

<!-- counts:authority -->
| | |
|---|---|
| Sources that can adjudicate a homology | 29 of 116 |
| Records following one | 115 of 129 (89%) |
| Median year of the governing source | 2016 |
| Records governed by pre-2010 work | 8 (7%) |
| Records with **no** homology-scope source | 14 — their homology rests on descriptive work alone |
<!-- /counts:authority -->

The records with **no** homology-scope source are the signal in that table. Each
is a muscle this dataset knows where to put on one animal and has no cross-taxon
treatment for — a different kind of gap from an unscored attachment, and one that
was invisible until the field existed. `validate.py` warns on each by name.
