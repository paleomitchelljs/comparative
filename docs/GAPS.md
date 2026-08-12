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
128 muscle records · 740 present occurrences · 253 skeletal elements · 104 sources · 19 operational taxa
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
| leg | 10 | 34 | 28 | 82% |
| thigh | 10 | 45 | 37 | 82% |
| foot | 11 | 27 | 22 | 81% |
| pectoral | 16 | 160 | 125 | 78% |
| arm | 5 | 63 | 46 | 73% |
| forearm | 19 | 167 | 115 | 69% |
| pelvic | 8 | 32 | 22 | 69% |
| cranial | 16 | 72 | 47 | 65% |
| fin | 9 | 39 | 23 | 59% |
| hand | 9 | 72 | 39 | 54% |
| axial | 15 | 29 | 14 | 48% |
| **all** | 128 | 740 | 518 | **70%** |
<!-- /counts:regions -->

**Cranial was the hole and is climbing.** It sat under 20% for several passes with
the head barely scored in any taxon. Huber et al. (2011) took the shark's six
muscles, and Jones et al. (2019) then took the whole avian jaw, throat and orbit
from a contrast-CT digital dissection of one *Columba livia* — ten rows, 33 named
parts. Ziermann & Diogo (2013) then took the axolotl, seven rows and the only larval
*and* adult attachments in the corpus. Ziermann et al. (2014) then took the head of
the hagfish, the lamprey and the skate, and Johnston (2011) the jaw adductors of the
two most basal frogs, and Dearden et al. (2020) the elephantfish. Cranial is now 65%,
up from under 20%, and it is no longer the region to worry about — **axial is**, and
it is now the only region under half.

It moved 66% to 63% and back to 65% inside one session, and the dip is worth keeping.
Anderson (2008) opened the holocephalan column with three present rows carrying no
attachments, which dropped Chondrichthyes 47% to 41%; Dearden then scored against
those same animals and took it to 48%. **A percentage falling because rows arrived is
the opposite of the case recorded in §2**, where the therian cranial column improved
because rows left. Read the scored count beside the percentage, never either alone.

Three of those five passes were on sources the dataset **already cited**. Ziermann
& Diogo (2013) was found by an audit that showed five rows citing it and none
scored; Ercoli et al. (2014) the same, 25 rows; Ziermann et al. (2014) and Johnston
(2011) came out of a density check run over the whole backlog at once, where they
ranked first and second ahead of every unmined paper in `papers/`. A citation is
not a mining. `MINING.md` now carries the ranked list.

**Hand has left last place for the first time, and axial has taken it.** Hand
went 47% → 54% and forearm 58% → 69% on the second half of Gambaryan
et al. (2015) — the same paper, the same three monotreme genera, 57 further rows.
Together the two Gambaryan passes are 108 rows, far the largest single-source
addition the dataset has taken, and they moved the whole corpus from 65% to 70%.
The forearm and hand still carry the two largest occurrence counts, so they remain
the biggest absolute gap even at 69% and 54%; nothing in `papers/` fixes them
across taxa at once and it goes one column at a time. Meers (2003) is the largest
single remaining bite — crocodylian forelimb, and the one naming scheme from Abdala
& Diogo's Tables 1-3 not yet held in full. Dearden et al. (2020) and Anderson
(2008) are now both mined, though Dearden only in part: *Scyliorhinus canicula* is
described in full and still has no rows at all. **The mammalian head remains the
one column with no source at all.**

The **prepollex** is worth singling out, and it is no longer an anuran story.
Anurans lost digit 1, and the preaxial muscles that would serve it — adductor
pollicis, a contrahens, flexores breves profundi slips — attach to the prepollex
instead. That is the position-versus-identity argument with a bone attached to it
rather than just a digit number. **Monotremes have a prepollex too, did not lose
digit I, and hang more on it**: Gambaryan et al. put the entire insertion of the
flexor carpi radialis on it in all three genera, plus the origins of the interossei
of digits I to III, and in *Zaglossus* ligaments relay its pull on to the distal
carpals and metacarpals I-III. So the element is not a compensation for a missing
digit — it is a preaxial lever that some tetrapods keep and load whether or not
digit I is there. The pisiform does the same job on the postaxial side of the same
wrist, taking the flexor carpi ulnaris and relaying to metacarpals II-IV.

