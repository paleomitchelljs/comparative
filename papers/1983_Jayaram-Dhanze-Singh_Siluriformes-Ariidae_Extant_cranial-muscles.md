# Jayaram, Dhanze & Singh (1983) — Cranial muscles of *Arius*

## Citation

Jayaram KC, Dhanze JR, Singh R. 1983. Comparative morphology of the cranial muscles
in some species of the genus *Arius*, with a note on their utility. *Bulletin of the
Zoological Survey of India* 5(1): 107–111.

## Question

Whether cranial myology carries taxonomic signal in a catfish genus whose species
are hard to separate.

## Taxa and material

Three species of the marine catfish genus *Arius*: **A. arius, A. caelatus and A.
thalassinus**. The mandibular and hyoid muscle complexes and their constituent
elements described in each, **18 muscles studied** in total.

## Findings worth carrying

**Nine of the eighteen muscles are identical across all three species** in origin,
insertion, disposition and morphology. In the other nine the interspecific
differences are slight, and the authors discuss them against each species' habitat
and systematic position.

That is a useful negative result for a dataset built on species-level scoring: a
genus can be myologically near-uniform, and where it is, one species' rows are a
reasonable guide to its congeners. It does not license copying rows between them —
but it does say what kind of variation to expect.

**They also clarify the nomenclature of several muscles confused by earlier
workers**, which is why the source is cited here for names as well as for rows.

## Scored

**Remined 2026-08-20. Twenty muscles across three species: 59 rows, 44 filed and 15
parked.** Until that day it was **3 rows on *Arius* sp. with no attachments at all**,
and that file is gone: the paper describes three animals and now has three columns.

### The genus-level fudge, and why it had to go

The old note gave the reason: "the rows are scored to *Arius* sp. rather than to one
of the three, because the shared condition is what was taken." That is defensible
and it threw away the paper's entire point. Jayaram et al. wrote it to test whether
cranial myology carries taxonomic signal in a genus whose species are hard to
separate, and **nine of the eighteen muscles differ between the three**. A genus row
cannot hold a difference between species of that genus. Worse, the three rows
carried no origin or insertion, so the file recorded neither the sameness nor the
variation.

`arius-sp` still exists — Ziermann & Diogo (2019) use it legitimately — but this
source no longer does.

### What the three columns say

| | *A. arius* | *A. caelatus* | *A. thalassinus* |
|---|---|---|---|
| Add. mand. 4 origin | dorsal **preopercle** + sphenotic + pterotic | dorsal **hyomandibular** + sphenotic + pterotic | as *arius*, **wholly tendinous** |
| Add. mand. 6 | undivided, from the hyomandibular | **cleft into two layers**, upper off the sphenotic | cleft, as *caelatus* |
| Intramandibularis | well developed, from aponeuroses of elements **2 and 6** | poorly developed, from element **6 alone** | moderate, from 2 and 6 |
| Dil. op. inferioris | hyomandibular **+ pterotic** | **hyomandibular alone** | hyomandibular + pterotic |

Four attachment differences in eleven muscles, and every one of them is invisible in
a genus-level row.

### A contradiction inside the paper, and the Discussion settles it

The introduction to the adductor mandibularis says six elements in *A. arius* and *A.
thalassinus* and **five in *A. caelatus***. The descriptions that follow then name *A.
caelatus* in all six numbered sections, including a sentence about the nature of
element 2's origin "in all the three species".

**The Discussion names the missing one**: *"the absence of Adductor mandibularis 2 in
A. caelatus unlike that of the other two species where it is present"*. And the
description of element 1 agrees without saying so — in *A. caelatus* its deep layer is
overlapped by element 3, where in the other two it is overlapped by element 2.

Three statements against one. **Element 2 is scored absent in *A. caelatus***, which
is why that species carries six parts and the others seven, and the `divisionNote` on
all three rows records the passage that says otherwise rather than deleting it.

A second inconsistency is left standing because nothing resolves it: the Discussion
lists adductor mandibularis 3 and 4 among the muscles with "a common pattern in
respect of the origin, insertion, disposition and morphology" in all three species —
but §1.1.1.4 gives element 4 a **preopercular** origin in *A. arius* and *A.
thalassinus* and a **hyomandibular** one in *A. caelatus*. The rows follow the
description.

### Four new skeletal elements, and a word collision avoided

`preopercle`, `opercle`, `sphenotic`, `pterotic` — the teleost opercular series and
two otic bones, which this skeleton had none of despite carrying four fish sources.

**`opercle` is not `operculum`.** The element already in the file under that name is
the *amphibian otic operculum*, the plate in the fenestra ovalis that the opercularis
muscle pulls on. Scoring a catfish gill cover on it would have put a dilator operculi
insertion in a salamander's ear. Two structures, one word, and the only thing between
them is that somebody looked.

### Section 2 — the hyoid groups, and where this dataset runs out

Nine more muscles. Four file and five park, and the split is not about the paper.

**The protractor hyoidei is two records fused, and the source says so.** Jayaram et
al. call it a compound of the intermandibularis posterior and the interhyoideus, after
Edgeworth (1935) and Winterbottom (1974). It is scored on `intermandibularis` with
`fusedWith: ["interhyoideus"]` — the first use of that field where the *source*
states the fusion rather than a dissector failing to separate two bellies.

**The hyohyoid series goes to `interhyoideus`**, whose consensus is ceratohyal-or-
hyomandibula to a midline raphe of the throat, which is what these muscles are. Two of
the three carry the paper's sharpest species characters:

- **The hyohyoides inferioris takes a different branchiostegal ray in each species** —
  the fourth in *A. thalassinus*, the fifth in *A. arius*, the sixth in *A. caelatus*.
- **The hyohyoidei adductores form a different number of bands in each** — six, six or
  seven, and five.

Three species, three states, twice over. That is the taxonomic signal the paper was
written to look for, and a genus-level row could not have carried either.

**Five muscles parked on `no-record` for a few hours, and were then unparked.** The
adductor arcus palatini, extensor tentaculi, levator operculi, adductor operculi and
adductor hyomandibulae had no record here: the only constrictor dorsalis record was
`levator-arcus-palatini`, whose consensus says *elevates and abducts the
palatoquadrate*, which is the opposite of what the adductor does — and which turns out
to be the right instinct for the right reason. **They are not constrictor dorsalis at
all.** Winterbottom (1973) derives every one of them from the *constrictor hyoideus
dorsalis*: a different arch, a different nerve, CN VII against CN V.

`constrictor-hyoideus-dorsalis` was created from Winterbottom the same day and all
fifteen rows were promoted onto it. The park did its job exactly as `MINING.md`
describes — the reading was done once, held with its attachments, and cost nothing to
file when the record appeared.

Eleven new elements for this section: `parasphenoid`, `orbitosphenoid`,
`lateral-ethmoid`, `autopalatine`, `ectopterygoid`, `metapterygoid`, `post-temporal`,
`epihyal`, `hypohyal`, `branchiostegal-rays`, `urohyal`. `autopalatine` is kept apart
from `palatine`, which in this file is the tetrapod dermal bone.

## Limitations

- **Sixteen pages of two-column OCR, and it is rough** — `g,.oup`, `()verlaps`,
  `lnuscular`. Reconstruct the columns by slicing each page at character 52; the
  anatomy is legible after that, the figure captions are not.
- The figures carry detail the text does not, and are not readable here.

## Relevance to comparative anatomy teaching

A small, clean example of muscle anatomy used for systematics at the species level,
and of the honest reporting of how *little* varied. Pair with **Winterbottom
(1973)** for the teleost naming framework these muscles sit in.
