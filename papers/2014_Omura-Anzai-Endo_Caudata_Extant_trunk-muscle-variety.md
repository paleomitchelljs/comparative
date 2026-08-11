# Omura, Anzai & Endo (2014) — Functional and morphological variety in trunk muscles of Urodela

*J. Vet. Med. Sci.* 76(2): 159–167. doi:10.1292/jvms.13-0211. Open access.
Source key: `omura-etal-2014`

## Why this one matters here

It is the only source in `papers/` that dissects ***Necturus maculosus***, and the
axial column was the region least served by everything else. The Caudata axial
records were built on *Taricha torosa* (Walthall & Ashley-Ross 2006) and
*Ambystoma* (Schilling 2011); this paper shows that the trunk is precisely where
those two do not stand in for the clade.

## Sample

Five species, five families, three habitat classes, n = 3 each:

| Species | Habitat |
|---|---|
| *Amphiuma tridactylum* | aquatic |
| *Necturus maculosus* | aquatic |
| *Cynops pyrrhogaster* | semi-aquatic |
| *Hynobius nigrescens* | terrestrial |
| *Ambystoma tigrinum* | terrestrial |

Method is gravimetric: every trunk muscle dissected from one side and weighed,
expressed as a percentage of total trunk muscle mass. Not architecture — no
fascicle lengths, no pennation, no PCSA — so nothing here fits the schema's
`architecture` block, and it is recorded as notes rather than forced into fields
it does not fill.

## What was scored into `data/`

**1. The external oblique is polymorphic within Caudata.**
Undivided in *Necturus* and *Hynobius*; split into a *superficialis* and a
*profundus* in *Amphiuma*, *Cynops* and *Ambystoma*. The lateral hypaxial stack
as a whole runs to two, three or four layers by species. Critically the split
does **not** track habitat — one aquatic and one terrestrial species share the
undivided condition — so this is polymorphism, not a functional grade.

Recorded as `division: "variable"` on the Caudata occurrence of
`obliquus-externus`, with both parts marked `membership: "variable"`. Scoring the
clade from any single exemplar would have manufactured a differentiation event on
whichever branch that exemplar sat on.

**2. The rectus abdominis is not separable in the aquatic species.**
In *Amphiuma* and *Necturus* it could not be distinguished from the external and
internal obliques. It separated cleanly in the semi-aquatic and terrestrial
species. Recorded as a note on the Caudata occurrence of `rectus-abdominis`,
which otherwise describes *Taricha*, where it is discrete.

This is the one most likely to matter at a bench: a student following a *Taricha*
or textbook description on a *Necturus* will look for a rectus abdominis that is
not there as a separate sheet.

**3. Mass apportionment tracks habitat.**
Lateral hypaxial layers take roughly a quarter of trunk muscle mass each in the
aquatic species against under a tenth in the terrestrial ones; the rectus
abdominis runs the other way, under 5% in aquatic and 12–13% in terrestrial.
Epaxial (*M. dorsalis trunci*) and subvertebral mass both rise with
terrestriality. Recorded as a note on the Caudata occurrence of
`hypaxial-musculature`.

The authors' functional reading: a trunk held off the ground between two girdles
needs a ventral tie and dorsal stabilisation against gravity; a swimming trunk
needs lateral benders instead.

## What was NOT scored, and why

- **No attachments.** The paper gives positions and relations, not origins and
  insertions at the resolution the attachment rows need. The Caudata axial rows
  remain Walthall & Ashley-Ross's.
- **The weight ratios are not architecture.** A percentage of trunk muscle mass
  is not a mass in grams, a PCSA or a fascicle length, and putting it in
  `architecture` would let it be read as force or excursion data. It is in prose.
- **`M. subvertebralis`, `M. interspinalis`, `M. intertransversarius` and
  `M. rectus lateralis` have no records of their own.** They are named and
  weighed here and would each need a homology group, a consensus description and
  a cross-taxon assessment. `hypaxial-musculature` currently carries the
  subvertebral portion as a `part` only. Splitting them out is the obvious next
  step for the axial region and is not done.
- **`M. rectus lateralis` is reported present in *Cynops* and *Ambystoma*** and
  is not mentioned for the other three; the paper excludes it from the mass
  ratios because it is small. Absence of mention is not absence, so nothing was
  scored from it.

## Terminology note

The paper uses *M. obliquus externus* for the undivided layer and
*M. obliquus externus superficialis* / *profundus* for the split condition —
i.e. the same name means "the whole layer" in one species and "the outer half of
it" in another. That is the naming problem this dataset exists to hold, and it is
why the parts are attached to the occurrence rather than given records.