**Axial is the floor at 48%, but it is not the empty region it was, and it is 17
rows shorter than it was.** The body
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
| Monotremata | 103 | 103 | 100% |
| Theria | 73 | 64 | 88% |
| Actinistia | 7 | 6 | 86% |
| Crocodylia | 56 | 48 | 86% |
| Tetrapodomorpha (stem) | 42 | 33 | 79% |
| Caudata | 92 | 70 | 76% |
| Lepidosauria | 105 | 67 | 64% |
| Actinopterygii | 14 | 7 | 50% |
| Anura | 72 | 36 | 50% |
| Synapsida (stem) | 4 | 2 | 50% |
| Aves | 79 | 39 | 49% |
| Chondrichthyes | 23 | 11 | 48% |
| Myxini | 3 | 1 | 33% |
| Petromyzontida | 3 | 1 | 33% |
| Testudines | 46 | 12 | 26% |
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

**The branchial basket is now resolved in the skeleton.** `epibranchials`,
`pharyngobranchials` and `hypobranchials` were added for Springer & Johnson's eel,
because the dorsal gill-arch muscles run between individual arch elements — a rectus
dorsalis from one epibranchial onto the preceding one — and the single
`branchial-arches` group could not express it. The ceratobranchial deliberately did
*not* get a new element: the ray-finned fishes joined `cornu-branchiale`, which
already held that element for turtles, salamanders and frogs. One element, per-taxon
names, which is the rule that keeps the hyomandibula and the stapes together.

**The lamprey basket then tested that rule from the other side.** Its constrictores
branchiales externi wrap the *outside* of the basket and end on the taeniae
longitudinales — fore-and-aft bars running across the segmental cartilages, with no
gnathostome counterpart, where every gnathostome branchial muscle this dataset holds
runs within or between arches. `taenia-longitudinalis` is therefore a new element
rather than a per-taxon name for something existing, and the test that distinguishes
the two cases is whether a source can be found that calls them the same thing. None
can. `extrabranchial-cartilages` is the harder call and went the other way: Ziermann
et al. use the one name for the chondrichthyan rods and the lamprey arcus, so it is
one element, with a note saying plainly that a shared id here is not a homology claim.

**Chondrichthyes moved 37% to 47%** on the same pass, from the cucullaris — whose
attachments had been sitting in that row's own `origin`/`insertion` prose,
unstructured, exactly as Ercoli's therian rows had — and from the depressor
hyomandibulae, once it was moved off the dogfish it was never described in. Dearden
et al. (2020), covering an elasmobranch and a holocephalan, and Didier (1987) on
holocephalan myology are still what would move it furthest.

**Myxini and Petromyzontida are off zero, at 33% each, and the interesting part is
what could not be scored.** Ziermann et al. (2014) is the only source in the corpus
that dissects either animal, and it took four new elements to hold what it says:
`lingual-cartilage`, `taenia-longitudinalis`, `extrabranchial-cartilages` and the
`scapular-process` landmark. The agnathan head was missing from `skeleton.json`
almost entirely, and that — not effort, and not the source — is what had kept both
columns empty. Reading the two 33%s as thin coverage would miss the finding: the
hagfish constrictor branchiarum arises from the mesentery and ends on the
connective tissue around the efferent branchial ducts, the surface of the heart and
the fascia of the branchial pouches, and only its most anterior fibres touch
cartilage at all. **A branchial constrictor that inserts on the heart is not a
scoring gap.** The lamprey hypobranchial series is the same case and is left
unscored with the reason in its note, because the alternative — copying the shark's
coracoid-to-mandible rows onto it — is the failure §7 is about.

**Monotremata went 43% to 100% and is the first extant column with no unscored
row in it.** Seven occurrences became 103 across two passes, on Gambaryan et al.
(2015) — a source already cited here for names, whose attachment data had never
been taken, and which measures 8.8 origin/insertion mentions per page over 56
pages. It was not on the ranked backlog in `MINING.md` at all; see that file for
why, and for the citation-derived ranking that replaces the hand-assembled one.
It is now the third-largest column in the dataset behind Lepidosauria and Caudata,
on one paper.

