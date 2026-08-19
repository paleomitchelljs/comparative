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

*Prestosuchus chiniquensis*, a well-preserved specimen, reconstructed against
myological descriptions of extant birds and crocodylians — the archosaur extant
phylogenetic bracket, under **explicit Witmer inference levels**.

## Findings

**Of 16 muscle groups analysed, 13 were recognised as present and homologous in
both extant archosaur groups**, and two more only in the crocodylian line, giving
15 reconstructed in the fossil.

The paper's own emphasis is that particularities of the pelvic girdle and hindlimb
of *Prestosuchus* give a **distinct arrangement of origin and insertion sites** —
so the reconstruction is not simply the crocodylian condition transferred.

## Scored, and what is not

**1 occurrence row**, `puboischiofemoralis-internus`, reconstructed at Witmer
inference level I over a muscular scar on the craniolateral face of the greater
trochanter, on the proximolateral tuberosity of the femur.

**One row from a 28-page reconstruction is a text-extraction problem, not a source
problem.** The paper's two-column layout interleaves badly under `pdftotext`, so
only claims that could be verified against their surrounding context were scored.
The rest of the reconstruction is still to be mined **by hand**, and it is the
largest unmined piece of fossil archosaur myology in `papers/`.

The fix is in `MINING.md`: use plain `pdftotext` without `-layout` where reading
order matters, and check that a heading sits above its own text.

## Limitations

- **A reconstruction.** Every row is `inferred`, and the fourth-trochanter class of
  correlate is the only direct evidence.
- **One specimen.**

## Relevance to comparative anatomy teaching

Worth pairing with **Burch (2014)** as the same job done on the two sides of the
archosaur split, with two different inference vocabularies — Witmer levels here,
maximum-likelihood proportional probabilities there — and it is instructive to ask a
student which they would trust and why.
