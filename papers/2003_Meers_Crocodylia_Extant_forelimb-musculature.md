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

## A conflict, now resolved

Meers puts the trapezius insertion "dorsal to the acromion" in a crocodylian.
`skeleton.json` used to record the acromion as **absent** in Crocodylia, the
validator rejected the row, and the landmark went unasserted while the
disagreement sat in the occurrence note.

**Resolved in favour of Meers.** He is not using the word loosely: he names the
acromion four times as a crocodylian scapular landmark, gives it a lateral
surface with an upper and lower portion, and hangs two muscle origins on it —
the deltoideus clavicularis arises from it along the cranial margin of the
scapula, and the supracoracoideus brevis from the lower part of its lateral
surface. Schreiweis (1982) independently gives three penguin muscles an origin
on the acromial process of the scapula, and Widrig et al. (2023) describe the
tinamou acromion projecting cranially. The element is now scored present in
Crocodylia and Aves.

Two consequences worth noting:

- **The trapezius still gets no acromion row.** Meers places that insertion
  *dorsal to* the acromion, on the cranial edge of the scapula — the acromion is
  his reference point, not the attachment site. Rescoring the bone does not
  license the row that first exposed the problem.
- **Two rows were mined that the old scoring had blocked**: the alligator
  deltoideus clavicularis, and the three-headed supracoracoideus complex, whose
  brevis carries the acromion origin. Both are new occurrences from this paper.

The homology caveat is on the element: the archosaur acromion and the therian
one occupy the same position and carry the same deltoid-series origins, but the
therian one is the distal end of a scapular spine that archosaurs do not have.
It is scored on topological correspondence, and the element note says so.
