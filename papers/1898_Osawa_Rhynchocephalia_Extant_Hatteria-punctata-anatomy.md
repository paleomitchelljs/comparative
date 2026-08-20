# Osawa (1898) — Beiträge zur Anatomie der *Hatteria punctata*

*Archiv für mikroskopische Anatomie* **51**: 481–691. Written at the anatomical
institute of the University of Freiburg i. Br.

Source key: `osawa-1898`. German, 211 pages, 53 text figures.

## What was acquired

archive.org item `archivfrmikros51berl` — Archiv f. mikr. Anat. **Bd. 51**. The
monograph does not have its own item; it had to be located inside the volume by
finding the printed page in the OCR text and reading off the offset, which is
**+14** (printed 481 is PDF page 495). Pages 495–705 were extracted; the next
paper, Bischoff on hair growth, begins at PDF 706.

## Structure

| part | what |
|---|---|
| I. Zur Knochenlehre | osteology, including the bones of the forelimb |
| **II. Zur Muskellehre** | the myology, by region and by layer (`Schicht`) |
| III. Zur Nervenlehre | spinal cord, brain, and the peripheral nerves muscle by muscle |

The myology numbers its muscles: **46 for the forelimb** and **37 for the
hindlimb**, each with *Ursprung*, *Ansatz* and *Innervation*. That third field is
why this source is unusual here — it is the only lepidosaur source in the
bibliography that supports structured `nerves` on a limb row, because Osawa
dissected the brachial and sacral plexuses alongside the muscles.

## Why it is worth the German

`sphenodon-punctatus` had 11 rows, all cranial, from Haas (1973). Osawa fills the
limbs and the girdles. **62 rows were taken from it; the tuatara now has 73, all
scored.**

Its second value is that Osawa argues with his predecessors constantly, and names
them. Nearly every muscle carries his own concordance against Fürbringer, Gadow,
Günther and Perrin — which is what made the mapping onto this dataset's records
possible at all, since his own names are compounds nobody else uses
(*capiti-dorso-clavicularis*, *subscapulo-coraco-brachialis*,
*pubo-ischio-trochantericus internus*).

## Corrections he makes, which are in the rows

- **Fürbringer** on the costo-coracoideus: what Fürbringer called by that name
  matches Osawa's *costo-sterno-scapularis*, and Osawa says the true
  costo-coracoideus of this animal seems not to have been seen by Fürbringer in
  any reptile.
- **Gadow** three times: on the innervation of the coccygeo-femoralis brevis
  (postsacral, not presacral or sacral); on the insertion of the pubo-tibialis
  posticus (the lateral proximal corner of the tibia, not the back of the fibular
  neck); and on the *fibulo-tibialis inferior*, which Gadow did not notice at all.
- **Günther** on his *M. gracilis*, whose description Osawa quotes to show it fits
  the pubo-tibialis posticus rather than the pubo-ischio-tibialis Gadow assigned
  it to.
- On the **tibialis posticus**: it arises from the fibula and the interosseous
  membrane and **not from the tibia**, "as is generally stated", despite the name.

## Observations that became notes rather than rows

- The **coraco-brachialis** is fused to the supracoracoideus in some specimens and
  cleanly separate in others, with the N. coraco-brachialis passing between them
  as the only reliable boundary — a muscle boundary that exists as a nerve.
- The **biceps** (his *coraco-antibrachialis*) has different nerves for its
  proximal and distal halves.
- The **levator scapulae** has one origin, two bellies and two different cervical
  nerves.
- The **extensor digitorum communis longus** of the foot had two slips in one
  specimen and three in another.
- There is **no calcaneal tendon**: both heads of the gastrocnemius end in the
  plantar aponeurosis, and the deep femoral head terminates in a tendinous arch
  that gives origin to the flexor digitorum communis sublimis — one muscle's
  insertion being the next one's origin, in series.

## Skeletal consequences

