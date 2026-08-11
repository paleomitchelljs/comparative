# Sigurdsen, Green & Bishop (2012) — Did *Triadobatrachus* jump?

*Fieldiana Life and Earth Sciences* 5:77–89. doi:10.3158/2158-5520-5.1.77
Source key: `sigurdsen-etal-2012`

## Why it was reached for, and what was wrong before it was opened

Anura was tied for the largest gap at 40 unscored rows, 21 of them forelimb and
pectoral. This paper was already cited for two of them and neither was scored — the
same "cited therefore mined" case as Ziermann & Diogo (2013).

Then the species check failed. **The paper examines no *Rhinella*,** yet both rows sat
on *Rhinella arenarum* and `attribute_species.py` had the source mapped there. That
mapping was Abdala & Diogo's anuran exemplar borrowed for a paper that does not use
it. Its bufonid is *Anaxyrus americanus*; its dissected and figured frogs are
*Leiopelma hochstetteri* and *L. archeyi*, *Ascaphus truei*, with *Lithobates
pipiens* and *catesbeianus*, *Xenopus laevis*, *Scaphiopus holbrookii* and *Conraua
goliath* also examined. The exemplar is now *Leiopelma hochstetteri* and the two rows
have been de-cited from this paper, keeping Abdala & Diogo.

Measured **3.8** mentions per page, not the 4.3 recorded — the mixed band.

**Anura 35% → 43%.** Seven rows for *Leiopelma hochstetteri*, two for *Xenopus
laevis*.

## What it fixes about this dataset's nomenclature

The single most useful paragraph, because three records depend on it:

- anuran **"deltoid"** = caudate **procoracohumeralis** = amniote **deltoideus
  clavicularis**
- anuran and caudate **"dorsalis scapulae"** = amniote **deltoideus scapularis**

Both mappings are now stated in the relevant `attachmentNote`s.

## Two anuran novelties, each scoreable

**A shared tendon.** The dorsalis scapulae and the latissimus dorsi *converge* and
insert together on the lateral face of the deltopectoral crest by a common tendon,
which they do not do in salamanders. Both rows land on the same landmark, and that is
the finding rather than a duplication.

**A head lost.** The anconeus (triceps) has three heads in anurans — caput mediale,
laterale, scapulare — where salamanders have a **fourth point of origin at the
coracoid**. A division count differing between two amphibian orders by a stated
absence rather than by how authors carve the muscle up.

## A disagreement now visible as one

Sigurdsen et al. state the salamander subscapularis **has no clear homologue in
frogs**, and explain the one anuran report of it — Ritland's (1955b)
subcoracoscapularis in *Ascaphus* — as the longus slip of the coracobrachialis under
another name. So `subcoracoscapularis` is scored `no` for *Leiopelma* against Abdala
& Diogo's `yes` for *Rhinella*, and **Anura now computes as `variable`**. Two
sources, two frogs, and a muscle whose anuran presence turns on whether a
coracobrachialis slip is being counted twice. The `coracobrachialis` row is scored
`divided` into longus and brevis for the same reason and the two rows must be read
together.

## The deltopectoral crest is the paper's real subject

It carries the insertion of both deltoideus and pectoralis, and in most anurans runs
further distally than in salamanders or any other tetrapod. *Leiopelma*'s is
relatively **short**, tapering out near the midpoint of the shaft — the plesiomorphic
condition, also found in extinct subfossil species of the genus — while strong
jumpers such as *Lithobates* extend it much further, and it is weak in the
semiaquatic *Ascaphus* and the terrestrial hopper *Anaxyrus*. They found **no extant
anuran whose crest resembles a salamander's**.

The headline reading: the deltoid grew in importance relative to the pectoralis, and
the crest's orientation follows from loading during **landing** rather than take-off.

## Xenopus, because the pipid humerus is the odd one

Two rows, and they disagree with *Leiopelma*: a prominent **boss** for the pectoralis
insertion close to the posterior edge of a short, almost straight, ventrally directed
crest with a biconcave proximal area; and a partially covered **groove** running from
the crest along the ventral shaft that houses the long coracoradialis tendon on its
way to the radio-ulna (Ritland 1955a reports the same in *Alytes*). The groove is a
correlate of the tendon's **path**, not of an attachment, so no humeral row is put on
it.

## One element added

`epicoracoid`, the cartilaginous medial part of the girdle, which carries the pars
episternalis of the deltoid. Present in anurans and lizards.

## Not scored: *Triadobatrachus*

The paper's title subject is a Triassic stem-salientian (MNHN MAE 126), and its
correlates — a frog-like deltoid attachment on the scapula, an enlarged deltoid, a
deltopectoral crest orientation read as a landing adaptation — are exactly the kind of
inference the stem-tetrapodomorph column holds. **It has nowhere to go: there is no
stem-salientian operational taxon**, and adding one means editing the topology in
`taxa.json`, which is a structural change deserving its own pass rather than a
footnote to this one. *Prosalirus bitis*, *Czatkobatrachus* and the proto-lissamphibians
*Amphibamus* and *Doleserpeton* are in the same position. That is the largest thing
left in this paper.
