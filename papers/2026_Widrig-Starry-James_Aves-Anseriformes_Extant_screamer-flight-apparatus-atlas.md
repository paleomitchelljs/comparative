# Widrig, Starry & James (2026) — Wing apparatus of the southern screamer

## Citation

Widrig K, Starry A, James HF. 2026. Anatomical atlas and three-dimensional
musculoskeletal model of the flight apparatus in the southern screamer
(Anseriformes: *Chauna torquata*). *Integrative Organismal Biology* 8(1): obag038.
Open access.
Source key: `widrig-etal-2026`

## Two things about this entry were wrong before it was opened

**The key said Starry & James.** The first author is Klara Widrig. Renamed from
`starry-james-2026`, which was safe to do because nothing cited it.

**It was filed as a musculoskeletal model, and warned against on that basis.** The
old `role` line grouped it with Allen et al. (2021) and Hutchinson et al. (2015)
and told the reader to check before scoring, on the reasoning that a model is a
different kind of source from a dissection. That is right about those two and
wrong about this one. This is a **diceCT digital dissection** of a fluid-preserved
specimen, with attachments described from the scan and checked against previously
dissected specimens — the same kind of source as Jones et al. (2019) on the pigeon
head and Widrig et al. (2023) on the tinamou, both of which are row sources here.
The 3D model is built on top of the atlas, not instead of it.

It had never been cited, so the warning had been doing its work for one pass and
nobody had checked it.

## Material

*Chauna torquata*, USNM 666527, diceCT. Previously dissected USNM 226502 (partial,
juvenile) and USNM 508683 (adult, fully skinned) were referenced, and the
**osteological correlates were read off dry skeletons**, USNM 345619 and 646637.

## Why it matters beyond one bird

Anhimids are early-diverging anseriforms and the English-language literature on the
anseriform wing is thin — the authors quote Zusi & Bentz (1978) remarking on the
same gap nearly half a century ago. *Chauna* soars rather than using the rapid
continuous wingbeat of most anseriforms, so its wing myology is a functional
outlier within the clade.

## Mined in full

**Every muscle the paper describes is extracted** — 38 blocks — so it should not
need reading again except to check this pass. 20 filed as *Chauna torquata*
occurrences, 16 parked in `observations.json`, and two folded into rows that
already existed.

### Filed (20)

Girdle and arm: `pectoralis`, `supracoracoideus`, `latissimus-dorsi`,
`scapulohumeralis-anterior`, `scapulohumeralis-posterior`, `subcoracoscapularis`
(subscapularis + subcoracoideus, which share a tendon and one rugose scar),
`deltoideus-scapularis`, `coracobrachialis` (cranialis + caudalis),
`biceps-brachii`, `brachialis`, `triceps-brachii` (scapulotriceps +
humerotriceps).

Antebrachium and hand: `pronator-teres`, `epitrochleoanconeus`,
`flexor-carpi-ulnaris`, `flexor-digitorum-longus`, `supinator`,
`extensor-antebrachii-carpi-radialis`, `extensor-antebrachii-carpi-ulnaris`,
`extensor-digitorum`, `abductor-pollicis-brevis`.

Its nomenclature is modern *Nomina Anatomica Avium*, so most rows bridged
straight onto the *Gavia*, *Cygnus* and *Gallus* names already on those records.
**The avian dorsal epicondyle is the ectepicondyle and the ventral epicondyle the
entepicondyle**, and the rows are translated accordingly.

### The extraction needed page images, and nearly went wrong

The PDF is two-column and `pdftotext` reading order **displaces some blocks from
their headings**. Three came out empty and, worse, the supinator and extensor
carpi radialis descriptions had swapped places — a radial insertion that belongs
to the supinator sat under the extensor carpi radialis heading, which would have
put an observation on the wrong record. Six blocks were re-read from page images
(pp. 7 and 12) and are marked as verified that way.

This is the case `MINING.md` warns about under "column order". The check that
caught it was reading the block against the muscle it claimed to describe.

### Parked (16), and one that matters

| Blocked on | n |
|---|---:|
| `no-record` | 12 — the propatagial complex, the ulnometacarpales, the ectepicondyloulnaris, the alular set |
| `nomenclature` | 3 — the digit-named hand muscles and the deltoideus pars minor |
| `homology` | 1 — see below |

**`M. propatagialis` is the one worth acting on.** This dataset has no record for
the propatagium, and Fisher & Goodman's tensor patagii longus and brevis are
parked on the same gap — so **two sources now describe the same structure with
nowhere to put it**, which is enough to justify creating the record. What it needs
first is a decision about whether the propatagialis is one homology group or
several, and whether `humeroradialis`, which carries "M. tensor propatagialis" as
a *Chauna* name, is part of it or a different muscle.

**`M. pronator profundus` is parked on a contradiction already in the data.**
`pronator-quadratus` carries "Pronator profundus" for *Gavia* and
`pronator-accessorius` carries "M. pronator profundus" for *Cygnus*. Filing the
*Chauna* row means choosing between them, and that is a homology question this
paper does not address. Worth settling before a third bird is added to it.

## Nomenclature

Modern *Nomina Anatomica Avium* throughout, which maps straight onto the dataset's
existing *Gavia* and *Cygnus* rows — `pronator-teres` already carried "Pronator
superficialis" for both. No 1955-style translation needed, unlike Fisher & Goodman.

## Relevance to comparative anatomy teaching

The clearest available demonstration that a muscle scar is readable as a muscle.
Pair with Pereyra et al. (2019) on the histology of attachment sites, and use it
when the question is how a palaeontologist gets from a bone to a reconstruction.
