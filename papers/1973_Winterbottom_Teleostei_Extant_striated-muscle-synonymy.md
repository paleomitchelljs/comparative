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

11 occurrence rows, all on **`teleostei-generalised`** with `speciesBasis:
"generalised"` — the six ancestral paired-fin muscles, and five cheek muscles added
on 2026-08-20 (see below). The fin rows cover: abductor
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

## The cheek muscles, mined 2026-08-20 — and a record that had to be made

Five more rows, all on `teleostei-generalised`, and **a new record for the field they
belong to**: `constrictor-hyoideus-dorsalis`.

This dataset held `levator-arcus-palatini` for the *constrictor dorsalis* — mandibular
arch, CN V — and `interhyoideus` for the *constrictor hyoideus ventralis*, and nothing
at all for the dorsal division of the hyoid constrictor between them. Fifteen rows
from Jayaram et al. (1983) sat parked on `no-record` waiting for it; they were
promoted the same day.

**Winterbottom treats the named muscles as differentiations of one embryonic sheet**,
after Edgeworth (1935): the adductor arcus palatini from its anterior portion, the
levator and adductor operculi from its posterior portion, and the adductor
hyomandibulae, extensor tentaculi and retractor arcus palatini as bundles separating
from those. Every one takes the ramus hyomandibularis of CN VII. He says outright that
the boundaries do not hold — the levator operculi "may not be separate from the
adductor arcus palatini or from the adductor operculi", the adductor operculi "may be
continuous anteriorly with the adductor arcus palatini" — so the six are the record's
`parts`, named because the literature names them and not because they are separable.

**The adductor hyomandibulae is the case worth reading.** In generalised lower
teleosts the adductor arcus palatini runs prootic to hyomandibular and *is*
morphologically an adductor hyomandibulae; the name only becomes inappropriate once
the muscle expands forward along the floor of the orbit, and Winterbottom applies
"adductor arcus palatini" to both conditions for that reason. **Same fibres, two
names, and which one applies is a fact about how far forward the muscle reaches.**

The open question is left open on the record: whether the tetrapod depressor mandibulae
and stapedius are this same field. Both are CN VII and dorsal hyoid arch, which would
make this their fish counterpart — but no source cited here says so, and the tetrapod
records stay separate until one does.

## Still to mine — most of it

The paper covers the whole teleost muscular system and this has taken the six fin
muscles and five of the cheek. Remaining, by his own table of contents: the rest of
the cheek (dilatator operculi, retractor tentaculi, retractor arcus palatini), the
ventral head (intermandibularis, protractor hyoidei, the three hyohyoidei), the dorsal
and ventral branchial series (levatores externi and interni, obliqui, transversi,
recti, sphincter oesophagi, retractor dorsalis), and the body and median-fin
musculature. **It is the largest body of scorable teleost myology in the corpus** and
every one of those names carries a full synonymy.

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
