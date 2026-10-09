# Dearden et al. (2020) — Chondrichthyan cranial muscles by digital dissection

## Citation

Dearden RP, Mansuit R, Cuckovic A, Herrel A, Didier D, Tafforeau P, Pradel A. 2020.
The morphology and evolution of chondrichthyan cranial muscles: a digital dissection
of the elephantfish *Callorhinchus milii* and the catshark *Scyliorhinus canicula*.
bioRxiv preprint.

**Preprint.** A peer-reviewed version was published subsequently and should replace
this entry once checked.

## Question

Chondrichthyans are the sister group to bony fishes, so their cranial anatomy
constrains any account of how the vertebrate head evolved. The two constituent
groups — holocephalans and elasmobranchs — are arranged strikingly differently, and
that difference has driven major hypotheses about the jaws and pharynx. Yet the
musculoskeletal information available was still largely from traditional accounts,
many of them a century old.

## Taxa and material

**Synchrotron tomography** yielding 3D data for two animals: the elephantfish
***Callorhinchus milii*** (holocephalan) and the catshark ***Scyliorhinus
canicula*** (elasmobranch). One from each group, which is the comparison the paper
exists to make.

## Scored

2 occurrence rows, both on ***Callorhinchus milii*** — `hypobranchial-muscles` and
`adductor-mandibulae-posterior`.

The coracomandibularis row carries the detail worth having: very large, its main
origin on the T-shaped anteroventral face of the coracoid region of the pectoral
girdle, inserting along Meckel's cartilage, triangular in ventral view and
broadening forwards.

**Only half this paper is mined.** *Scyliorhinus canicula* is described in full and
still has no rows at all. That is the largest single piece of scorable chondrichthyan
description sitting unused in `papers/`, and closing it would move the thinnest
extant column in the dataset.

## Limitations

- **Preprint.** Check against the published version before relying on any specific
  claim.
- **Two species.** Chondrichthyes is a large group and these are one holocephalan
  and one elasmobranch.

## Relevance to comparative anatomy teaching

The modern counterpart to the century-old accounts, and a good demonstration of what
tomography adds: muscles traced in three dimensions without the dissection destroying
the relationships between them. Pair with **Ziermann et al. (2014)** for hagfish,
lamprey and skate, **Huber et al. (2011)** for the shark jaw, and **Anderson (2008)**,
which reconciles holocephalan names against the rest of the gnathostomes.

## Both animals mined, 2026-10-08

The earlier note above said only half the paper was mined. The *Scyliorhinus*
half is now filed: 26 rows in
`data/observations/scyliorhinus-canicula__dearden-etal-2020.json`, and the
*Callorhinchus* file grew from 2 rows to 34. Every muscle in the two cranial-muscle
sections is a row, including the six extraocular muscles and the eyelid muscles;
about half are filed and half parked, each with a `blockedNote`. The three
ligaments (ethmopalatine, labial, rostral) are described but are not muscles, so
they have no rows; the ethmopalatine ligament is the one a jaw-mechanics model
would want.

**Worth carrying forward.**
- Their *Scyliorhinus* levator labii superioris runs from the back of the nasal
  capsule to the dorsal adductor, close to what Wilga et al. (2001) and Huber et
  al. (2011) call the preorbitalis in *Squalus*. Nothing here equates them.
- Their constrictor hyoideus dorsalis includes the levator hyomandibulae, whose
  front fibres cannot be separated. The dataset's record for it assumes they are
  distinct.
- Their *Callorhinchus* muscles agree closely with Didier (1987) on *Hydrolagus*,
  with the differences noted in the rows (the pars rostralis insertion; the
  levator anguli oris posterior's insertion; the interpharyngobranchialis, which
  Didier found absent).
