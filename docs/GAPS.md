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
126 muscle records · 634 present occurrences · 234 skeletal elements · 104 sources · 19 operational taxa
<!-- /counts:headline -->

**Every PDF in `papers/` has a `sources.json` entry, and every entry resolves to a
file.** Both directions are checked; duplicates are removed as they are found.

**A large batch of sources is catalogued but not yet mined.** 33 entries are
uncited in records. Five are the long-standing cases — two declared out of scope
(catfish brain, cardiac review), two methods and framing papers cited in the docs
instead (Demuth et al. 2022, Richardson 2022), one with no muscle-level content
(Huynen et al. 2014, moa *tbx5*). The rest are a recent intake, filed with
`role` and `pdf` set so they can be worked through, and listed in
[§6](#6-catalogued-but-not-yet-mined) with what each would close.

The validator's `never cited` warnings are the worklist. That is the intended
use: a catalogued source is a promise, and the warning is what stops the promise
being forgotten.

---

## 1. Underreported body regions

`%att` is the share of present occurrences carrying taxon-specific attachments —
the number that decides whether attachment change is analysable or merely
illustrated.

<!-- counts:regions -->
| Region | Muscles | Present occurrences | Scored | %att |
|---|---:|---:|---:|---:|
| foot | 11 | 27 | 22 | 81% |
| leg | 10 | 36 | 28 | 78% |
| thigh | 10 | 48 | 37 | 77% |
| pectoral | 16 | 128 | 88 | 69% |
| arm | 5 | 51 | 34 | 67% |
| fin | 9 | 39 | 23 | 59% |
| pelvic | 8 | 39 | 23 | 59% |
| cranial | 15 | 59 | 33 | 56% |
| forearm | 18 | 116 | 64 | 55% |
| axial | 15 | 29 | 14 | 48% |
| hand | 9 | 62 | 29 | 47% |
| **all** | 126 | 634 | 395 | **62%** |
<!-- /counts:regions -->

**Cranial was the hole and is climbing.** It sat under 20% for several passes with
the head barely scored in any taxon. Huber et al. (2011) took the shark's six
muscles, and Jones et al. (2019) then took the whole avian jaw, throat and orbit
from a contrast-CT digital dissection of one *Columba livia* — ten rows, 33 named
parts. Ziermann & Diogo (2013) then took the axolotl, seven rows and the only larval
*and* adult attachments in the corpus. Cranial is now 56%, up from under 20%.

**Hand is the floor now, at 47%, and the forearm and hand still carry the two
largest occurrence counts in the dataset**, so they remain the biggest absolute
gap. Nothing in `papers/` fixes them across taxa at once; it goes one column at a
time. Meers (2003) is the largest single remaining bite — crocodylian forelimb, and
the one naming scheme from Abdala & Diogo's Tables 1-3 not yet held in full. For
the cranial region what is left is Dearden et al. (2020) for Chondrichthyes, Bauer
(1997) for the urodele jaw openers — specifically the ceratomandibularis, which
Ziermann & Diogo report as variable across urodeles — and Anderson (2008) as a
cross-check across all of them. **The
mammalian head remains the one column with no source at all.**

The **prepollex** is worth singling out. Anurans lost digit 1, and the preaxial
muscles that would serve it — adductor pollicis, a contrahens, flexores breves
profundi slips — attach to the prepollex instead. That is the position-versus-
identity argument with a bone attached to it rather than just a digit number.

**Axial is no longer the empty region, and it is now 17 rows shorter.** The body
wall carries the rectus abdominis, the three oblique layers and the ypsiloideus
scored for Caudata, and the tracts are scored for *Varanus exanthematicus* from
Cieri (2018). What left were the Schilling (2011) rows for taxa he does not
examine — the crocodylian, avian, actinopterygian and cheetah rows were his
Figure 1, a cladogram synthesis with no animal behind it. Seven of his rows
stayed, re-attributed to the animals his Figures 2 and 3 actually show:
*Myxine glutinosa*, *Etmopterus spinax*, *Ambystoma tigrinum*, *Microtus
arvalis*, *Canis familiaris*. See [§7](#7-the-base-layer-species-and-source).

**The crocodylian and avian axial columns are now empty, and that is a source
gap, not a coverage regression.** Nothing in `papers/` describes crocodylian trunk
musculature; Boumans et al. (2015) covers the avian *neck* and would be the way
back in for Aves.

## 2. Underreported taxonomic groups

<!-- counts:taxa -->
| Taxon | Present occurrences | Scored | %att |
|---|---:|---:|---:|
| Dipnoi | 7 | 7 | 100% |
| Pseudosuchia (stem) | 1 | 1 | 100% |
| Crocodylomorpha (stem) | 3 | 3 | 100% |
| Crocodyliformes (stem) | 7 | 7 | 100% |
| Theria | 64 | 55 | 86% |
| Actinistia | 7 | 6 | 86% |
| Crocodylia | 60 | 48 | 80% |
| Tetrapodomorpha (stem) | 42 | 33 | 79% |
| Caudata | 90 | 68 | 76% |
| Lepidosauria | 105 | 67 | 64% |
| Synapsida (stem) | 4 | 2 | 50% |
| Aves | 79 | 39 | 49% |
| Actinopterygii | 13 | 6 | 46% |
| Anura | 70 | 30 | 43% |
| Monotremata | 7 | 3 | 43% |
| Chondrichthyes | 19 | 7 | 37% |
| Testudines | 50 | 13 | 26% |
| Myxini | 3 | 0 | 0% |
| Petromyzontida | 3 | 0 | 0% |
<!-- /counts:taxa -->

**Caudata was the anomaly and is now the reference column.** It went from 11% to
69% on Walthall & Ashley-Ross (2006), which states an origin and an insertion for
every postcranial muscle it describes. Because Caudata is the taxon this dataset
uses for the plesiomorphic tetrapod condition, the consensus rows that every other
tetrapod column inherits are now anchored to a scored column rather than to a
composite. It is also the only taxon whose body wall is scored.

**Aves is no longer the broad-but-shallow column.** It was 13% with architecture
data and almost no attachment structure; it is now 49% on two passes and five
species. McKitrick (1991) supplied the loon forelimb and Jones et al. (2019) the
pigeon head, and between them they answer the objection recorded below — that the
avian sources were either synonymy tables or the wrong kind of animal. Both are
single-specimen descriptive works, which is what the column needed.

**Chondrichthyes at 37% is now the sharpest gap at the fish end**, and the one a
single source could most change: Dearden et al. (2020) covers both an elasmobranch
and a holocephalan, and Didier (1987) is a holocephalan myology thesis.

**Theria was the largest gap and is now level with Caudata at 69%.** Ercoli et al.
(2012) took it from 15% to 38% across the hindlimb, lumbar region and tail; Ercoli
et al. (2014) then took it to 69% across the forelimb. The second of those needed
no new source — 25 Theria occurrences already cited that paper for their *names*
and had no `attachments` block, which is worth stating as a general lesson: a
source counting as "mined" because it is cited is not the same as a source mined
for everything it holds.

**Theria now reads 86%, and the jump is a deletion.** Its cranial column is
*gone* — all ten therian cranial rows were guessed onto *Acinonyx jubatus*, an
animal in this corpus because Hudson et al. measured a cheetah's limbs, and
sourced to reviews that dissect no mammal. **No source in `papers/` describes a
mammalian head.** That is the single clearest acquisition need in the dataset: a
therian cranial myology would restore ten rows and the arch-identity teaching
cases that go with them. The percentage rose because unscored rows left, which is
worth remembering whenever a column improves without a paper being read.

**Aves at 13% is source-limited, not effort-limited, and the limit is real.**
Thirty of its 48 unscored rows cite only Abdala & Diogo (2010), whose Tables 1-3
are synonymy tables — name against name across six taxa — with 36 origin or
insertion mentions in 38 pages. It settles what a muscle is called, not where it
attaches. The avian sources that *are* descriptive do not fit the column:
Schreiweis (1982) is a penguin, whose flipper contradicts this taxon's stated
exemplars (*Gallus*, *Cairina*, *Coturnix*); Ghetie et al. (1976) is a
Latin-labelled plate atlas; Matsuoka & Hasegawa (2007) is eight pages on a swan
with its attachment data in figure captions.

The avian **hindlimb** rows cite Allen et al. (2021) and Hutchinson et al. (2015),
and both are now in `papers/`. Neither closes them, and it is worth recording why:
Hutchinson et al. is a musculoskeletal model whose attachments are digitised 3D
coordinates rather than prose, and its **architecture table is already fully
entered** — the eleven avian `architecture` blocks are its Table 2. Allen et al.
is a moment-arm study whose contribution here, the crocodylian-to-avian homology
table, is already carried in the occurrence names. A source can be cited, fully
mined, and still leave a row unscored, because what it holds is not an attachment.

**This is now fixed at the source.** `papers/` has since gained Fisher & Goodman
(1955), a complete myology of the whooping crane running to 156 pages with an
explicit `Origin.—` and `Insertion.—` for every muscle; Widrig et al. (2023) on
tinamou pectoral morphology in 3D; and McKitrick (1991) on the loon forelimb. A
crane is a flying neognath, far closer to this taxon's exemplars than a penguin,
and between the three the column has a neognath, a palaeognath and a
foot-propelled diver. Aves is no longer source-limited — it is simply unmined,
and it is the largest remaining gap in the dataset.

Fisher & Goodman is a scan with OCRed text, so it needs checking against the
plates as it is worked through.

**Lepidosauria moved 29% to 53%** on Zaaf et al. (1999), whose tables state an
origin and an insertion for every fore- and hindlimb muscle in two gecko species.
Those rows are *Eublepharis macularius*, with the *Gekko gecko* differences in
`attachmentNote` — and four of those differences are a different bone rather than
a different part of one, which is the sharpest available warning against reading
any single lizard as the clade.

**Tetrapodomorpha (stem) moved 0% to 79%**, and it is the one column where the
attachments are osteological correlates rather than dissection. Molnar et al.
(2018) §III describes them taxon by taxon, which is what let the column go from
seven occurrences on one species to 42 across four: *Eusthenopteron foordi*,
*Tiktaalik roseae*, *Acanthostega gunnari* and *Ossinodus pueri*. Read the
percentage with that in mind — a scored row here is an inference from a scar, and
six rows are `uncertain` precisely because the source declines to call the muscle
separate.

## 3. Is the skeletal mapping keeping pace?

Partly. The element *inventory* is healthy; the *resolution* is the weak link.

<!-- counts:skeleton -->
| | |
|---|---|
| Elements | 234, of which 201 (86%) carry at least one attachment |
| Observed attachment rows | 1036 |
| Rows naming a **landmark** | 235 (23%) |
| Rows naming a **side** | 600 (58%) |
| Osteological correlates | 97 flagged, 81 carry a muscle |
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
| cranial | 21 | 57 | 2.7 |
| hindlimb | 42 | 38 | 0.9 |
| axial | 33 | 26 | 0.8 |
| pectoral | 32 | 24 | 0.8 |
| forelimb | 51 | 37 | 0.7 |
| fin | 8 | 5 | 0.6 |
| pelvic | 26 | 14 | 0.5 |
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
**Taxon-specific attachments: 395 of 634 present occurrences (62%).**
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
| pectoral | 16 | 210 |
| forearm | 18 | 161 |
| cranial | 15 | 127 |
| thigh | 10 | 104 |
| leg | 10 | 77 |
| hand | 9 | 75 |
| arm | 5 | 72 |
| foot | 11 | 63 |
| fin | 9 | 57 |
| pelvic | 8 | 54 |
| axial | 15 | 36 |
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
| **Fisher & Goodman (1955)** | The avian column entire — but the scan is uneven: 83 of ~328 headings have a recoverable Origin paragraph, and plate-facing pages OCR to noise. Page-by-page work |
| **Pereyra et al. (2019)** | NOT rows. Sharpey's fibre orientation at turtle pectoral attachments, in three classified patterns — evidence for what `correlate` asserts, and the way into §3's 18 unused correlates |
| **Westphal et al. (2019)** | Amphisbaenian pectoral: all 17 shoulder muscles retained under any degree of limb reduction, with insertions shifting to connective tissue while origins stay put |
| **Martins et al. (2019)** | Threadsnake head and neck, 18 species. Miniaturised burrowers — best for what varies within Squamata, not as a lepidosaur stand-in |
| **Boumans et al. (2015)** | Barn owl cervical muscles, origin and insertion tabulated across 14 vertebrae |
| **Vélez-García et al. (2023)** | Kinkajou shoulder and brachium — the second caniform against Galictis, which is what would show whether the therian forelimb rows are therian or mustelid |
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

> The per-source worklist, with a density check that predicts whether a paper
> will actually yield rows, is in [`MINING.md`](MINING.md).

## 6. Catalogued but not yet mined

A batch of 29 sources was filed into `papers/` and `sources.json` in one pass and
has not been worked through. Each has `role`, `pdf` and where known a `doi`, so
the question "what is this for" is already answered; what is missing is the
records. Ordered by the gap each would close.

| Source | Would close |
|---|---|
| **Jones et al. (2019)** | Avian cranial muscles from contrast CT. Aves is 13% and has no cranial attachments at all |
| **Ziermann & Diogo (2013)** | Salamander cranial development, including muscles lost at metamorphosis — developmental evidence for the coarsest region |
| **Collings & Richards (2019)** | Anuran pelvis and hindlimb, attachment-level, in a walking rather than jumping frog |
| **Dearden et al. (2020)** | Chondrichthyan cranial muscles, elasmobranch *and* holocephalan. Chondrichthyes is the thinnest column at 5% |
| **Huber et al. (2011)** | Reference summary for the same gap |
| **Anderson (2008)** | Cranial nomenclature reconciled across gnathostomes — a whole-region cross-check rather than new rows |
| **Diogo & Abdala (2007); Diogo (2008)** | The osteichthyan half of the pectoral and cranial homology arguments the tetrapod records rest on |
| **Cole et al. (2011)** | Developmental origin for the pelvic fin muscles, which the fin records mostly assert topologically |
| **Bauer (1997)** | Urodele jaw openers on CN VII — the half of the salamander cranial series development does not resolve |
| **Wiseman et al. (2021); Cuff et al. (2022)** | Crocodylian and archosaur hindlimb attachment coordinates and muscle-size estimation |
| **Mathou et al. (2023)** | Architecture for the axial column, which has none |
| **O'Reilly et al. (2000); Reilly & White (2003)** | Axial function, and the epipubic bone — a skeletal element the dataset does not carry |
| **Demuth et al. (2023)** | A stem archosaur earlier than any fossil column here |
| **Springer & Johnson (2015); Lemell et al. (2002)** | Branchial and hyobranchial detail, outgroup and functional respectively |
| **Didier (1987); Zhu (2011)** | Holocephalan myology and turtle plastron reduction. Both unpublished theses — check, do not defer to |
| **Schlough; Lőw et al. (2016); OSU Extension (2009); Jacob & Pescatore** | Dissection vocabulary for mustelid, frog, salmonid and chicken, as Campbell (2007) supplied for the rat |
| **Hattori & Tsuihiji (2021)** | Pedal muscles across all four sauropsid clades with osteological correlates named for most. The correlate gap in §3 — 18 flagged sites with no muscle on them — is what this closes, more than it closes rows |
| **Lowie et al. (2018)** | Lizard forelimb flexors. Lepidosauria's forearm is its largest remaining region gap at 8 rows |
| **Sánchez et al. (2019)** | Felid forearm and hand. The therian forelimb is currently scored entirely from a mustelid, and the cat is the animal most labs actually use |
| **Gyambibi & Lemelin (2013); Lemelin & Diogo (2016)** | Primate forearm and hand, quantitative in the first case. Hand is the second-thinnest region at 36% |
| **Diogo et al. (2016, marsupials)** | Whether the therian rows are therian or merely eutherian — the column is scored from placental exemplars throughout |

**Zaaf et al. (1999) is now scored as two species.** Its differences column
records *Gekko gecko* against *Eublepharis macularius* for every fore- and
hindlimb muscle, and a blank in that column is an observation of sameness rather
than a gap — so both geckos carry rows, 21 each. Ten of the pairs disagree, and
two disagree about **which bone**: the extensor carpi ulnaris inserts on the
ulnare in *Eublepharis* and the pisiform in *Gekko*, and the latissimus dorsi
shifts from the dorsal to the lateral humerus. Those were prose in an
`attachmentNote` until species-level scoring gave them somewhere to live.

Mined from this batch so far: **Ercoli et al. (2012)** (19 occurrences, Theria
15% to 38%), **Zaaf et al. (1999)** (21 occurrences, Lepidosauria 29% to 53%),
**Omura et al. (2014)**, **Prikryl et al. (2009)** (8 occurrences, Anura 23% to
35%, plus four new elements), **Meers (2003)** (11 occurrences, Crocodylia 58% to
75%) and **Campbell (2007)**; see the reading notes beside their PDFs. Zaaf et al. also holds the first architecture data for any lepidosaur
(Tables 4-6), which is left unentered pending a schema decision on how to carry
two species with two specimens each.

## 7. The base layer: species and source

**Every mined statement carries a species and a source. Clades, homology
hypotheses and every other generalisation are layers on top of that, never stored
as though they were observations.** The audit that established this found the
sourcing sound — 0 present rows and 0 attachment rows without a citation, 0
occurrences storing a clade — and the species tagging holed:

| | Before | After |
|---|---:|---:|
| `speciesBasis: "note"` — the row's prose names the species | 159 | 181 |
| `source` — a single-species study | 216 | 216 |
| `survey` — a survey with a stated exemplar for the clade | 262 | 262 |
| **`default` — a guess** | **54** | **0** |

The 54 guesses resolved two ways, and which one applied turned entirely on
**whether the cited source examined an animal of that clade**:

**22 re-attributed.** The source names a species and the row pointed at the wrong
one. Schilling (2011)'s hagfish is *Myxine glutinosa*, not a lamprey; his shark is
*Etmopterus spinax*, not a holocephalan; his salamander is *Ambystoma tigrinum*
and his mammals *Microtus arvalis* (Fig. 2) and *Canis familiaris* (Fig. 3).
Naumann et al. (2017) is *Lepisosteus osseus*, not a catfish. Abdala & Diogo
(2010)'s Tables 2–3 add "the mammal *Rattus*" to their six reptile and amphibian
columns. Johnston (2011)'s cartilaginous fish is *Callorhinchus milii*. Four
salamander cranial rows moved from Ziermann & Diogo's 2019 review to their 2013
axolotl paper, which is where the observation is, and an anuran row to that
paper's *Xenopus laevis*.

Each of those rows now names its binomial **in its own prose**, which is
`attribute_species.py`'s first rule, so the fix survives every rebuild and carries
its evidence with it. Five species were added, each with a note on what it is
*not* representative of.

**31 lifted out.** The source is a review that examined no animal of that clade,
so the row asserted an observation nobody made. A clade-level statement is derived
data: it belongs in the record's `consensus`, `synonyms` or `homology.notes`. The
substantive facts moved up — the avian epaxial reduction, the mammalian
ventrovertebral series, the palatoglossus exception, the retractor bulbi's loss in
primates — and 13 orphaned `division`/`parts` blocks moved into
`seed_division.py`'s `EXCLUSIONS` with their reasons. What the rows enumerated is
in `synonyms`, which is what the search index reads, so "masseter" still finds the
adductor mandibulae.

Two consequences worth stating plainly. The therian cranial column and the
crocodylian and avian axial columns are now **empty**, and the percentages in §1
and §2 *rose* because unscored rows left. And the clade-keyed seed tables
(`seed_occurrence_attachments.py`, `seed_division.py`) are the same inversion in
code — they key attachments and subdivisions on a taxon and land them on whichever
row happens to belong to it. They work, but they are the next thing that should be
species-keyed.

Two pseudo-species remain in `species.json`: `teleostei-generalised` (6 rows) and
`amphisbaenia-generalised` (3 rows). Both are clades wearing a species tag.

### What the loon then exposed in the code

Adding *Gavia immer* to records that already had an avian row made the clade keying
fail out loud. `seed_occurrence_attachments.py` built `{clade: row}`, so a clade with
two rows silently kept **whichever came last** — three blocks written for *Gallus*,
the swan and the penguin were handed to the loon, overwrote its attachments, and let
`attribute_species.py` re-derive its species from the wrong prose. The row vanished
from a clean build with no error.

The matcher now requires a clade to hold exactly one row, or the block to name its
`species`, and reports rather than clobbers. Fixing it also showed that Schreiweis's
**penguin** supracoracoideus and subcoracoscapularis rows had been quietly
overwritten by Abdala & Diogo's generic avian block for years, for the same reason.

One shape of the same problem is still open: a single row can carry several sources
that examined **different animals**. The *Gallus* latissimus dorsi cites Abdala &
Diogo, Ghetie et al., Matsuoka & Hasegawa and Schreiweis — a chicken, a domestic-bird
atlas, a swan and a penguin — on one species tag, and its seeded note describes
*Cygnus*. Splitting those is the next base-layer pass.

## What is still unmined outside `papers/`

The outstanding fetches are external:

| Source | Would fix |
|---|---|
| **Molnar et al. (2018) Tables S1–S6** | The per-taxon character scoring. No longer blocking — the fossil column was scored from their §III instead — but the matrices would settle which correlates each fossil actually carries, where the prose reports a node reconstruction rather than a specimen |
| Anuran, chelonian or therian equivalents of Walthall & Ashley-Ross | The columns that would make the salamander scores comparable |

*A salamander source other than* Taricha *is no longer outstanding* — Omura et al.
(2014) supplies it for the trunk, and confirms the concern: the external oblique
and the separability of the rectus abdominis both vary across urodeles.

## Roadmap position

Phases 1–3 done. Phase 5 (architecture) has a working pipeline and 21 records;
extending it is data entry from papers in hand. **Phase 4 (the diagram) can now be
scoped to the whole limb**: foot, fin, leg, pelvic, thigh, pectoral and arm are all
above 28%, and only forearm, hand, cranial and axial sit below 25%. The constraint
on phase 4 is no longer coverage but Leavey et al. (2024) — bone dimensions do not
predict muscle size, so a diagram must not scale muscle bands to skeletal
geometry.
