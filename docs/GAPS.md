# Data gaps after plumbing `papers/`

Measured, not estimated. Regenerate the numbers with `python3 scripts/export_matrix.py`
and the audit block in the session log; all figures below are current as of this
pass.

**State:** 92 muscles · 537 occurrences · 121 skeletal elements · 37 sources · 16 taxa.

Every PDF in `papers/` now has a `sources.json` entry. Four were byte-identical
duplicates and were deleted; two are declared out of scope (a catfish brain, a
review of cardiac evolution) and are listed only so the folder is fully
accounted for.

---

## The one gap that blocks everything downstream

**Taxon-specific attachments: 64 of 479 present occurrences (13%).**

Everything else in the roadmap depends on this number. The phylogeny view (phase
3) computes gains and losses from per-taxon records; the diagram (phase 4) draws
per-taxon bands. Both degrade to showing the consensus repeated 16 times if the
occurrences are empty.

It is also the number that decides whether "attachment change is data" is true
in practice. At 13%, a computed shift table is a demonstration rather than an
analysis.

### Where the hole is

| Region | Muscles | Taxon-attachment rows |
|---|---:|---:|
| pectoral | 16 | 35 |
| arm | 5 | 9 |
| pelvic | 5 | 7 |
| thigh | 7 | 4 |
| leg | 7 | 4 |
| forearm | 18 | 6 |
| cranial | 15 | 6 |
| **hand** | **9** | **0** |
| **foot** | **3** | **0** |
| **fin** | **7** | **0** |

And by taxon — the fish and fossil end is empty:

| Taxon | Present rows | With attachments |
|---|---:|---:|
| Myxini, Petromyzontida, Actinopterygii, Actinistia, Dipnoi, Tetrapodomorpha | 36 | **0** |
| Chondrichthyes | 17 | 1 |
| Caudata | 63 | 7 |
| Anura | 55 | 4 |
| Testudines / Lepidosauria / Crocodylia / Aves | 227 | 34 |
| Synapsida (stem) / Monotremata / Theria | 81 | 17 |

The fish rows being empty is the sharpest problem, because the fins-to-limbs
transition is exactly where attachment change should be most informative.

---

## Gap-by-gap, with what would close it

### 1. Fish and sarcopterygian attachments — 0 rows

Diogo et al. (2016) state that their **Supplementary Tables S1–S4 show all
muscle–bone attachments** for *Latimeria*, *Neoceratodus* and *Polypterus*. The
PDF in `papers/` is the main article only; the SI is a separate download.

**This is the single highest-yield item in the list.** One download would take
six taxa from zero to well-attested and make the fin-to-limb attachment story
computable rather than narrated. Paper is CC-BY, so the SI is freely available.

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

### 4. `side` 31%, `landmark` 9%

Currently 156 of 511 rows carry a side and 46 a landmark. The best sources are
those that describe attachments with an explicit aspect: **Klinkhamer et al.
(2017)** is the model ("proximo-lateral coracoid", "ventro-lateral humerus"), and
**Ercoli et al. (2014)**, **Gambaryan et al. (2015)** and **Werneburg (2011)**
are all mineable in the same way and not yet fully worked.

`scripts/extract_werneburg_appendix.py` already parses Werneburg's 78 turtle
cranial units with origin, insertion, function and innervation into structured
JSON. **That is sitting unused** — it is the most mechanical win available.

### 5. `layer` — 41 of 77 appendicular muscles (53%)

The 36 without it are mostly muscles no source in `papers/` assigns to a
superficial or deep layer. Filling them means either finding a source that does,
or accepting that the four-cell classification of Mansuit & Herrel (2021) simply
does not resolve every muscle. **The honest answer may be that this stays
partial**, and the hierarchy view should keep its "layer not assigned" bucket.

### 6. Muscle architecture — no field exists

PCSA, fascicle length, pennation, mass fraction. Sources already in `papers/`:
Allen et al. (2014), Ercoli et al. (2014), Fahn-Lai et al. (2020). Mansuit &
Herrel (2021) names the rest (Huby et al. 2021 for *Latimeria*; Dick & Clemente
2016 and Cieri et al. 2020 for varanids; Payne et al. 2005 for horse).

This is roadmap phase 5 and is genuinely additive rather than blocking.

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

1. **Diogo et al. (2016) SI download** — one action, six taxa, unblocks the
   fin-to-limb attachment story.
2. **Run the Werneburg extractor into records** — mechanical, closes much of the
   cranial gap, script already written.
3. **Phase 3** — no new data needed.
4. **Phase 5** — additive, sources mostly in hand.
5. **Phase 4**, scoped to pectoral/arm first.
