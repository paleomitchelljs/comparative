# Coverage and gaps

Measured, not estimated. Regenerate with `python3 scripts/export_matrix.py`.

**State:** 95 muscles · 560 occurrences · 188 skeletal elements · 55 sources · 16 taxa.

Every PDF in `papers/` has a `sources.json` entry, including two declared out of
scope. Duplicates are removed as they are found.

---

## 1. Underreported body regions

`%att` is the share of present occurrences carrying taxon-specific attachments —
the number that decides whether attachment change is analysable or merely
illustrated.

| Region | Occurrences | With attachments | %att | Two passes ago |
|---|---:|---:|---:|---:|
| fin | 32 | 13 | 41% | 41% |
| pectoral | 96 | 36 | 38% | 38% |
| arm | 33 | 9 | 27% | 27% |
| **foot** | 12 | 3 | **25%** | 0% |
| pelvic | 33 | 8 | 24% | 24% |
| cranial | 60 | 10 | 17% | 17% |
| **thigh** | 36 | 6 | **17%** | 14% |
| **leg** | 27 | 4 | **15%** | 0% |
| **hand** | 59 | 7 | **12%** | 0% |
| forearm | 94 | 7 | 7% | 6% |
| **axial** | 20 | 0 | **0%** | — |

Overall 21%, from 17%. Architecture records 10, from 4.

**The autopod is half fixed.** Blotto et al. (2020) has now been mined: the hand
went 0% → 12%, the foot 0% → 25%, and Anura as a whole 7% → 25%. That work also
added nine anuran autopod elements the ontology lacked — prepollex, prehallux,
distal carpal 3-4-5, radiale, element Y, tibiale, fibulare, ligamentum calcanei,
aponeurosis plantaris — and three anuran occurrence rows for pes muscles that had
no anuran record at all.

The **prepollex** is worth singling out. Anurans lost digit 1, and the preaxial
muscles that would serve it — adductor pollicis, a contrahens, flexores breves
profundi slips — attach to the prepollex instead. That is the position-versus-
identity argument with a bone attached to it rather than just a digit number.

**What Blotto does not fix:** the leg (zeugopod) is still 0%, and the hand
remains low because Blotto covers Anura only — the other eight tetrapod columns
still inherit the consensus. The forearm at 7% is the largest region with the
least attachment detail.

**Axial is newly present but skeletal.** Three records (epaxial, hypaxial,
caudal) from Schilling (2011), covering the division that everything else is
built on. They are deliberately coarse: Schilling reviews tracts, not individual
muscles. Splitting the transversospinal system, longissimus and iliocostalis into
separate records is the obvious next step, with Cieri (2018) for the squamate
column.

## 2. Underreported taxonomic groups

| Taxon | Occurrences | With attachments | Regions covered | Missing regions |
|---|---:|---:|---:|---|
| Dipnoi | 7 | 7 (100%) | 1 | everything but fin |
| Actinistia | 7 | 6 (86%) | 1 | everything but fin |
| Synapsida (stem) | 4 | 2 (50%) | 1 | all but thigh |
| Monotremata | 7 | 3 (43%) | 1 | all but pectoral |
| Crocodylia | 55 | 14 (25%) | 8 | cranial, fin, foot |
| Testudines | 50 | 12 (24%) | 6 | axial, fin, thigh, leg, foot |
| Lepidosauria | 76 | 13 (17%) | 10 | fin |
| Theria | 73 | 12 (16%) | 10 | fin |
| Caudata | 66 | 7 (11%) | **11 (all)** | — |
| Aves | 54 | 6 (11%) | 9 | fin, foot |
| Anura | 56 | 4 (7%) | 9 | fin, foot |
| Chondrichthyes | 19 | 1 (5%) | 4 | most appendicular |
| Actinopterygii | 12 | 0 (0%) | 4 | most appendicular |
| Tetrapodomorpha (stem) | 7 | 0 (0%) | 2 | most |
| Petromyzontida | 5 | 0 (0%) | 2 | most |
| Myxini | 1 | 0 (0%) | 1 | most |

Two different kinds of thin:

**Deep but narrow** — Dipnoi, Actinistia, Monotremata, stem synapsids have
excellent attachment coverage over very few muscles. They are single-region
columns, which is honest: those sources covered one appendage.

**Broad but shallow** — Caudata covers all eleven regions but only 11% of its
occurrences carry attachments. Anura and Aves are similar. These are the columns
where the muscle *roster* is good and the attachment detail is not.

**Genuinely underreported:** Actinopterygii (12 occurrences, 0 attachments) is
the weakest column with a real literature behind it. *Polypterus* appendicular
attachments are not in the Diogo et al. supplementary the way the sarcopterygian
ones are, and Winterbottom (1973) — a 93-page teleost synonymy, still unmined —
would at least fix the naming. Myxini and Petromyzontida are thin by nature
(1 and 5 occurrences) and will stay that way.

