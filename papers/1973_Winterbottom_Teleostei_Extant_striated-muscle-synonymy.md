# Winterbottom (1973) — A descriptive synonymy of the striated muscles of the Teleostei

## Citation

Winterbottom R. 1973. A descriptive synonymy of the striated muscles of the
Teleostei. *Proceedings of the Academy of Natural Sciences of Philadelphia* 125:
225–317.

## What it is

93 pages reconciling the competing naming schemes for teleost striated muscle,
organised by region — cheek, jaws, branchial arches, pectoral fin, pelvic fin,
body — with each muscle given a description and the list of names other authors
have used for it.

**It is a synonymy, not a dissection.** That distinction governs how every row from
it is scored here.

## Why it matters to this dataset

**It is the single richest source of synonyms in the bibliography**, and synonyms
are how a reader arrives from an old paper. Every name in it is indexed, so
searching a term from a nineteenth-century description lands on the right modern
record and says which name matched.

It also makes actinopterygian muscle names tractable at all. Without it the fish
end of the tree is a set of records whose names cannot be matched to the
literature.

`homologyScope: true`: reconciling nomenclature across a group is its stated
purpose, and it therefore counts as a source that can adjudicate a homology.

## Scored, and how

6 occurrence rows, all on **`teleostei-generalised`** with `speciesBasis:
"generalised"`, covering the six ancestral paired-fin muscles: abductor
superficialis and profundus, adductor superficialis and profundus, arrector
ventralis and arrector dorsalis.

**Those rows previously claimed `speciesBasis: "source"`, which means a
single-species study.** So the rows least like an observation were asserting the
opposite. This is the case that `generalised` exists for, and the validator now
enforces it in both directions — a species record flagged `generalised: true` may
only carry `generalised` rows, and no other record may carry them.

The attachment rows record the teleost *condition* rather than an animal: the
abductor superficialis arises chiefly or entirely on the lateral cleithrum and the
posterolateral side of its anterolateral flange, occasionally from the coracoid or
even the radials, with a diffuse insertion in generalised fishes that consolidates
into tendons on the outer anterior bases of the fin rays in more derived ones.

## Limitations

- **No animal stands behind these rows.** Read them as the group's condition,
  which is what the `generalised` flag says.
- **Teleosts are one branch of Actinopterygii.** Nothing here bears on *Polypterus*
  or the other non-teleost actinopterygians the fin records also cover.

## Relevance to comparative anatomy teaching

The demonstration that a naming problem can be a research programme. It is also
the fish-end counterpart to Abdala & Diogo's Tables 1–3 and to Werneburg's turtle
synonymy — three attempts at the same job in three different groups, and worth
comparing for how differently each author decides two names denote one muscle.
