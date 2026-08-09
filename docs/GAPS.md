# Data gaps after plumbing `papers/`

Measured, not estimated. Regenerate the numbers with `python3 scripts/export_matrix.py`
and the audit block in the session log; all figures below are current as of this
pass.

**State:** 92 muscles · 537 occurrences · **154** skeletal elements · **42** sources · 16 taxa.

> **Updated after the second plumbing pass.** The Diogo et al. (2016) supplementary
> tables and the Werneburg appendix extractor have both been run. Movement since
> the first measurement:
>
> | | before | now |
> |---|---:|---:|
> | taxon-specific attachments | 13% | **18%** |
> | *Latimeria* (Actinistia) | 0% | **86%** |
> | *Neoceratodus* (Dipnoi) | 0% | **100%** |
> | fin-region attachment rows | 0 | **13** |
> | cranial attachment rows | 6 | **10** |
> | skeletal elements | 121 | **154** |
> | architecture records | 0 | **4** |
>
> The two sarcopterygian fish columns went from nothing to near-complete, which
> was the highest-yield item on the list below. Gaps 1 (partly), 4 (partly) and
> 6 are now closed or in progress; the rest stand.

Every PDF in `papers/` now has a `sources.json` entry. Four were byte-identical
duplicates and were deleted; two are declared out of scope (a catfish brain, a
review of cardiac evolution) and are listed only so the folder is fully
accounted for.

---

## The one gap that blocks everything downstream

**Taxon-specific attachments: 86 of 479 present occurrences (18%).**

Everything else in the roadmap depends on this number. The phylogeny view (phase
3) computes gains and losses from per-taxon records; the diagram (phase 4) draws
per-taxon bands. Both degrade to showing the consensus repeated 16 times if the
occurrences are empty.

It is also the number that decides whether "attachment change is data" is true in
practice. At 18% a computed shift table is still closer to a demonstration than
an analysis — but the distribution now matters more than the total, because two
whole taxa are complete and two whole regions are still empty.

### Where the hole is

| Region | Muscles | Taxon-attachment rows |
|---|---:|---:|
| pectoral | 16 | 35 |
| fin | 7 | 13 |
| cranial | 15 | 10 |
| arm | 5 | 9 |
| pelvic | 5 | 8 |
| forearm | 18 | 6 |
| thigh | 7 | 4 |
| **hand** | **9** | **0** |
| **leg** | **7** | **0** |
| **foot** | **3** | **0** |

By taxon, the sarcopterygian fish end is now the *best*-covered:

| Taxon | Present rows | With attachments |
|---|---:|---:|
| **Dipnoi** | 7 | **7 (100%)** |
| **Actinistia** | 7 | **6 (86%)** |
| Actinopterygii | 11 | 0 |
| Chondrichthyes | 17 | 1 |
| Tetrapodomorpha (stem) | 7 | 0 |
| Myxini, Petromyzontida | 4 | 0 |

**The autopod is now the sharpest hole** — hand, leg and foot are at zero across
21 muscles. That is also where Abdala & Diogo's best teaching material sits (the
intrinsic hand musculature, and the position-versus-identity digit story), so it
is worth a targeted source hunt.

---

## Gap-by-gap, with what would close it

### 1. Fish and sarcopterygian attachments — **mostly closed**

Diogo et al. (2016) Supplementary Tables S1–S4 have been mined. *Latimeria* is at
86% and *Neoceratodus* at 100%; the fin region went from zero attachment rows to
13, sourced to `diogo-etal-2016-si`.

**Still open at this end:** *Polypterus* (Actinopterygii, 0%) and Chondrichthyes
(6%). The supplementary's Tables S5–S6 name their muscles in the homology matrix
but do not give per-muscle attachments the way S1–S4 do for the sarcopterygians.
The stem-tetrapodomorph column (0%) is inference from osteological correlates and
would come from Molnar et al. (2018) Tables S1–S6 rather than from dissection.

### 2. Hindlimb attachments — 15 rows against the forelimb's 50

Partly closeable from papers already here:

- **Klinkhamer et al. (2017)** covers the crocodylian hindlimb as well as the
  forelimb; this pass mined it for iliofemoralis, caudofemoralis, femorotibialis,
  ambiens, ischioflexorius and extensor iliotibialis. More remains in it.
- **Allen et al. (2014)** and **Bishop & Pierce (2024)** carry more.

Not closeable from what is here: amphibian and avian hindlimb attachment detail.
Diogo & Molnar (2014) is a homology-table paper — it establishes correspondence,
not attachment topography.

### 3. Hand and foot — 12 muscles, 0 taxon rows

Abdala & Diogo (2010) name the intrinsic muscles across six taxa but describe
attachments only coarsely, and Diogo & Molnar (2014) do the same for the foot.
This needs dedicated sources. Given that the intrinsic hand musculature is one
of the project's better teaching stories — lizard and salamander hands having
*more* intrinsic muscles than human ones — it is worth a targeted search.

### 4. `side` 30%, `landmark` 11% — moving slowly

