# Allen, Kilbourne & Hutchinson (2021) — Pelvic limb muscle moment arms in bird-line archosaurs

## Citation

Allen VR, Kilbourne BM, Hutchinson JR. 2021. The evolution of pelvic limb muscle
moment arms in bird-line archosaurs. *Science Advances* 7: eabe2778.
doi:10.1126/sciadv.abe2778. Open access.

## Question

Bipedal locomotion along the line to birds shifted from hip-based to knee-based
mechanisms. Which individual muscles produced that shift, and when along the tree
did each change happen?

## Taxa and material

**13 three-dimensional musculoskeletal models** of bird-line archosaur hindlimbs,
from *Marasuchus* to extant birds, carrying **35 locomotor muscles**. Not a
dissection: a modelling study built on published attachment data.

## What it gave this dataset

**Avian nomenclature, from their Table 1.** The table gives 25 crocodylian↔avian
correspondences, and it is the source for the avian names on 13 hindlimb records
here. It settled a naming question the dataset had left open — the avian column is
now almost entirely named.

**Corroboration of a contested homology it was not written to test.** They equate
the crocodylian extensor digitorum longus with the avian *m. tibialis cranialis*,
which is Hattori & Tsuihiji's (2021) reading rather than the classical one. The
two papers work on different problems — homology versus moment arms — so the
agreement is not circular. Both records stay `contested`; the balance of evidence
has moved.

**Two subdivisions worth having.** They split the avian caudofemoralis into *pars
caudalis* (= crocodylian caudofemoralis longus) and *pars pelvica* (= brevis), and
give the crocodylian correspondences for the puboischiofemoralis internus 1–2 and
externus 1–3 and the iliotibialis 1–3 groups.

## Findings worth carrying

Two results the paper supports, both of them changes in leverage rather than in
anatomy:

- **Knee flexor moment arms decreased relative to knee extensors'** from early
  theropods to birds.
- **Medial long-axis rotator moment arms at the hip increased**, trading off
  against decreased hip extensor leverage. Hip medial-rotator moment arms roughly
  double along the bird line.

**Caudofemoralis reduction is the defining event.** Its leverage declines across
several nodes, tracking the shortening of the tail to the pygostyle and the shift
to a knee-driven gait with the femur held near horizontal.

## Limitations, and why the rows are thin

**This is a model, not a description**, and its attachments are three-dimensional
coordinates rather than statements about named bone surfaces. That is why almost
every row it supports here carries a name, a presence and a division but **no
attachment rows** — there is nothing in the paper to score as `{element, side,
landmark}` without inventing the correspondence.

Reading it as a row source would be a category error, and `WORKLIST.md` lists it
among the sources that cannot yield species-level attachments.

## Relevance to comparative anatomy teaching

The right paper for showing that anatomy is not function: the muscles barely
change while their leverage changes enormously, and the locomotor transition lives
in the second fact. Its method is also the template for roadmap phase 4 — fit
geometric primitives to joints, trace muscle paths from origin to insertion,
compute moment arms across joint angles — which is what this dataset's attachment
records are ultimately for, and the argument for chasing `side` and `landmark`
resolution rather than treating them as decoration.
