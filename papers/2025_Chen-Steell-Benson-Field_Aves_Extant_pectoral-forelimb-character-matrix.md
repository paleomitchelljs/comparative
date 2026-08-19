# Chen, Steell, Benson & Field (2025) — An anatomical matrix for crown birds

## Citation

Chen A, Steell EM, Benson RBJ, Field DJ. 2025. Toward a comprehensive anatomical
matrix for crown birds: phylogenetic insights from the pectoral girdle and forelimb.
*Integrative Organismal Biology* 7(1): obaf029.

## What it is

An **osteological character matrix** for the crown-bird pectoral girdle and forelimb.
Skeletal rather than myological: it scores bones and their features, not muscles.

## What it is used for here

Cited on seven `skeleton.json` elements — carpometacarpus, coracoid, furcula,
scapula, sternal keel, tarsometatarsus, tibiotarsus — for **avian presence and
per-taxon naming** rather than for any muscle row.

Three of those are compound bones this dataset records with `fusedFrom` rather than
`partOf`: the carpometacarpus, tarsometatarsus and tibiotarsus. That distinction
matters because `partOf` means containment within one bone and the attachment diff
reads it that way — a bird inserting on the tarsometatarsus compared with a
crocodylian inserting on the metatarsals would otherwise report as a *refinement*,
one author being more precise than another, when what has happened is that a bone
absorbed its neighbours. See `METHODS.md`.

**No occurrence rows**, correctly.

## Why it is worth having anyway

It is the model for how a character matrix over this anatomy is built and scored,
which is directly relevant to the phylogeny view: the presence data here is already
a character matrix, and the questions this paper answers about character
construction — what counts as one character, how to treat a fused element, how to
avoid scoring the same fact twice — are the same ones that arise in `taxa.json`.

## Relevance to comparative anatomy teaching

A current example of morphological phylogenetics on a group where molecules are
well resolved, which is the case where morphological characters have to justify
themselves. Pair with **Blotto et al. (2020)**, which does the same job with muscles
rather than bones in Anura.
