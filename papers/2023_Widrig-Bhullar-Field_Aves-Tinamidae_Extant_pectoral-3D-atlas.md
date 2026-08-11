# Widrig, Bhullar & Field (2023) — 3D atlas of tinamou pectoral morphology

*Journal of Anatomy*. doi:10.1111/joa.13919. Open access.
Source key: `widrig-etal-2023`

## Why it was reached for

Aves is the largest gap in the dataset and Fisher & Goodman (1955), the obvious
source, turned out to be an uneven scan that has to be read page by page. This is
modern, open access, contrast-enhanced CT of *Nothoprocta pentlandii*, with clean
text and current avian nomenclature — the highest yield per effort left in the
avian corpus.

Scored (3): `scapulohumeralis-anterior`, `scapulohumeralis-posterior`,
`deltoideus-clavicularis`.

## Why only three: the columns interleave

The PDF is two-column and `pdftotext` interleaves adjacent descriptions, so a
section heading frequently sits above text belonging to its neighbour. The block
under `3.2.12 | M. deltoideus pars major` is half scapulohumeralis cranialis and
half a description mentioning the triosseal canal — which is supracoracoideus
territory, not deltoid. Anything scored from that would have been a guess.

Only descriptions that identify themselves in their own first clause ("M.
scapulohumeralis caudalis is substantially larger than…") were used. The rest —
`serratus-anterior`, `deltoideus-scapularis` — need the figures, or a
column-aware extraction, and are left.

## The finding worth keeping

**The avian clavicular deltoid takes a furcular origin.** M. deltoideus pars minor
arises from the lateral acrocoracoid process of the coracoid *and the acromial
process of the furcula*. This record is the clavicular deltoid across tetrapods;
in birds the clavicles are fused into the furcula, so the homology is carried by a
bone that no longer exists as a pair. That is the fusion machinery in
`skeleton.json` earning its place on a muscle record rather than only on an
element.

## A word-collision the validator caught

The **"acromial process of the furcula" is not the scapular acromion.** Scoring it
as `landmark: acromion` failed twice over — wrong parent, and the acromion is
correctly recorded as absent in birds. Two different structures sharing a word,
and the containment check is what separated them. The row is scored on the furcula
with the detail in the note.

## Not covered by this paper

`protractor-pectoralis` (the avian occurrence is cucullaris capitis/cervicis, a
neck muscle outside a pectoral atlas) and `rhomboideus`. Neither appears in the
muscle list.
