# Liparini & Schultz (2013) — Thigh musculature of *Prestosuchus chiniquensis*

## Citation

Liparini A, Schultz CL. 2013. A reconstruction of the thigh musculature of the
extinct pseudosuchian *Prestosuchus chiniquensis* from the Triassic of southern
Brazil. *Geological Society, London, Special Publications* 379: 441–468.

## Why it was reached for

**The first source here for the loricatan grade** — a large terrestrial
pseudosuchian from the Middle Triassic, on the crocodylian side of the archosaur
split and well away from the bird line the other fossil columns sample.

## Taxa and material

*Prestosuchus chiniquensis*, specimen UFRGS-PV-0629-T, reconstructed against the
archosaur extant phylogenetic bracket — Crocodylia and Aves, with Lepidosauria as
outgroup — under **explicit Witmer inference levels**. No dissections were carried
out; the extant myology is taken from Gadow, McKitrick and Romer, and the homology
scheme from Rowe (1986), Hutchinson & Gatesy (2000), Hutchinson (2001a, b) and
Kischlat (2003).

## Re-mine of 2026-08-20 — the accounting

**16 muscles in Table 2, 16 filed, 0 parked.**

| | |
|---|---:|
| Muscle groups reconstructed as present | 15 |
| Reconstructed as absent (`M. pubo-tibialis`) | 1 |
| **Total the paper reconstructs** | **16** |
| Filed onto a record | 16 |
| Parked | 0 |

They merge into **13 occurrences**, because three records take two of the paper's
entries each: the two parts of the puboischiofemoralis internus, the two heads of
the ambiens, and the flexor cruris beside the first and second flexores tibiales
interni. Each source name is kept in `data/mapping/`, so the paper's own
abbreviations remain findable.

### The previous verdict was wrong, and it named the fix itself

The note this replaces recorded **one** scored row and explained it:

> One row from a 28-page reconstruction is a text-extraction problem, not a source
> problem. The paper's two-column layout interleaves badly under `pdftotext`, so
> only claims that could be verified against their surrounding context were scored.
> […] The fix is in `MINING.md`: use plain `pdftotext` without `-layout` where
> reading order matters.

The diagnosis was right and **nobody ran the command**. Plain `pdftotext` gives a
clean reading order with every heading above its own text, and the paper turns out
to carry **Table 2 — origin, insertion and inference level for all sixteen
muscles** — which extracts perfectly well under `-layout`, where the columns matter.
Both routes were available the whole time.

That is worth generalising: **a note saying a source cannot be mined is a claim
about tooling, and tooling claims expire.** This one cost 15 of 16 muscles for the
one row that happened to survive a bad extraction.

### What the reconstruction is careful about, and the rows with it

Liparini & Schultz decline to reconstruct more often than they reconstruct, and
those refusals are scored as refusals:

- **Both parts of the puboischiofemoralis internus carry an insertion and no
  origin.** For each, the origin is an unresolved ambiguity between the avian and
  the crocodylian condition, and the authors will not call either ancestral —
  because if the whole deep dorsal group arose laterally on the ilium in the
  saurian ancestor, then *both* living conditions are derived, and whether the
  shift happened once before the archosaur split or twice after it is open.
- **The ambiens pars II carries an origin and no insertion**, because it inserts on
  the femoro-tibialis, muscle to muscle, as in crocodylians and lepidosaurs.
- **The adductores femores carry one insertion for two heads**, the authors stating
  they could not distinguish separate sites.
- **The caudofemoralis longus origin is recorded as the caudal series with no
  count**: the relevant vertebrae are not preserved, and the third-to-fifteenth
  range is read off living archosaurs rather than off this animal.
- **`M. pubo-tibialis` is filed `present: "no"`.** An asserted absence, not a blank.

Only two muscles reach inference level I at *both* ends — the ambiens and the
ilio-tibialis — and both do it on muscle scars. Everything else is level I at the
insertion and II or II′ at the origin, which is the signature of a pelvis whose
muscle scars are femoral and tibial rather than iliac.

### What it settles that the bird-line reconstructions cannot

Two muscles here are absent from *Tyrannosaurus* and *Poposaurus* alike:

- **`M. pubo-ischio-tibialis`**, which among living archosaurs survives only in
  Crocodylia. Present here, absent in *Tyrannosaurus* for want of any scar —
  which places its loss on the avemetatarsalian line **before theropods**.
- **`M. ambiens pars II`**, which Carrano & Hutchinson treat as a crocodylian
  autapomorphy with no avian homologue. Liparini & Schultz restore it on the
  argument that the crocodylian condition is plesiomorphic and matched in
  lepidosaurs.

The paper also disagrees with Schachner et al. (2011) on *Poposaurus* in a way that
has a functional consequence: the PIFI 1 insertion is caudomedial here and
craniolateral there, which reverses the muscle's rotational moment from supination
to pronation.

### Skeleton entries this pass added

`fourth-trochanter`, `cnemial-crest` and `iliofibular-tubercle` had no
`pseudosuchia-stem` presence, and the fourth trochanter defaults to absent — so
scoring the caudofemorales onto it failed validation. All three are figured and
attached-to in this paper, the fourth trochanter at inference level I from muscle
scars, and all three now carry the taxon with this source cited.

## Limitations

- **A reconstruction.** Every present row is `inferred`. The fourth trochanter is
  the only correlate of the class that would survive independent of the bracket.
- **One specimen**, and the caudal series incomplete.

## Relevance to comparative anatomy teaching

Worth pairing with **Burch (2014)** as the same job done on the two sides of the
archosaur split, with two different inference vocabularies — Witmer levels here,
maximum-likelihood proportional probabilities there — and it is instructive to ask a
student which they would trust and why. It is also the clearest case in the corpus
of a paper whose *refusals* are the data: a student can be asked why a muscle with
a known insertion and two candidate origins is better recorded with none.
