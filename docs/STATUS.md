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
164 muscle records · 1618 present occurrences · 278 skeletal elements · 120 sources · 20 operational taxa
<!-- /counts:headline -->

<!-- counts:summary -->
Taxon-specific attachments cover **79%** of 1618 present occurrences. The thinnest columns of any size are Chondrichthyes at 48%, Testudines at 72%, Anura at 75%; the thinnest regions are cranial, fin, hand. `side` is on 56% of observed rows and `landmark` on 26%; `layer` resolves for 58 of 98 appendicular muscles; architecture data covers 21 muscle–taxon pairs across 2 taxa.
<!-- /counts:summary -->

## By region

<!-- counts:regions -->
| Region | Muscles | Present occurrences | Scored | %att |
|---|---:|---:|---:|---:|
| foot | 12 | 150 | 142 | 95% |
| leg | 10 | 108 | 102 | 94% |
| thigh | 10 | 150 | 139 | 93% |
| pelvic | 8 | 105 | 95 | 90% |
| arm | 5 | 106 | 92 | 87% |
| pectoral | 16 | 281 | 241 | 86% |
| forearm | 19 | 280 | 233 | 83% |
| axial | 15 | 59 | 45 | 76% |
| hand | 9 | 120 | 81 | 68% |
| fin | 9 | 39 | 23 | 59% |
| cranial | 51 | 220 | 92 | 42% |
| **all** | 164 | 1618 | 1285 | **79%** |
<!-- /counts:regions -->

## By taxon

<!-- counts:taxa -->
| Taxon | Present occurrences | Scored | %att |
|---|---:|---:|---:|
| Dipnoi | 7 | 7 | 100% |
| Pseudosuchia (stem) | 12 | 12 | 100% |
| Crocodylomorpha (stem) | 3 | 3 | 100% |
| Crocodyliformes (stem) | 7 | 7 | 100% |
| Theropoda (stem) | 38 | 34 | 89% |
| Actinistia | 7 | 6 | 86% |
| Crocodylia | 75 | 64 | 85% |
| Monotremata | 182 | 151 | 83% |
| Theria | 439 | 359 | 82% |
| Lepidosauria | 271 | 217 | 80% |
| Tetrapodomorpha (stem) | 42 | 33 | 79% |
| Caudata | 106 | 82 | 77% |
| Aves | 172 | 131 | 76% |
| Anura | 146 | 109 | 75% |
| Testudines | 57 | 41 | 72% |
| Actinopterygii | 19 | 12 | 63% |
| Myxini | 4 | 2 | 50% |
| Petromyzontida | 4 | 2 | 50% |
| Synapsida (stem) | 4 | 2 | 50% |
| Chondrichthyes | 23 | 11 | 48% |
<!-- /counts:taxa -->

## The gap that gates the roadmap

Phases 3 and 4 both compute per-taxon; both degrade to showing the consensus
repeated twenty times where occurrences are empty. A shift is only computable
where **two** taxa are scored for the same muscle, so the distribution matters
more than the total.

<!-- counts:scored -->
**Taxon-specific attachments: 1285 of 1618 present occurrences (79%).**
<!-- /counts:scored -->

### Extracted, not yet filed

A source's statement about a muscle in an animal can be extracted before anyone
decides which homology group it belongs to. Those rows live in
the study's own extraction file with `record: null`, and are **not** counted above
— they are not occurrences and move no coverage figure.

<!-- counts:parked -->
739 extracted observations from 7 sources are waiting for a record (639 on partial, 44 on no-record, 27 on nomenclature, 13 on homology, 12 on division, 4 on occupied). They carry no coverage weight — they are mining already done.
<!-- /counts:parked -->

<!-- counts:unscored -->
333 present occurrences still have no attachment rows.
<!-- /counts:unscored -->

### Observed attachment rows, by region

<!-- counts:holes -->
| Region | Muscles | Observed attachment rows |
|---|---:|---:|
| pectoral | 16 | 758 |
| forearm | 19 | 629 |
| foot | 12 | 463 |
| thigh | 10 | 438 |
| cranial | 51 | 401 |
| leg | 10 | 345 |
| pelvic | 8 | 339 |
| arm | 5 | 282 |
| hand | 9 | 237 |
| axial | 15 | 144 |
| fin | 9 | 57 |
<!-- /counts:holes -->

## The skeleton

Element *inventory* is healthy; *resolution* is the weaker half — how many rows
name a side or a landmark rather than the bare bone.

<!-- counts:skeleton -->
| | |
|---|---|
| Elements | 278, of which 258 (93%) carry at least one attachment |
| Observed attachment rows | 4093 |
| Rows naming a **landmark** | 1074 (26%) |
| Rows naming a **side** | 2281 (56%) |
| Osteological correlates | 126 flagged, 120 carry a muscle |
<!-- /counts:skeleton -->

### Elements per muscle, by region

A parity check on whether the ontology is thick enough to carry the musculature
hung off it. Cranial runs high — a coarse adductor mandibulae complex sitting over
a finely divided skull. The pelvis, fin and forelimb run low.

<!-- counts:parity -->
| Region | Muscles | Elements | Elements per muscle |
|---|---:|---:|---:|
| cranial | 27 | 72 | 2.7 |
| hindlimb | 44 | 52 | 1.2 |
| axial | 37 | 33 | 0.9 |
| pectoral | 35 | 31 | 0.9 |
| forelimb | 59 | 46 | 0.8 |
| fin | 8 | 5 | 0.6 |
| pelvic | 31 | 19 | 0.6 |
<!-- /counts:parity -->

## Whose homology scheme each record follows

Recency governs homology and does not govern attachment; `homology.authority`
records the answer per record, derived from the most recent source cited on it
that was written to settle homology across more than one taxon. The rule is in
[`METHODS.md`](METHODS.md#recency-governs-homology-and-does-not-govern-attachment).

<!-- counts:authority -->
| | |
|---|---|
| Sources that can adjudicate a homology | 31 of 120 |
| Records following one | 157 of 164 (96%) |
| Median year of the governing source | 2014 |
| Records governed by pre-2010 work | 43 (27%) |
| Records with **no** homology-scope source | 7 — their homology rests on descriptive work alone |
<!-- /counts:authority -->

The records with **no** homology-scope source are the signal in that table. Each
is a muscle this dataset knows where to put on one animal and has no cross-taxon
treatment for — a different kind of gap from an unscored attachment, and one that
was invisible until the field existed. `validate.py` warns on each by name.
