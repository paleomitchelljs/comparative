# Pereyra, Bona, Cerda & Desántolo (2019) — Osteohistological correlates of muscular attachment in terrestrial and freshwater Testudines

*Journal of Anatomy* 234: 875–898. doi:10.1111/joa.12975. PMC6533408.
Source key: `pereyra-etal-2019`

## What it is not

Reached for as the largest Testudines row source. **It is not one.** Density check
on the PDF: 85 origin/insertion mentions in 15,000 words, against 270 in Meers's
26 pages and 445 in Prikryl's 40. The muscles appear as *labels on attachment
sites*, not as descriptions with an origin and an insertion.

Recording that here so nobody reaches for it again on the strength of the title.
`role` in `sources.json` says the same thing.

## What it is

The evidence layer under the `correlate` flag. The authors section the pectoral
girdle and humerus of *Chelonoidis chilensis* (terrestrial), *Phrynops hilarii*
and *Hydromedusa tectifera* (freshwater) and classify **Sharpey's fibre
orientation at each muscle attachment** into three patterns:

| Type | Fibre arrangement |
|---|---|
| I | Parallel, at right or acute angles to the subperiosteal margin |
| II | Organised cross-pattern, two main orientations |
| III | Disorganised cross-pattern, more than two orientations |

Their Table 2 maps element × attachment × pattern across the three species.

This is what `correlate: true` is asserting when the dataset says an attachment
leaves a recognisable trace — and it is the first source here that tests the
claim histologically rather than by inspection.

## Why that matters for the gaps

`WORKLIST.md` lists the flagged correlates that carry no muscle: scapular
spine, coronoid process, lesser trochanter, trochanteric fossa, linea aspera,
tibial tuberosity, and others. Those are the sites a palaeontologist looks at
first, and the dataset currently says nothing about what pulls on them. This
paper is the way into that list for the turtle pectoral girdle, and its method
generalises.

It also bears on the caution already in `METHODS.md` from Leavey et al. (2024) —
that a correlate locates an attachment but does not size the muscle. Pereyra et
al. add the other half: which attachments record themselves in bone at all, and
how legibly.

## Not mined

No rows. Testudines stays at 26%; the sources that would move it are still
Werneburg (cranial) and something descriptive for the forelimb, which the corpus
does not have.
