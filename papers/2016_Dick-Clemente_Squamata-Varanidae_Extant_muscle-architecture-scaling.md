# Dick & Clemente (2016) — Scaling of muscle architecture in monitor lizards

## Citation

Dick TJM, Clemente CJ. 2016. How to build your dragon: scaling of muscle
architecture from the world's smallest to the world's largest monitor lizard.
*Frontiers in Zoology* 13: 8.

## Question

Muscle design is shaped by conflicting demands for support and propulsion, and the
conflict sharpens with size: mass scales faster than area, so a geometrically
scaled-up animal would run musculoskeletal stresses close to failure. How do
varanids avoid that?

## Taxa and material

**22 hindlimb muscles in 27 individuals from 9 species of varanid**, spanning three
orders of magnitude in body mass — from the 7.6 g *Varanus brevicauda* to the 40 kg
*Varanus komodoensis*. Mass, fascicle length, pennation angle and PCSA for each.

## Findings worth carrying

**Larger varanids increase the relative force-generating capacity of three muscle
groups** — femur adductors, knee flexors and ankle plantarflexors — with scaling
exponents greater than geometric similarity predicts. That is how size-related
increases in stress are mitigated: not by changing the skeleton but by
disproportionately investing in particular muscles.

The result belongs beside the ROADMAP argument that mass and layer, not
attachment, are the stable axis. Here the attachments are constant across three
orders of magnitude and the architecture is what changes.

## Scored

8 occurrence rows — iliofemoralis, caudofemoralis, iliofibularis, femorotibialis,
ambiens, adductor femoris and their neighbours, with attachments from the paper's
Table 1. Six sit on `varanidae-generalised` and two on *V. komodoensis*; see below
for why.

## The species attribution, and how it was settled

**This source was mapped to an animal it never names.** Six hindlimb rows carried
its Table 1 on *Varanus exanthematicus* with `speciesBasis: "source"`, an
attribution borrowed from Cieri's monitor. Table 1 is a compilation *of the varanid
hindlimb* assembled from four earlier papers — Snyder (1954), Gans et al., Reilly
on *Sceloporus clarki*, and Anzai et al. on Cuban *Anolis* — two of which are not
varanids at all.

**Resolved to `varanidae-generalised`.** The caption is explicit that the table is
a compilation, and it carries no per-muscle provenance, so there is no underlying
species to recover: the "find the animal" branch is closed, not merely unattempted.
That leaves the disposition the schema already provides for a source describing a
clade rather than a specimen — `generalised: true` on the species and
`speciesBasis: "generalised"` on every row of it, which the validator enforces both
ways. `dick-clemente-2016` is out of `SOURCE_SPECIES` entirely, so no future row
citing it inherits a monitor nobody dissected.

The two *V. komodoensis* rows are untouched. Their species comes from Tomańska
et al. (2025) naming the animal in prose, and this paper is supporting argument on
them rather than the attachment source.

Nothing about the **architecture** is affected. That is this paper's own
measurement across 27 individuals, and it remains attributable to the nine species
it was taken from.

## Limitations

- **The attachment table is a compilation, not a dissection** — see above. The
  *architecture* is this paper's own measurement and is trustworthy; the
  attachments are inherited.
- **Nine species, but one clade.** Sprawling tetrapods generally are not sampled.

## Relevance to comparative anatomy teaching

The counterpart to Hudson et al. (2011) on the cheetah: same question, opposite
posture. Named by Mansuit & Herrel (2021) as a key architecture source, and one of
the sources that would populate roadmap phase 5 if the schema carried more than one
specimen per record.