What made the column jump by a factor of seven is that the paper describes **all
three living genera** with a separate Origin and Insertion paragraph each, and the
dataset held one echidna. *Zaglossus bruijnii* was a `taxa.json` exemplar with no
`species.json` entry; *Ornithorhynchus anatinus* had an entry and zero rows. **Three
of the seven pre-existing rows were also wrong, and all three cited this paper** —
a `divided` pectoralis where the source says undivided, a sternocoracoideus on the
coracoid where the source says procoracoid, and a serratus anterior on the cervical
transverse processes where the source says cervical ribs. All three came from
clade-keyed seed blocks; see [§7](#7-the-base-layer-species-and-source).

Two things in it bear on arguments this file already makes. **The monotreme
supracoracoideus is not the intermediate it is usually cited as.** Romer's (1922)
derivation of supraspinatus and infraspinatus from it rests largely on the
monotreme condition, and Gambaryan et al. find all three muscles present at once —
the supracoracoideus on the procoracoid, the other two on the scapula — and read
the latter pair as mammalian additions. That record is now `contested` rather than
`well-supported`, with the two as `membership: disputed` parts. It is the mirror
of the coracoid case below: the same bone loss that moved the therian
supracoracoideus onto the lateral scapula also removed the only animal in which
the three-muscle alternative is visible. And **the monotreme latissimus inserts on
the medial epicondyle**, the far distal humerus, against the lesser tubercle in
therians and reptiles — an attachment that moved the length of a bone, with a
stated mechanism: the barrel rib cage puts the elbow in the plane of the widest
ribs, so the muscle runs straight down the flank.

**The second pass, on the forearm and hand, produced the harder find: a muscle
this dataset records as lost, in a mammal.** `contrahentium-caput-longum` — the
urodele ulnocarpalis — read "an amphibian muscle lost in amniotes, retaining only
its distal derivatives", with no therian row on it. Gambaryan et al. identify it
as the caput humerale profundum of the flexor digitorum profundus, and the
argument is topological rather than positional: the head wedges between the caput
olecrani and the caput ulnare exactly as the urodele ulnocarpalis wedges between
the two heads of the palmaris communis profundus — which are `flexor-accessorius-
lateralis` and `flexor-accessorius-medialis`, both records here — and it ends on
the ligamentum flexorium commune transversum, which they read as the surviving
postaxial segment of the transverse subcarpal ligament the urodele muscle inserts
on. Against Straus (1942), who held it dissolved into the profundus beyond
amphibians. Scored `yes` in the platypus and `uncertain` in both echidnas, where
the belly is there and the diagnostic ligament is reported only by Kajava (1911)
and only as variation. **Three rows on one record disagreeing about a muscle's
identity rather than its presence** is what `uncertain` is for, and it is the
first time this dataset has used it that way.

Three further things from that pass are characters rather than rows. The
**palmaris longus is absent in all three genera**, surviving in *Zaglossus* only
as a bundle of the cutaneus trunci that runs to the flexor tendon — a skin muscle
standing in the position of a limb muscle that does not yet exist. The
**intermetacarpales are absent in both echidnas and present in the platypus**,
explicitly against Kajava (1911) and Howell (1936), who had it the other way
round. And the **lumbricales bifurcate in *Tachyglossus***, each splitting off a
head to the preceding digit, which is reported elsewhere only in colugos.

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
| Elements | 253, of which 223 (88%) carry at least one attachment |
| Observed attachment rows | 1420 |
| Rows naming a **landmark** | 397 (28%) |
| Rows naming a **side** | 913 (64%) |
| Osteological correlates | 111 flagged, 96 carry a muscle |
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
landmark. Fifteen osteological correlates carry no muscle at all: coronoid process
of ulna, linea aspera, tibial tuberosity, pectoral articular process, pygostyle,
tibiotarsus, cranial and lateral cnemial crests, fossa metatarsi I, Meckelian
fossa, epipterygoid, basipterygoid process, temporal bar, ventral radial crest,
posterior ulnar crest. Those are landmarks a palaeontologist would look at first,
and the dataset currently says nothing about what pulls on them. The count rose
because earlier passes added correlates faster than they added the muscles that use
them, and has since fallen as those muscles arrived.

**The flag itself now has histological evidence under it, and the evidence is a
warning.** Pereyra et al. (2019) sectioned the pectoral girdle and humerus of
*Phrynops hilarii*, *Hydromedusa tectifera* and *Chelonoidis chilensis* and
classified the Sharpey's fibres at every attachment. The useful result is the
blanks in their Table 2: **nine attachments leave fibres in one or two of the three
turtles and none at all in the others**, and it runs in both directions — the
testocoracoideus insertion and the biceps origin mark the two pleurodires and not
the tortoise, the deltoideus scapularis and subscapularis origins mark the tortoise
and neither pleurodire. The triceps origin marks the humeral diaphysis in two
species and not the third. Same muscle, same bone, three animals.

So the absence of a correlate is not evidence of the absence of a muscle, and that
is now measured rather than assumed. It is the strongest available argument for
keeping Molnar et al.'s six stem-tetrapodomorph rows at `uncertain`, and `humerus`
is flagged `correlate` on this evidence. The full argument is in
[`METHODS.md`](METHODS.md#what-correlates-can-and-cannot-do).

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
| cranial | 22 | 68 | 3.1 |
| hindlimb | 42 | 38 | 0.9 |
| pectoral | 32 | 28 | 0.9 |
| axial | 33 | 28 | 0.8 |
| forelimb | 52 | 42 | 0.8 |
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
**Taxon-specific attachments: 518 of 740 present occurrences (70%).**
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
| pectoral | 16 | 354 |
| forearm | 19 | 290 |
| cranial | 16 | 169 |
| arm | 5 | 116 |
| thigh | 10 | 104 |
| hand | 9 | 102 |
| leg | 10 | 77 |
| foot | 11 | 63 |
| fin | 9 | 57 |
| pelvic | 8 | 52 |
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

**`seed_division.py` has since been caught doing it, and the prediction above is
the reason it was looked at.** Adding two monotreme species forced the check, and
it turned out **ten blocks were already landing on a clade holding more than one
dissected animal** and silently taking the first — including three of Zaaf's
gecko pairs, both of Johnston's frogs, and Ziermann's shark against the two
chimaeras. It now carries the same `species` key and the same refuse-rather-than-
guess guard as `seed_occurrence_attachments.py`, and all ten are pinned to the
animal they were already landing on, so no data changed silently in either
direction. **Checking what the ten had actually cost turned out to matter more
than the guard.** The obvious inference — that the second species in each of those
clades had been left with no `division` — is wrong: eight of the ten already carry
their own, written by the later pass that added them, so the stale block had been
landing on the first row and the second row had been scored properly anyway. Only
**two** were genuinely unrecorded, both *Gavia immer*, and both were carrying the
split in their `name` and nowhere countable — `"'Rhomboideus' (superficialis +
profundus)"` and `"Scapulotriceps + humerotriceps"`, which is the exact string
problem `seed_division.py` was written to end. McKitrick (1991) describes both
divisions in the loon, so both are now scored, and the script's uniqueness check
keys on (muscle, taxon, species) so a clade can legitimately hold one block per
dissected animal. The lesson is the cheaper one: **a bug's blast radius is worth
measuring before it is described.**

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

### The mapping tables themselves, audited against the papers

Three of these mappings were caught one at a time — Sigurdsen's *Rhinella*,
McKitrick's `gavia-sp`, Sánchez's *Felis catus* — each while reading the paper it
pointed at, and each after the mapping had already survived several passes. That
is a bad detection rate for a table that decides the species on 465 occurrences,
so all 95 mappings were checked at once.

The screen is cheap: extract every PDF to text, then count how many times the
mapped binomial appears in the paper it claims to describe. Zero is the flag. It
ran in a few seconds over the 68 mappings with a local copy, and returned 19
zero-hit flags — **15 real and 4 artefacts of how the papers spell things**.
Johnston writes *Callorhinchus milli* for *milii*, so a correct mapping read as
zero; Hattori & Tsuihiji write *Gallus gallus* where `species.json` carries
*Gallus domesticus*; Diogo et al. name their shark as the genus *Squalus* and
never the species. The false-positive rate is the reason to keep this as a first
pass and not an oracle — every flag was then read against the paper's Materials
section, which is where the real answers were.

Two more came from the tier below, where the mapped species appears once or twice
and the paper's actual animal appears seven times. One came from a source with no
local PDF at all, caught by reading its title: Navarro et al. describe South
American lizards and were mapped to a European one.

**Nineteen of the 95 are wrong, across twelve sources, and they are almost all
one mistake.** Eighteen are fixed here; the nineteenth is flagged in the code and
argued at the end of this section. Abdala & Diogo (2010) genuinely dissected
*Ambystoma ordinarium*, *Rhinella arenarum*, *Trachemys scripta*, *Timon
lepidus*, *Caiman latirostris* and *Gallus* — six columns, verified, and the
largest correct block in the table. Those six exemplars were then copied onto
papers that used none of them:

| Source | Claimed | Actually examined |
|---|---|---|
| Johnston (2014) | *Timon lepidus* | *Ctenosaura pectinata*, figured and "chosen"; *Sphenodon* as the plesiomorphic reference. *Timon* appears zero times |
| Hattori & Tsuihiji (2021) | *Timon*, *Trachemys*, *Caiman* | Dissections listed with counts: *Iguana iguana* [2], *Varanus indicus* [1], *Chelydra serpentina* [1], *Paleosuchus palpebrosus* [1], *Crocodylus porosus* [2], *Gallus gallus* [1], *Grus japonensis* [1]. Only the bird was right |
| Diogo & Molnar (2014) | six clade exemplars | Four key taxa, named in the Materials: *Ambystoma mexicanum*, *Timon lepidus*, *Rattus norvegicus*, *Homo sapiens*. *Caiman* and *Rhinella* appear zero times, *Ornithorhynchus* once, *Gallus* twice, all as literature |
| Leavey et al. (2024) | *Rhinella arenarum* | Thirty-odd frogs compared across locomotor modes. No exemplar, and no *Rhinella* |
| Navarro et al. (2023) | *Timon lepidus* | South American lizards. *Timon* is European |
| Werneburg & Maier (2019) | *Trachemys scripta* | *Chrysemys picta* and *Emydura subglobosa*, one cryptodire and one pleurodire, which is the paper's whole comparison |
| Ziermann et al. (2014) | *Eptatretus burgeri* | *Myxine glutinosa*, 2 juveniles, dissected. *Eptatretus* appears only as other people's developmental work |
| Diogo et al. (2016) + SI | *Ambystoma ordinarium* | *A. mexicanum*, carried over from their own axolotl work. Their other four are stated outright and were all correct |
| Gyambibi & Lemelin (2013) | *Homo sapiens* | 17 prosimians across eleven genera. Lemelin & Diogo (2016) is the same error in a review |

**The pattern is worth naming because it will recur.** Every one of these is a
mapping written from what the *dataset* wanted the paper to be — a lepidosaur
column, a turtle column — rather than from the paper's Materials section. The
tell is that the wrong species is nearly always one of Abdala & Diogo's six. A
paper is not obliged to use the same animals as the paper next to it in the
bibliography, and when it does not, borrowing the exemplar invents an observation.

**Thirteen rows were lifted out**, all of them Diogo & Molnar rows in three of the
five clades that paper never examined — anura, testudines and crocodylia; the
avian and monotreme slots had never had a row on them, which is why the error sat
undetected there. They were name-and-presence rows citing one review, and the
substantive content was already at record level or moved there:
the anuran caudofemoralis reduction into `homology.notes` on that record, the
anuran gastrocnemius hypertrophy likewise. The anuran `gluteus-maximus` row said
`present: "no"` about a frog nobody in the citation chain had looked at, and its
false-friend argument was already carried in `homology.teaching`. Present
occurrences fall 646 → 634, and §1 and §2 rise again for the same reason as
before.

One of the thirteen had a `seed_occurrence_attachments.py` block behind it —
caudofemoralis on *Trachemys*, caudal vertebrae to femur, sourced to Diogo &
Molnar alone. The seed reported `no occurrence row for taxon 'testudines'` and
stopped the build, which is the clade-keyed inversion catching itself. Removing
the row without removing the block would have left the build broken; removing
both is right, because the attachment was the record's consensus written onto a
clade nobody dissected.

**One mapping is knowingly left wrong, and flagged in the code.** Dick & Clemente
(2016) is mapped to *Varanus exanthematicus*, which the paper never names — their
own dissections are nine other varanids, and the Table 1 the six attachment rows
come from is a compilation "of the varanid hindlimb" drawn from Snyder (1954),
Gans et al., Reilly (*Sceloporus clarki*) and Anzai et al. (*Anolis*). Two of the
four are not varanids. The species was borrowed from Cieri's monitor. It stays
only because removing it hands those rows to Diogo & Molnar's *Timon*, which is a
different animal nobody observed them in, and the honest disposition — lifting six
scored attachment rows to record level — should be a decision made deliberately
rather than as a side effect of fixing a lookup table.

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
