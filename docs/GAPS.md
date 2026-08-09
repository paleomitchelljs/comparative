# Coverage and gaps

Measured, not estimated. Regenerate with `python3 scripts/export_matrix.py`.

**State:** 108 muscles · 535 present occurrences · 205 skeletal elements · 58 sources · 16 taxa.

**Every source in `papers/` is now mined or accounted for.** Five remain uncited in
records: two declared out of scope (catfish brain, cardiac review), two methods and
framing papers cited in the docs instead (Demuth et al. 2022, Richardson 2022), and
one with no muscle-level content (Huynen et al. 2014, moa *tbx5*).

Every PDF in `papers/` has a `sources.json` entry, including two declared out of
scope. Duplicates are removed as they are found.

---

## 1. Underreported body regions

`%att` is the share of present occurrences carrying taxon-specific attachments —
the number that decides whether attachment change is analysable or merely
illustrated.

| Region | Muscles | Occurrences | With attachments | %att |
|---|---:|---:|---:|---:|
| fin | 9 | 34 | 19 | **56%** |
| foot | 3 | 15 | 6 | 40% |
| pectoral | 16 | 96 | 36 | 38% |
| leg | 7 | 30 | 9 | 30% |
| arm | 5 | 33 | 9 | 27% |
| pelvic | 5 | 33 | 8 | 24% |
| thigh | 8 | 40 | 8 | 20% |
| cranial | 15 | 60 | 10 | 17% |
| axial | 13 | 41 | 6 | 15% |
| hand | 9 | 59 | 8 | 14% |
| **forearm** | 18 | 94 | 7 | **7%** |

Overall 24%. Landmark resolution 15%. Correlates carrying a muscle 76%.
Architecture records 21 across two taxa.

The autopod is no longer the hole — **the forearm is**, at 7% across 94
occurrences, the largest region with the least attachment detail. Axial is 0% by
construction: the three records are whole muscle tracts, not individual muscles.

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

| Taxon | Occurrences | With attachments | %att |
|---|---:|---:|---:|
| Dipnoi | 7 | 7 | **100%** |
| Actinistia | 7 | 6 | 86% |
| Synapsida (stem) | 4 | 2 | 50% |
| Actinopterygii | 14 | 6 | 43% |
| Monotremata | 7 | 3 | 43% |
| Crocodylia | 65 | 24 | 37% |
| Lepidosauria | 87 | 24 | 28% |
| Anura | 60 | 15 | 25% |
| Testudines | 50 | 12 | 24% |
| Theria | 81 | 12 | 15% |
| Aves | 55 | 7 | 13% |
| Caudata | 66 | 7 | 11% |
| Chondrichthyes | 19 | 1 | 5% |
| **Tetrapodomorpha (stem)** | 7 | **0** | **0%** |
| Petromyzontida | 5 | 0 | 0% |
| Myxini | 1 | 0 | 0% |

Actinopterygii is no longer the weak column — Winterbottom (1973) took it from 0
to 43%. **Caudata is now the anomaly**: it covers all eleven regions, the widest
of any taxon, at 11% attachment coverage. It is the reference taxon for the
plesiomorphic tetrapod condition throughout this dataset, and it is among the
thinnest for attachment detail. That is the highest-leverage single column to
improve.

**Theria at 15% and Aves at 13%** are similarly broad-but-shallow, and both have
architecture data but little attachment structure.

**Tetrapodomorpha (stem) at 0%** is the fossil column, and its attachments would
have to come from osteological correlates rather than dissection — Molnar et al.
(2018) Tables S1-S6 are the source, still unfetched.

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

## Fetched from the web this pass

Open-access papers can be pulled by DOI without a local copy. Wiley and PeerJ
block direct fetching, but Europe PMC and PubMed Central serve the full text —
including **green** OA, where the publisher page is paywalled but a repository
copy exists.

| Source | Route | What it gave |
|---|---|---|
| **Hattori & Tsuihiji (2021)** | Europe PMC | Sauropsid pedal homology; contested anterior tibial muscles |
| **Pereyra et al. (2024)** | PMC, green OA | *Caiman* crural and pedal myology in seven layers; **first pedal osteological correlates** for a crocodylian |
| **Allen et al. (2021)** | Europe PMC | Crocodylian↔avian pelvic limb homology table; avian names for 13 records; the iliofibularis |
| **Hutchinson et al. (2015)** | Europe PMC | Ostrich pelvic limb architecture — **first avian architecture data**; 11 records |

Pereyra et al. took Crocodylia from nothing in the leg and foot to 38% overall,
and their fine metatarsal striae are now recorded as correlates. They report that
most correlates vary little between crocodylian species, which is the condition
for using them on fossils.

Allen et al. (2021) supplied avian nomenclature for 13 hindlimb records from
their Table 1, and settled a naming question the dataset had left open — 54 of
55 avian occurrences are now named. They also **corroborate the contested
anterior tibial homology**: they equate the crocodylian extensor digitorum longus
with the avian *m. tibialis cranialis*, which is Hattori & Tsuihiji's reading
rather than the classical one. The two papers work on different problems —
homology versus moment arms — so the agreement is not circular. The records stay
`contested`, but the balance of evidence has moved.

Their method is also the template for roadmap phase 4: fit geometric primitives
to joints, trace muscle paths from origin to insertion, compute moment arms. That
is precisely what this dataset's attachment records are for, and it is what makes
`side` and `landmark` resolution worth chasing rather than decorative.

## What is still unmined in `papers/`

| Source | Would fix |
|---|---|
| **Leavey et al. (2024)**, **Přikryl et al. (2009)** | Anuran pelvis and hindlimb detail |
| **Schreiweis (1982)** | Penguin appendicular myology |
| Werneburg & Maier (2019), Werneburg & Preuschoft (2024), Gai et al. (2022), Miyashita (2016), Clack et al. (2016), Higashiyama et al. (2016) | Cranial detail and the spiracular/ear sequence |
| Demuth et al. (2022) | Method for 3D muscle volumes from skeletal geometry — read before phase 4 |

## Roadmap position

Phases 1–3 done. Phase 5 (architecture) has a working pipeline and four records;
extending it is data entry from papers in hand. Phase 4 (the diagram) should
still be scoped to pectoral, arm and fin — the three regions above 25%
attachment coverage — until the autopod is filled.
