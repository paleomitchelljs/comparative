# Ghetie et al. (1976) — Anatomical atlas of domestic birds

## Citation

Ghetie V, Chitescu St, Cotofan V, Hillebrand A. 1976. *Atlas de anatomie a
pasarilor domestice / Atlas d'anatomie des oiseaux domestiques / Anatomical atlas
of domestic birds*. Editura Academiei RSR, Bucharest. Four languages: Romanian,
French, English, Russian.

## What it is, and what it is not

A **plate atlas** of four galloanserine birds — domestic fowl, turkey, duck and
goose. Osteology, arthrology, myology and the rest presented as labelled figures.

**It carries no descriptive myology.** A density check over the full 295-page
extraction returns essentially zero origin or insertion statements: the anatomy is
in the plates, not in prose. No attachment can be scored from text that does not
exist.

### It is mostly a turkey book, and it was mapped to a chicken

The myology section runs pp. 88–141. Of the 52 plates there whose caption names a
bird, **35 are the turkey** — *curcan* / *dindon*, *Meleagris gallopavo* — against
12 goose, 7 duck or drake, and 7 hen or cock. The wing series, the thigh, the
shank, the deep pelvis and the cervical plates are all turkey; the hen has the tail
and one deep-pelvis plate.

`attribute_species.py` mapped the whole book to `gallus-domesticus`, so it asserted
the wrong animal for about six plates in seven. Only one row was actually decided
that way — `deltoideus-scapularis`, which now takes *Gallus* from Abdala & Diogo's
avian exemplar under `speciesBasis: "survey"`, where it belongs — but the mapping
would have mis-attributed every row of any pass through the wing or hindlimb
plates. The source is out of `SOURCE_SPECIES`. A plate names its own bird in four
languages, so rows mined from it carry the binomial in prose.

This is the same error as Dick & Clemente (2016) and was found the same way: by
asking what animal the source actually says it looked at.

## Scored

5 occurrence rows on *Gallus domesticus* — pectoralis, supracoracoideus, deltoideus
scapularis, latissimus dorsi, coracobrachialis — carrying names and presence. The
attachments on those rows come from elsewhere; this source supplies the vocabulary
and the confirmation that the muscle is there.

## What the plates will and will not yield

They read cleanly as page images at 170 dpi — the same treatment that recovered the
Diogo tables. Numbered labels, four-language captions, layered dissections. So the
"figure-only means unmineable" verdict was wrong about the *legibility*. It is
still right about the *attachments*, and the distinction is the whole finding.

What a caption states, and can therefore be scored:

- the **species**, in four languages
- the muscle's **name**
- its **presence** in that bird
- its **layer** — captions say *stratul profund* against superficial outright,
  which is the roadmap's mass-and-layer spine handed over directly
- its **face** — *facies dorsalis / ventralis / medialis / lateralis*

What no caption states is where the muscle attaches. Reading an origin off a
drawing is an inference by whoever is looking, not an observation by Gheție et al.,
and entering it would break the same rule as inventing a `side`.

So this is a **presence, name and layer source for four birds**, not an attachment
source for one. Worth knowing before a pass is planned around it: mining it will
*lower* the Aves `%att`, because it adds present occurrences with nothing scored
beneath them. That is the figure behaving correctly, not a regression.

## The consequence for the Aves column

The way to grow the avian column is the species that are actually described — the
crane (Fisher & Goodman 1955, whose text layer is fine; see its note), the screamer
(Widrig et al. 2026), the swan (Matsuoka & Hasegawa 2007), the loon (McKitrick
1991), the penguin (Schreiweis 1982), the tinamou (Widrig et al. 2023), the pigeon
(Jones et al. 2019), the kiwi (Vanden Berge 1982).

## Relevance to comparative anatomy teaching

Genuinely useful in a teaching context, which is worth separating from its
uselessness here: labelled plates in four languages are a good way to learn avian
topography. It is a reference for what a structure *looks* like, not for where a
muscle attaches.
