# Coverage and gaps

Measured, not estimated. Every figure between `<!-- counts:… -->` markers is
generated — **run `python3 scripts/doc_counts.py --write` after touching
`data/`**, and never edit those numbers by hand. The prose around them is
curated and the script leaves it alone.

A present occurrence is one whose `present` is not `no`, so `variable`,
`uncertain` and `inferred` count. The resolution figures are over **observed**
attachment rows only: a consensus row is one row inherited by up to nineteen
taxa, and counting it once per taxon inflated `side` and `landmark` coverage in
earlier passes.

**State:**

<!-- counts:headline -->
126 muscle records · 571 present occurrences · 214 skeletal elements · 62 sources · 19 operational taxa
<!-- /counts:headline -->

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

<!-- counts:regions -->
| Region | Muscles | Present occurrences | Scored | %att |
|---|---:|---:|---:|---:|
| foot | 11 | 26 | 19 | 73% |
| fin | 9 | 34 | 19 | 56% |
| arm | 5 | 38 | 20 | 53% |
| leg | 10 | 33 | 15 | 45% |
| pelvic | 8 | 39 | 17 | 44% |
| thigh | 10 | 44 | 19 | 43% |
| pectoral | 16 | 96 | 41 | 43% |
| forearm | 18 | 96 | 23 | 24% |
| axial | 15 | 46 | 11 | 24% |
| hand | 9 | 59 | 11 | 19% |
| cranial | 15 | 60 | 11 | 18% |
| **all** | 126 | 571 | 206 | **36%** |
<!-- /counts:regions -->

**The forearm and the hand are the holes now.** Walthall & Ashley-Ross (2006)
took the foot to 73% and the leg to 45% in one pass, and Blotto et al. (2020)
opened the anuran autopod, but the forearm and hand still sit at the bottom of
the table across the largest occurrence counts in the dataset. Both are places
where the salamander column is nearly complete and every other tetrapod column
inherits the consensus.

The **prepollex** is worth singling out. Anurans lost digit 1, and the preaxial
muscles that would serve it — adductor pollicis, a contrahens, flexores breves
profundi slips — attach to the prepollex instead. That is the position-versus-
identity argument with a bone attached to it rather than just a digit number.

**Axial is no longer the empty region.** The body wall now carries the rectus
abdominis, the three oblique layers and the ypsiloideus scored for Caudata,
alongside the coarse tract records from Schilling (2011), who reviews tracts
rather than individual muscles. Splitting the transversospinal system,
longissimus and iliocostalis into separate records is the next step, with Cieri
(2018) for the squamate column.

## 2. Underreported taxonomic groups

<!-- counts:taxa -->
| Taxon | Present occurrences | Scored | %att |
|---|---:|---:|---:|
| Dipnoi | 7 | 7 | 100% |
| Pseudosuchia (stem) | 1 | 1 | 100% |
| Crocodylomorpha (stem) | 3 | 3 | 100% |
| Crocodyliformes (stem) | 7 | 7 | 100% |
| Actinistia | 7 | 6 | 86% |
| Caudata | 88 | 61 | 69% |
| Crocodylia | 66 | 38 | 58% |
| Synapsida (stem) | 4 | 2 | 50% |
| Actinopterygii | 14 | 6 | 43% |
| Monotremata | 7 | 3 | 43% |
| Lepidosauria | 87 | 25 | 29% |
| Testudines | 50 | 13 | 26% |
| Anura | 62 | 14 | 23% |
| Theria | 81 | 12 | 15% |
| Aves | 55 | 7 | 13% |
| Chondrichthyes | 19 | 1 | 5% |
| Myxini | 1 | 0 | 0% |
| Petromyzontida | 5 | 0 | 0% |
| Tetrapodomorpha (stem) | 7 | 0 | 0% |
<!-- /counts:taxa -->

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

<!-- counts:skeleton -->
| | |
|---|---|
| Elements | 214, of which 175 (82%) carry at least one attachment |
| Observed attachment rows | 549 |
| Rows naming a **landmark** | 107 (19%) |
| Rows naming a **side** | 273 (50%) |
| Osteological correlates | 82 flagged, 64 carry a muscle |
<!-- /counts:skeleton -->

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

**Side resolution runs well ahead of landmark resolution.** Walthall &
Ashley-Ross state an aspect for nearly every attachment ("posterolateral face of the fibula", "internal
(dorsal) face of the pubo-ischiac plate") while rarely naming a named process, so
the salamander column is well resolved on side and poorly on landmark. That is a
property of how salamanders are described, not a defect in the scoring: their
attachments are largely fleshy sheets, which is also why they leave few correlates.

**Elements per muscle, by region** — a rough parity check:

<!-- counts:parity -->
| Region | Muscles | Elements | Elements per muscle |
|---|---:|---:|---:|
| cranial | 21 | 51 | 2.4 |
| hindlimb | 42 | 33 | 0.8 |
| axial | 31 | 24 | 0.8 |
| pectoral | 32 | 21 | 0.7 |
| fin | 8 | 5 | 0.6 |
| forelimb | 51 | 29 | 0.6 |
| pelvic | 25 | 12 | 0.5 |
<!-- /counts:parity -->

The pelvis, fin and forelimb are where the skeleton is thinnest relative to the
musculature hung off it. The fin especially: radials, rays, axial elements and
preaxial radials, carrying every fin muscle in the dataset, when Diogo et al.
distinguish individual axial elements and named radial series. Fin skeletal
detail is the correlate of the fin muscle detail already recorded. Cranial runs
the other way at 2.4 elements per muscle, which is what a coarse adductor
mandibulae complex sitting over a finely divided skull looks like.

---

Every PDF in `papers/` now has a `sources.json` entry. Five were byte-identical
duplicates; two are declared out of scope (a catfish brain, a review of cardiac
evolution) and are listed only so the folder is fully accounted for. The fifth
duplicate had also produced two `sources.json` entries under one `key`, which
the app resolves by letting the later one win — so the bibliography quietly
showed the entry with no reading notes. `validate.py` now rejects a repeated
key.

---

## The one gap that blocks everything downstream

<!-- counts:scored -->
**Taxon-specific attachments: 206 of 571 present occurrences (36%).**
<!-- /counts:scored -->

Everything else in the roadmap depends on this number. The phylogeny view (phase
3) computes gains and losses from per-taxon records; the diagram (phase 4) draws
per-taxon bands. Both degrade to showing the consensus repeated 19 times if the
occurrences are empty.

It is also the number that decides whether "attachment change is data" is true
in practice. At this level a computed shift table is analysable for some
comparisons and not others, and the distribution matters more than the total: no
region is empty any longer, but a shift is only computable where **two** taxa
are scored for the same muscle. Caudata at 69% raises the ceiling for every tetrapod comparison, because
it is one end of most of them.

### Where the hole is

<!-- counts:holes -->
| Region | Muscles | Observed attachment rows |
|---|---:|---:|
| pectoral | 16 | 109 |
| forearm | 18 | 63 |
| foot | 11 | 56 |
| cranial | 15 | 55 |
| fin | 9 | 51 |
| thigh | 10 | 44 |
| arm | 5 | 42 |
| leg | 10 | 41 |
| pelvic | 8 | 35 |
| hand | 9 | 28 |
| axial | 15 | 25 |
<!-- /counts:holes -->

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