## 3. Is the skeletal mapping keeping pace?

Partly. The element *inventory* is healthy; the *resolution* is the weak link.

| | |
|---|---|
| Elements | 167, of which 134 (80%) carry at least one muscle attachment |
| Attachment rows | 597 |
| Rows naming a **landmark** | 100 (**17%**, up from 11% this pass) |
| Rows naming a **side** | 182 (30%) |
| Osteological correlates | 53 flagged, 44 (83%) carry a muscle |

**What was wrong and is now fixed.** An audit found 28 rows whose own
`origin`/`insertion` prose named a landmark — "olecranon", "fourth trochanter",
"radial tuberosity" — while the structured row recorded only the parent bone.
That was captured information that never reached structure, and it is exactly
the difference between "attaches to the humerus" and "attaches to the
deltopectoral crest". `scripts/promote_landmarks.py` promotes them, refusing
relative references ("distal *to* the deltopectoral crest" locates a muscle by a
landmark it does not touch) and cross-taxon disjunctions.

**What is still wrong.** 44 muscles attach only to group-level elements with no
landmark — most of the cranial and fin records. Nine osteological correlates
carry no muscle at all: scapular spine, coronoid process of ulna, lesser
trochanter, linea aspera, tibial tuberosity, pectoral articular process, maxilla,
pygostyle, urostyle. Those are landmarks a palaeontologist would look at first,
and the dataset currently says nothing about what pulls on them.

**Elements per muscle, by region** — a rough parity check:

| Region | Muscles | Elements | Ratio |
|---|---:|---:|---:|
| axial | 3 | 25 | 8.3 |
| cranial | 15 | 60 | 4.0 |
| pelvic | 5 | 11 | 2.2 |
| pectoral | 16 | 22 | 1.4 |
| hindlimb | 17 | 19 | 1.1 |
| forelimb | 32 | 26 | 0.8 |
| fin | 7 | 4 | 0.6 |

The forelimb and fin are the two places where the skeleton is thinner than the
musculature it has to support. The fin especially: four elements (radials, rays,
axial elements, preaxial radials) carrying seven muscles across four taxa, when
Diogo et al. distinguish individual axial elements and named radial series. Fin
skeletal detail is the correlate of the fin muscle detail already recorded.

---

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

## Mined this pass

| Source | What it gave |
|---|---|
| **Blotto et al. (2020)** | Anuran hand and foot; 9 autopod elements incl. prepollex/prehallux; hand 0→12%, foot 0→25% |
| **Dick & Clemente (2016)** | Varanid hindlimb attachments from their Table 1; **leg 0→15%**, thigh 14→17% |
| **Hudson et al. (2011) hindlimb** | Cheetah hindlimb architecture for 6 muscles — mass, fascicle length, PCSA |
| **Hattori & Tsuihiji (2021)** | Pedal homology and osteological correlates; fetched from Europe PMC, no local PDF |

### One substantive homology change

Hattori & Tsuihiji (2021) propose that the classical homologies of the anterior
tibial muscles are **swapped**: avian *m. tibialis cranialis* is the homologue of
the non-avian *m. extensor digitorum longus*, and avian *EDL* of the non-avian
*m. tibialis anterior*. Their argument is that this requires no drastic change in
attachment sites, whereas the classical scheme — descending from Romer (1923-27)
and, they note, used uncritically by palaeontologists for a century — does.

Both `tibialis-anterior` and `extensor-digitorum-longus-hl` are now marked
`contested`, with the avian rows scored `uncertain` rather than picking a side.

Worth flagging a methodological disagreement this creates: Hattori & Tsuihiji
weight morphological and functional congruence **over innervation**, on the
grounds that nerve-muscle specificity is itself variable across taxa. That is the
reverse of the priority used elsewhere in this dataset. Both positions are
defensible and the dataset now holds both.

## What is still unmined in `papers/`

| Source | Would fix |
|---|---|
| **Winterbottom (1973)**, 93 pp | Teleost muscle synonymy; the actinopterygian naming gap |
| **Leavey et al. (2024)**, **Přikryl et al. (2009)** | Anuran pelvis and hindlimb detail |
| **Schreiweis (1982)** | Penguin appendicular myology |
| **Cieri (2018)** | Squamate axial detail, to split the coarse axial records |
| Werneburg & Maier (2019), Werneburg & Preuschoft (2024), Gai et al. (2022), Miyashita (2016), Clack et al. (2016), Higashiyama et al. (2016) | Cranial detail and the spiracular/ear sequence |
| Demuth et al. (2022) | Method for 3D muscle volumes from skeletal geometry — read before phase 4 |

## Roadmap position

Phases 1–3 done. Phase 5 (architecture) has a working pipeline and four records;
extending it is data entry from papers in hand. Phase 4 (the diagram) should
still be scoped to pectoral, arm and fin — the three regions above 25%
attachment coverage — until the autopod is filled.
