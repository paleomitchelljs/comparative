# Coverage and gaps

Measured, not estimated. Regenerate with `python3 scripts/export_matrix.py`.

**State:** 126 muscles · 517 present occurrences · 212 skeletal elements · 59 sources · 16 taxa.

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
| **foot** | 11 | 26 | 19 | **73%** |
| fin | 9 | 35 | 19 | 54% |
| leg | 10 | 33 | 15 | 45% |
| pelvic | 8 | 37 | 14 | 38% |
| thigh | 10 | 45 | 17 | 38% |
| pectoral | 16 | 119 | 38 | 32% |
| arm | 5 | 36 | 10 | 28% |
| axial | 15 | 47 | 11 | 23% |
| hand | 9 | 61 | 11 | 18% |
| cranial | 15 | 62 | 11 | 18% |
| **forearm** | 18 | 118 | 16 | **14%** |

Overall 34%. Landmark resolution 14% of rows. Correlates carrying a muscle 78%.
Architecture records 21 across two taxa.

**The autopod is no longer the hole — the forearm is.** Walthall & Ashley-Ross
(2006) took the foot from 40% to 73% and the leg from 30% to 45% in one pass, and
created eleven pedal records where there had been three. The forearm at 14% across
118 occurrences is now the largest region with the least attachment detail, and it
is the one place where the salamander column is nearly complete while every other
tetrapod column still inherits the consensus.

Axial is no longer 0%: the body wall now has the rectus abdominis, the three
oblique layers and the ypsiloideus scored for Caudata, alongside the three coarse
tract records from Schilling (2011).

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
| **Caudata** | 88 | 61 | **69%** |
| Synapsida (stem) | 4 | 2 | 50% |
| Actinopterygii | 14 | 6 | 43% |
| Monotremata | 7 | 3 | 43% |
| Crocodylia | 66 | 24 | 36% |
| Lepidosauria | 87 | 25 | 29% |
| Testudines | 50 | 13 | 26% |
| Anura | 62 | 14 | 23% |
| Theria | 81 | 12 | 15% |
| Aves | 55 | 7 | 13% |
| Chondrichthyes | 19 | 1 | 5% |
| **Tetrapodomorpha (stem)** | 7 | **0** | **0%** |
| Petromyzontida | 5 | 0 | 0% |
| Myxini | 1 | 0 | 0% |

**Caudata was the anomaly and is now the reference column.** It went from 11% to
69% on Walthall & Ashley-Ross (2006), which states an origin and an insertion for
every postcranial muscle it describes. Because Caudata is the taxon this dataset
uses for the plesiomorphic tetrapod condition, the consensus rows that every other
tetrapod column inherits are now anchored to a scored column rather than to a
composite. It is also the only taxon whose body wall is scored.

**Theria at 15% and Aves at 13%** are now the broad-but-shallow columns, and both
have architecture data but little attachment structure. Chondrichthyes at 5% is
the sharpest gap at the fish end.

**Tetrapodomorpha (stem) at 0%** is the fossil column, and its attachments would
have to come from osteological correlates rather than dissection — Molnar et al.
(2018) Tables S1-S6 are the source, still unfetched.

## 3. Is the skeletal mapping keeping pace?

Partly. The element *inventory* is healthy; the *resolution* is the weak link.

| | |
|---|---|
| Elements | 212, of which 173 (82%) carry at least one muscle attachment |
| Attachment rows | 930 |
| Rows naming a **landmark** | 130 (14%) |
| Rows naming a **side** | 316 (**34%**) |
| Osteological correlates | 80 flagged, 62 (78%) carry a muscle |

**What was wrong and is now fixed.** An audit found 28 rows whose own
`origin`/`insertion` prose named a landmark — "olecranon", "fourth trochanter",
"radial tuberosity" — while the structured row recorded only the parent bone.
That was captured information that never reached structure, and it is exactly
the difference between "attaches to the humerus" and "attaches to the
deltopectoral crest". `scripts/promote_landmarks.py` promotes them, refusing
relative references ("distal *to* the deltopectoral crest" locates a muscle by a
landmark it does not touch) and cross-taxon disjunctions.

