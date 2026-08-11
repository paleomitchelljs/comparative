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
- **The humeral origin of both pronators.** She flags "homology problems with
  Baumel et al." over whether the tuberculum supracondylare ventrale and the ventral
  epicondyle are the same thing, so no landmark is asserted — naming the
  entepicondyle would settle by fiat what she leaves open.
- **The os radiale** in the extensor metacarpi radialis row: it is a pulley the
  tendon passes around, not an attachment.
- The avian-only muscles with no record here: expansor secundariorum,
  ectepicondylo-ulnaris, ulnometacarpalis dorsalis and ventralis, extensor longus
  alulae, extensor longus digiti majoris.

## A recorded disagreement

The scapulotriceps has **no "furcular" origin** in loons, against Sanders (1967).
That is in the occurrence note rather than resolved.

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
