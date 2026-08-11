# Meers (2003) — Crocodylian forelimb musculature and its relevance to Archosauria

*The Anatomical Record Part A* 274A: 891–916. doi:10.1002/ar.a.10097
Source key: `meers-2003`

## Why it matters here

Meers is one of the six naming schemes Abdala & Diogo's Tables 1–3 exist to
translate between, and it was the only one this dataset did not hold in full. It
is a proper descriptive myology — attachment sites, innervation and function for
the whole crocodylian forelimb. **Crocodylia went 58% → 75%.**

Scored (11): `latissimus-dorsi`, `protractor-pectoralis`, `abductor-digiti-minimi`,
`lumbricales`, then the manus — `extensores-digitorum-breves`,
`flexores-breves-superficiales`, `flexores-breves-profundi`,
`contrahentes-digitorum`, `intermetacarpales`, `dorsometacarpales`,
`abductor-pollicis-brevis`.

## How the manus was done

Meers uses crocodylian names that do not appear in this dataset —
*abductor metacarpi I*, *flexores digitorum intermedii*, *interossei dorsalae*.
Mapping them by eye would have been guesswork, so every manus row was bridged
through **Abdala & Diogo's Table 1**, whose *Caiman latirostris* column gives
explicit "sensu Meers, 2003" equivalences:

| This record | Meers 2003 |
|---|---|
| `abductor-pollicis-brevis` | abductor metacarpi I |
| `abductor-digiti-minimi` | abductor metacarpi V |
| `flexores-breves-superficiales` | flexores digitorum breves superficiales |
| `flexores-breves-profundi` | flexores digitorum profundus (+ possibly flexor digitorum intermedius digiti V) |
| `contrahentes-digitorum` | flexores digitorum intermedii |
| `intermetacarpales` | *part of* interossei dorsalae |
| `dorsometacarpales` | *part of* interossei dorsalae |

**Two caveats are in the data, not just here.** Abdala & Diogo split the interossei
dorsalae between `intermetacarpales` and `dorsometacarpales` without saying which
slips go where, so both carry the same rows and each note says the rows describe
the complex rather than that record alone. And `extensores-digitorum-breves` has
**no** published equivalence in Table 1 — it is scored from Meers's *extensor
digitorum profundi* on shared topology (metacarpal origin, ungual insertion, deep
to the long extensors), and its note says so explicitly.

## Findings worth carrying

**The latissimus dorsi insertion is a reliable fossil correlate.** It leaves a
large scar about a quarter of the shaft length from the humeral head, as a
tubercle or a pit, **present even in hatchlings**.

**Two manus muscles are inconsistent within a species.** The flexores digitorum
intermedii of digits IV/V and V were found commonly but not always, even within
*Alligator mississippiensis*; digit V appeared to lack a flexor digitorum brevis
superficialis altogether.

## A conflict left open

Meers puts the trapezius insertion "dorsal to the acromion" in a crocodylian.
`skeleton.json` records the acromion as **absent** in Crocodylia, and the
validator rejected the row — the same check that once caught a crocodylian
muscle attached to a clavicle. The landmark is not asserted and the disagreement
is written into the occurrence note. One of the two is wrong: either crocodylians
have an acromion process this dataset denies them, or Meers is using the term
loosely for the cranial scapular margin. It needs a decision, not a silent fix.