**What is still wrong.** Three muscles attach only to group-level elements with no
landmark. Eighteen osteological correlates carry no muscle at all: scapular spine,
coronoid process of ulna, lesser trochanter, trochanteric fossa, linea aspera,
tibial tuberosity, pectoral articular process, maxilla, pygostyle, urostyle,
tibiotarsus, cranial and lateral cnemial crests, fossa metatarsi I, Meckelian
fossa, epipterygoid, basipterygoid process, temporal bar. Those are landmarks a
palaeontologist would look at first, and the dataset currently says nothing about
what pulls on them. The count rose because recent passes added correlates faster
than they added the muscles that use them.

**Side resolution overtook landmark resolution this pass** — 34% of rows now name
an aspect, against 14% naming a landmark. Walthall & Ashley-Ross state an aspect
for nearly every attachment ("posterolateral face of the fibula", "internal
(dorsal) face of the pubo-ischiac plate") while rarely naming a named process, so
the salamander column is well resolved on side and poorly on landmark. That is a
property of how salamanders are described, not a defect in the scoring: their
attachments are largely fleshy sheets, which is also why they leave few correlates.

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

**Taxon-specific attachments: 178 of 517 present occurrences (34%).**

Everything else in the roadmap depends on this number. The phylogeny view (phase
3) computes gains and losses from per-taxon records; the diagram (phase 4) draws
per-taxon bands. Both degrade to showing the consensus repeated 16 times if the
occurrences are empty.

It is also the number that decides whether "attachment change is data" is true in
practice. At 34% a computed shift table is analysable for some comparisons and not
others, and the distribution matters more than the total: no region is empty any
longer, but a shift is only computable where **two** taxa are scored for the same
muscle. Caudata at 69% raises the ceiling for every tetrapod comparison, because
it is one end of most of them.

### Where the hole is

| Region | Muscles | Taxon-attachment rows |
|---|---:|---:|
| pectoral | 16 | 38 |
| fin | 9 | 19 |
| foot | 11 | 19 |
| thigh | 10 | 17 |
| forearm | 18 | 16 |
| leg | 10 | 15 |
| pelvic | 8 | 14 |
| axial | 15 | 11 |
| cranial | 15 | 11 |
| hand | 9 | 11 |
| arm | 5 | 10 |

No region is at zero. The distribution is now flat enough that the limiting factor
is no longer which regions are covered but **how many taxa are covered per
muscle** — a shift needs two scored columns, and most muscles have one.

By taxon the picture inverted this pass: the sarcopterygian fish end is complete
but small (Dipnoi 7/7, Actinistia 6/7), while Caudata is now both large and
well-covered (61 of 88). The columns that would make salamander scores comparable
— Anura at 23%, Testudines at 26%, Theria at 15% — are what to fill next.

---

## This pass — Walthall & Ashley-Ross (2006)

One source, the largest single-pass movement in the dataset so far.

| | Before | After |
|---|---:|---:|
| Caudata attachment coverage | 11% | **69%** |
| Overall attachment coverage | 24% | **34%** |
| Muscle records | 108 | 126 |
| Skeletal elements | 205 | 212 |
| foot / leg / axial %att | 40 / 30 / 15 | **73 / 45 / 23** |

Eighteen records were created for muscles the dataset had no row for — mostly
intrinsic pedal muscles whose manual counterparts already existed, plus the
internal oblique, which had been missing between the external oblique and the
transversus. Seven elements were added: the ypsiloid cartilage, trunk and caudal
transverse processes, carpal and tarsal intermedium, tarsal centrale, and the
distal tarsal row.

### Three data-integrity problems this surfaced

Creating the pes records exposed errors that had been invisible while the records
did not exist.

**1. Eight taxon blocks in `seed_occurrence_attachments.py` were never applied.**
The `SEED` dict literal had duplicate muscle-id keys, and in Python a later key
silently overwrites an earlier one. Lost this way: the testudine hypobranchial
block, the Matsuoka & Hasegawa avian sternocoracoideus (the richer of two), three
anuran pedal blocks from Blotto et al., and three varanid hindlimb blocks from
Dick & Clemente. All eight are merged and applied; the seed now writes 110 taxon
blocks where it wrote 102. The failure mode is worth naming because it is silent —
the script reported success every time.

**2. Ten attachment rows named the wrong limb's bones.** Five were consensus rows
on pes muscles pointing at `phalanges-manus`, copied from the forelimb counterpart
when those records were created. The other five were pedal observations parked on
forelimb records — their own notes said "recorded from the FOOT" — because no pes
record existed to hold them. They now sit on the pes records, which means
`abductor-digiti-minimi-pes` and `contrahentium-caput-longum-pes` arrive with two
taxa rather than one.

**3. `contrahentes-digitorum-pes` inserted on the phalanges of the hand.** A
consequence of (2), and the reason the audit was run at all.

A cross-limb check is cheap and worth keeping: no row in a `pelvic`/`thigh`/`leg`/
`foot` muscle should name a forelimb element, and vice versa. The dataset is
currently clean by that test.

### What the source itself contributed beyond rows

- **The pubo-ischiac plate is glossed by the paper as pubis plus ischium**, which
  is what licenses scoring it on two bones instead of inventing a composite
  element and stranding the salamander's pelvic muscles on a bone no other tetrapod
  has.
- **A muscle identified by its insertion alone.** The iliocaudalis is
  indistinguishable from the epaxial muscles except by ending on the ilium.
- **Postaxial position and digit number disagree between the limbs.** The manual
  extensor lateralis digiti IV and the pedal abductor digiti V sit at the same
  margin on differently numbered digits, because the salamander hand has lost digit
  V. Matching by number pairs the manual muscle with nothing.
- **A size trade-off between two muscles of very different span.** The
  femorofibularis crosses only the knee; the ischioflexorius runs pelvis to sole.
  They substitute for one another in size across species and within one species
  across ontogeny, and share a nerve branch.
- **A disagreement recorded rather than resolved.** This paper describes a discrete
  m. opercularis in *Taricha*; Abdala & Diogo (2010) hold the urodele structure to
  be part of the levator scapulae. Presence stays `no` and the note carries both.

### The caveat on this column

Caudata is now scored almost entirely from **one genus**, and the paper's own
comparisons show that several of the characters it reports vary across salamanders
— the iliotibialis head count, the puboischiotibialis inscription, the
ischioflexorius division, the femorofibularis/ischioflexorius size trade-off. The
attachment *sites* are likely general; the muscle *divisions* demonstrably are not.
A second salamander source is the obvious next acquisition.

## Mined in earlier passes

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

Nothing in `papers/` is unmined. Five sources remain uncited in records and are
accounted for above.

The outstanding fetches are external:

| Source | Would fix |
|---|---|
| **Molnar et al. (2018) Tables S1–S6** | Stem-tetrapodomorph attachments — the only route to the 0% fossil column |
| A salamander source other than *Taricha* | Caudata is scored from one genus; the paper's own comparisons show several characters vary across salamanders |
| Anuran, chelonian or therian equivalents of Walthall & Ashley-Ross | The columns that would make the salamander scores comparable |

## Roadmap position

Phases 1–3 done. Phase 5 (architecture) has a working pipeline and 21 records;
extending it is data entry from papers in hand. **Phase 4 (the diagram) can now be
scoped to the whole limb**: foot, fin, leg, pelvic, thigh, pectoral and arm are all
above 28%, and only forearm, hand, cranial and axial sit below 25%. The constraint
on phase 4 is no longer coverage but Leavey et al. (2024) — bone dimensions do not
predict muscle size, so a diagram must not scale muscle bands to skeletal
geometry.
