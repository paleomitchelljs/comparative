# McKitrick (1991) — Forelimb myology of loons

*Zoological Journal of the Linnean Society* 102: 115–152. Source key: `mckitrick-1991`

## Why it was reached for

Aves was the largest remaining gap — 43 unscored rows, concentrated in the forearm
and hand — and this is the densest avian source in `papers/` at 6.0 origin/insertion
mentions per page, confirmed on the PDF before opening it. **Aves 30% → 42%.**

## What makes it usable: one specimen, named

> "Descriptions are for *Gavia immer* CM 2320, with variations for other specimens
> and species as noted."

That sentence is why this paper scores cleanly. Two *G. immer* (CM 2320, USNM
504983), one *G. stellata*, two *Pelecanoides garnoti*. The rows are CM 2320; the
second loon specimen's differences go in the notes, where they read as
within-species variation rather than as a clade character.

Two species added: `gavia-immer` (replacing the genus-level `gavia-sp` placeholder,
which had no rows) and `pelecanoides-garnoti`.

## Scored (13)

Girdle and arm: `latissimus-dorsi`, `rhomboideus`, `serratus-anterior`,
`triceps-brachii`, `biceps-brachii`, `brachialis`. Forearm: `pronator-teres`,
`pronator-quadratus`, `extensor-antebrachii-carpi-radialis`, `extensor-digitorum`,
`extensor-antebrachii-carpi-ulnaris`, `supinator`.

Plus one absence: **the supinator is absent in *Pelecanoides garnoti***, in the same
dissection series that describes it as a bulky belly in the loon. That is a
species-level `present: "no"` from a dissection, and it is one of the character
differences behind the paper's negative result.

## The negative result is the paper's point

She set out to test a proposed loon–tubenose (Gaviiformes–Procellariiformes) sister
relationship from Cracraft and Sibley et al., and the wing muscles do not support
it. Worth keeping because it is a reminder that a myology paper's characters can be
gathered for a question that fails.

## What was deliberately not scored

- **Pars metapatagialis of the serratus superficialis** inserts into the *humeral
  feather tract*, not onto bone. Like the anuran knee aponeurosis and the shark's
  midventral raphe, it is a muscle whose distal end a fossil cannot record.
- **The biceps slip** ends in the propatagial aponeurosis.
- **The humeral origin of both pronators** — but not for the reason this note used
  to give. The "homology problems with Baumel et al." remark is made about
  ***Pelecanoides garnoti*'s pronator profundus**, where the origin shifts off the
  tuberculum supracondylare ventrale onto the ventral epicondyle. In *Gavia immer*
  she names the tuberculum for both pronators without hedging. The rows stop at the
  bone because `skeleton.json` resolves no tuberculum supracondylare ventrale — and
  they must not be collapsed onto the entepicondyle, because in this animal she
  **distinguishes** the two: the flexor digitorum superficialis arises from the
  ventral epicondyle, both pronators from the tuberculum. A caveat had been
  transplanted from one species to another, and it was hiding a real distinction.
- **The os radiale** in the extensor metacarpi radialis row: it is a pulley the
  tendon passes around, not an attachment.
- The avian-only muscles with no record here: expansor secundariorum,
  ectepicondylo-ulnaris, ulnometacarpalis dorsalis and ventralis, extensor longus
  alulae, extensor longus digiti majoris.

## A recorded disagreement

The scapulotriceps has **no "furcular" origin** in loons, against Sanders (1967).
That is in the occurrence note rather than resolved.

## What a blind re-mine of this paper corrected

Nine of the thirteen rows came back exactly right, and the measured density
reproduced at 6.0. Four things did not:

- **`triceps-brachii` had both heads on one landmark-free insertion row.** She gives
  them different sites: scapulotriceps on the **processus cotylaris dorsalis**,
  humerotriceps on the **olecranon**. The note's reasoning — that the processus is
  not the olecranon and equating them would manufacture a correlate — is right for
  the scapulotriceps, and it had been over-applied to suppress a site she states
  plainly for the other head. Two rows now; `olecranon` was in `skeleton.json` as a
  correlate all along.
- **`serratus-anterior` is named "superficialis + profundus" and scored only the
  superficialis.** The profundus' cranial head arises from the **last cervical
  vertebrae**, not a rib, and inserts on the **dorsomedial** scapula. Both were
  missing; both elements existed.
- **The latissimus' iliac origin was one `lateral` row** where she gives the
  **medial, cranial and lateral** surfaces of the ala preacetabularis ilii. Three
  rows now, per the one-row-per-aspect rule.
- **A sourced absence had been filed as a to-do.** M. scapulohumeralis cranialis is
  **absent in *Gavia immer* CM 2320** — the specimen every other *G. immer* row here
  is scored from — and present in USNM 504983, in *G. stellata* and in
  *Pelecanoides*. Sanders (1967) also found it in *G. immer*. That is a presence
  disagreement *between two specimens of one species*, which the "still in it" list
  below recorded merely as unmined. It is now an `uncertain` row on
  `scapulohumeralis-anterior` with no attachments, because the animal it was seen in
  is not the animal the other rows describe.

Also: the *Pelecanoides* supinator absence is kept as `no` on the strength of her
descriptive section, but her character 11 is headed "reduction or absence" and reads
"absent **or reduced to an aponeurosis**", and under the ectepicondylo-ulnaris she
allows that part of that tendinous mass "represents all that is left of M.
supinator". The belly is gone; the tendon may not be. That hedge is now in the row.

## One element added

`carpometacarpus`, `fusedFrom` the distal carpals and metacarpals, following the
tarsometatarsus and tibiotarsus pattern: she records insertions on the processus
extensorius and on the proximal caudodorsal surface of the major metacarpal, which
are sites on the compound bone. The alular and major metacarpals stay
distinguishable within it, which is why sources name both on one bone.

## What this pass exposed in the code

Adding a second avian species to records that already had one made
`seed_occurrence_attachments.py` misbehave: its table is keyed on **clade**, and
`{clade: row}` silently kept whichever row came last, so three blocks written for
Gallus, the swan and the penguin were handed to the loon and overwrote it. The
matcher now requires a clade to have exactly one row, or the block to name its
species. It also turned up that the penguin's supracoracoideus and
subcoracoscapularis rows had been quietly overwritten by Abdala & Diogo's generic
avian block for the same reason.

## Still in it

*Gavia stellata* throughout, *Pelecanoides garnoti* in full (a procellariiform
forelimb, which the corpus otherwise lacks), and the girdle muscles not yet taken:
pectoralis with its four partes, supracoracoideus, deltoideus major and minor,
subscapularis and subcoracoideus, coracobrachialis cranialis and caudalis,
sternocoracoideus, scapulohumeralis cranialis and caudalis, and the manus
intrinsics.