Currently 156 of 511 rows carry a side and 46 a landmark. The best sources are
those that describe attachments with an explicit aspect: **Klinkhamer et al.
(2017)** is the model ("proximo-lateral coracoid", "ventro-lateral humerus"), and
**Ercoli et al. (2014)**, **Gambaryan et al. (2015)** and **Werneburg (2011)**
are all mineable in the same way and not yet fully worked.

`scripts/extract_werneburg_appendix.py` has now been run. Its 78 turtle cranial
units were mapped onto seven dataset muscles, which drove 33 new skeletal
elements (the skull roof, braincase and the postdentary mandibular series) and
turtle attachment records for the adductor components, depressor mandibulae,
intermandibularis, interhyoideus, hypobranchials and extraocular muscles.

The proportion barely moved because adding elements adds rows to the denominator
as fast as it adds sides. **The percentage is a poor progress metric here**;
absolute counts by region are the thing to watch.

### 5. `layer` — 41 of 77 appendicular muscles (53%)

The 36 without it are mostly muscles no source in `papers/` assigns to a
superficial or deep layer. Filling them means either finding a source that does,
or accepting that the four-cell classification of Mansuit & Herrel (2021) simply
does not resolve every muscle. **The honest answer may be that this stays
partial**, and the hierarchy view should keep its "layer not assigned" bucket.

### 6. Muscle architecture — **field now exists, 4 records**

An `architecture` block sits on occurrence rows, carrying species, n, and per-part
mass, fascicle length and PCSA with standard deviations. Populated from Hudson et
al. (2011) for the cheetah forelimb — latissimus dorsi, pectoralis, supracoracoideus
(as supraspinatus + infraspinatus) and triceps brachii — with the greyhound
comparison recorded. Exports to `architecture.csv`.

**Still open:** the cheetah *hindlimb* paper is in `papers/` and unmined; Allen et
al. (2014), Ercoli et al. (2014) and Fahn-Lai et al. (2020) likewise. Mansuit &
Herrel (2021) names the rest (Huby et al. 2021 for *Latimeria*; Dick & Clemente
2016 and Cieri et al. 2020 for varanids; Payne et al. 2005 for horse).

### 7. No axial musculature

Epaxial and hypaxial series are entirely absent, and no source in `papers/`
covers them. A deliberate scope decision so far, but it means the dataset cannot
speak to trunk-limb integration, which matters for the locomotor story.

### 8. Nine sources cited but not yet used in records

| Source | What it would add |
|---|---|
| Werneburg & Maier (2019) | Turtle skull ontogeny — developmental sequence for the cranial records |
| Werneburg & Preuschoft (2024) | Temporal fenestration ↔ adductor volume; osteological-correlate side of cranial reconstruction |
| Gai et al. (2022) | Fossil sequence for the spiracular region; would source the spiracle→tympanic claim now stated without one |
| Miyashita (2016) | Jaw origin; background for why cyclostome feeding muscles are not homologised with the adductor complex |
| Clack et al. (2016) | Ear evolution volume — hyomandibula→stapes detail |
| Higashiyama et al. (2016) | Vagal innervation and the head–trunk boundary; complements Sefton et al. (2016) |
| Demuth et al. (2022) | Method for 3D muscle volumes and lines of action from skeletal geometry — the bridge from these attachment records to biomechanics |
| Huynen et al. (2014) | Moa *tbx5*; forelimb identity, no muscle-level data |
| Richardson (2022) | Evo-devo homology framing; conceptual, not a record source |

Only the first six would produce new records. Demuth is a methods paper worth
reading before phase 4, since it defines what a diagram would need to support
downstream reconstruction.

---

## What this means for phases 3–5

**Phase 3 (phylogeny view) is buildable now** and does not depend on the
attachment gap. The presence matrix is 92 × 16 and complete — that is the
character matrix, and it is the one thing that *is* dense. Gains, losses and
subdivisions can be mapped today. The `derivatives` edges give subdivisions for
free.

**Phase 5 (architecture) is additive** and can proceed independently.

**Phase 4 (the diagram) should wait**, or be scoped to the pectoral girdle and
arm only — the one region with enough per-taxon attachment data (44 rows across
21 muscles) to make a per-taxon redraw meaningful. Attempting a whole-body
diagram at 13% attachment coverage would mean drawing the consensus and labelling
it as sixteen different animals.

### Suggested order given the gaps

1. ~~Diogo et al. (2016) SI~~ — **done**, sarcopterygian fish now near-complete.
2. ~~Werneburg extractor~~ — **done**, turtle cranial records seeded.
3. **Phase 3** — no new data needed, and still the obvious next build.
4. **Phase 5** — the field and pipeline exist; extending it is now data entry
   from papers already in hand (cheetah hindlimb, Allen, Ercoli, Fahn-Lai).
5. **Phase 4**, scoped to pectoral/arm first. Note the fin region now has enough
   attachment data (13 rows across 7 muscles, two taxa near-complete) that a
   fin-to-limb schematic is also viable.

**Newly available and unmined:** Winterbottom (1973), a 93-page descriptive
synonymy of teleost striated muscle. It is the richest untapped synonym source in
the collection and would materially improve the search index for the
actinopterygian end, which is currently the weakest column for names.