Three elements gained Lepidosauria on this source: `humerus-lateral-process`,
`humerus-medial-process` and `lesser-tubercle`'s hindlimb counterpart, the
trochanter minor. The first two matter comparatively — they had been scored for
Testudines alone on Walker, who puts the same two muscles on the same lateral
process, so the tuatara has the turtle's two proximal humeral processes rather
than the greater and lesser tubercles of the other amniote columns.

## Not mined

**Part I (osteology) and Part III (nerves).** The nerve section describes the
plexuses in their own right and would support far more than the per-muscle
innervation already taken from the myology.

## Audit, 2026-08-19: two findings, one of them procedural

**Held: 63 rows, all limb, plus the iliocaudalis and ischiocaudalis.**

**Osawa describes the cranial and axial musculature and none of it was taken.**
Mentions in the myology: pterygoideus 17, temporalis 14, masseter 12 for the jaw;
obliquus 28, intercostales 26, transversus 10, longissimus 7 for the trunk. The
dataset holds zero cranial and zero axial rows from this source. Lepidosauria's
cranial column is thin and *Sphenodon* is the outgroup half of every squamate jaw
comparison, so this is a real gap rather than a tidy one.

### The procedural finding

`MINING.md`'s density triage greps `origin|insert`. On this paper that returns
**0.06 mentions per page** across 211 pages — below the 2.0 threshold, whose
instruction is "do **not** plan rows around it".

**The dataset already holds 63 scored rows from this paper.** The metric was
refuted by data committed before the metric was written. What it actually measured
was that the paper is in German: *entspringt* appears 142 times, *Ursprung* 71,
*Ansatz* 55, *inserirt* 52 — **314 attachment statements**, or 1.5 per page in a
language that says in one word what English says in four.

Four of the ten works in `WORKLIST.md`'s acquisition table are German, so the check
would have told a future reader to skip Gaupp, Ribbing, Lakjer and Ogushi on
arrival. `MINING.md` is corrected.

## Re-mine, first pass: the cranial half, and a correction to the audit

The audit said "Osawa describes the cranial and axial musculature and none of it
was taken", and drew the conclusion that Lepidosauria's thin cranial column was
the gap. **The first half is true and the conclusion is wrong.** *Sphenodon*
already carries ten cranial rows from Haas (1973), a dedicated Rhynchocephalia and
Squamata jaw-muscle monograph, which is the better source for that animal's jaw
and is `homologyScope` besides. Osawa is a second independent worker on an animal
already scored, not an empty column.

That matters for what to do with him. The dataset holds **one row per record per
species**, so a second description cannot simply be added alongside — it has to be
merged into Haas's row or left out. Osawa's Kaumuskeln are therefore **parked on
`occupied`**, a `blockedBy` kind this pass added for exactly this: two workers, one
animal, one row.

His jaw musculature, in full:

| Osawa's name | Belongs on | Innervation |
|---|---|---|
| M. capiti-mandibularis s. temporo-massetericus | `adductor-mandibulae-externus` | V3 |
| M. pterygoideus externus | `adductor-mandibulae-internus` | V3 |
| M. pterygoideus internus | `adductor-mandibulae-internus` | V3 |
| M. parieto-mandibularis | `depressor-mandibulae` | **VII** |

**Two things in that table are worth carrying across whatever is done with the
rows.** Osawa states that no portion answering to a *masseter* is yet
differentiated in *Hatteria* — a presence claim, not an absence of description.
And he innervates the parieto-mandibularis from the **facialis**, noting that the
"Digastricus" of earlier authors is justified on that ground and that the muscle
ought really to be discussed apart from the other three. That is the arch-2
identity of the depressor mandibulae argued from innervation in 1898.

He also remarks that the pterygoideus externus and internus insertions are
continuous and that the two cannot be sharply separated — the boundary is only
indicated by the course of the third trigeminal branch.

**Still not taken:** the axial musculature, the neck (he divides it into ventral
and deep groups and names five ventral muscles on the page after the Kaumuskeln),
and Part III on the nerves, which describes the plexuses in their own right.
