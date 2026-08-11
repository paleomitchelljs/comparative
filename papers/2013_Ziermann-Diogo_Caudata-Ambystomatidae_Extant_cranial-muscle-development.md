# Ziermann & Diogo (2013) — Cranial muscle development in the axolotl

*The Anatomical Record* 296:1031–1048. doi:10.1002/ar.22713.
Source key: `ziermann-diogo-2013`

## Why it was reached for

An audit of previously mined papers found it **cited for five rows and none of them
scored** — the "cited therefore mined" fallacy running in reverse. It had picked up
those citations in the re-attribution pass, which moved four salamander cranial rows
here from the authors' own 2019 review (that review examines *Scyliorhinus*,
*Polypterus* and *Danio*, and no tetrapod).

Measured **3.3** origin/insertion mentions per page, squarely in `MINING.md`'s mixed
2–4 band, and the band's description was exactly right: the attachments are there,
but embedded in a developmental narrative instead of set out under headings. A slower
pass, and worth it.

**Cranial 46% → 56%. Caudata 70% → 76%.** Seven rows for *Ambystoma mexicanum*.

## What this source has that no other in the corpus does

**Larval AND adult attachments for the same animal.** Several muscles move:

| Muscle | Larva | Adult |
|---|---|---|
| adductor mandibulae A2 | palatoquadrate + orbital cartilage → Meckel's cartilage | **squamosal** → **dentary** |
| pseudotemporalis | palatoquadrate, dorsolateral → Meckel's cartilage | **parietal midline + first vertebrae** → **dentary** |
| depressor mandibulae | Meckel's cartilage | **dentary** |
| intermandibularis posterior | Meckel's cartilage | **dentary** |

The rows are the adult; the larval condition is in each `attachmentNote`. This is an
attachment shift **inside one species**, which is a different object from the
between-species shifts the Skeleton view diffs — and *A. mexicanum* is neotenic, so
its "adult" is a larval form that breeds and the shift happens anyway.

The pseudotemporalis is the striking one: its origin **moves dorsally** off the
palatoquadrate onto the parietal and the first vertebrae. A jaw muscle acquiring an
axial origin, which is why that row carries a vertebral element.

## Two differentiation events running backwards

- The **pseudotemporalis profundus** (the A3″ of fishes) is a distinct larval muscle
  from stage 39 and becomes *completely integrated* into the main body of the
  pseudotemporalis. Scored `single` in the adult, with the larval two-part condition
  in `divisionNote`.
- The **levator hyoideus** is likewise not a distinct adult muscle — it is inside the
  depressor mandibulae. Which is why that row has **two insertions on two different
  bones**: the dentary for the depressor proper, and the ceratohyal for the levator
  hyoideus fibres that still reach it at a steep angle at stage 44.

## The best single sentence in it, for this dataset

Their Fig. 3C: in the adult all the superficial ventral muscles are fused into **one
thin sheet**, and can only be divided by their origins — the mandible for the
intermandibularis posterior, the ceratohyal for the interhyoideus. Here the
attachment is not merely where the muscle ends; it is the only thing that makes two
muscles two.

## A nerve criterion that disagrees between taxa

CN V3 runs **between** the A2 and the A2-PVM in the axolotl. Jones et al. (2019) find
the pigeon's adductor mandibulae externus lateral to **both** CN V2 and CN V3, where
amniotes usually have it between them. The same nerve, used the same way as a
boundary criterion, giving different answers — recorded in the `divisionNote` of both
rows so the two can be read against each other.

## Sourced absences

The tongue muscles **hyoglossus and genioglossus are missing in both larva and
adult**. Carried as `variable` parts of `hypobranchial-muscles` with the absence in
their notes, rather than dropped — the absence is the observation. And the
**ceratomandibularis** is genuinely variable across urodeles: a distinct muscle in
some obligate neotenes, fused to the branchiohyoideus and/or the depressor
mandibulae in others, missing in others again. That is what Bauer (1997) is about,
and it is the next source for this column.

## Nomenclature bridge

Ceratobranchial → `cornu-branchiale`, basibranchial → `corpus-hyoidei`. Both were
bare records with no synonyms; the two names are now in `synonyms` so a search for
either resolves.

## Not scored

The **branchiohyoideus**, which shares an anlage with the depressor mandibulae and
levator hyoideus and runs from the ceratobranchial around behind the jaw joint to the
ceratohyal — it has no record here, and is noted on the depressor mandibulae row.
The **levator bulbi**, identified only in adults. The **commissurae terminales**, the
cartilage bars the levatores and depressores branchiarum arise from, which have no
element. The larval attachments throughout, which would need a schema for ontogenetic
stage rather than a second row.
