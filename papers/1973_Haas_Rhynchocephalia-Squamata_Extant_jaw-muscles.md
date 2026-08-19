# Haas (1973) — Muscles of the jaws and associated structures in the Rhynchocephalia and Squamata

*Biology of the Reptilia* **4** (Morphology D), ch. 5, pp. 285–490. Academic Press.

Source key: `haas-1973`.

## What was acquired

Same mechanism as volume 21: one PDF per page from
[carlgans.org](https://carlgans.org/biology-reptilia-full-content/), **offset +9
for volume 4** (chapter page 1 is `page10`).

**The whole chapter is here** — 206 pages, chapter pp. 285–490, PDF pages
294–499, verified continuous with no gaps. It was fetched in two passes: the
Rhynchocephalia section and the synonymy tables first, then the remaining 175
pages. 206 requested in total, 206 returned as PDFs, no Cloudflare
interstitials.

| chapter pp. | what |
|---|---|
| 285–287 | I. Introduction — Haas's scheme, after Luther and Lakjer, subdividing on the branches of the trigeminal rather than on topography |
| 288–310 | **II. Rhynchocephalia** — introduction, description of the muscles (290–310), discussion |
| 311–419 | III. Lacertilia |
| 420–471 | IV. Ophidia |
| 472–476 | V. Synonymies of Muscles Discussed |
| 477–490 | VI. List of forms studied, acknowledgments, references |

**Page 1 of the local PDF is chapter page 285.** All four descriptive sections are
now mined.

## Why this one

`sphenodon-punctatus` has been in `species.json` since the species layer was
built and carried **one row** — the M. anconaeus quartus, and that only because
Russell & Bauer (2008) mention it while describing *Iguana*. Nothing in the
corpus described a tuatara.

This does, for the head. Haas **dissected two specimens himself**, in Basel and
London, and the description is his own rather than a compilation: where earlier
workers disagree he says which he found and why. 78 *Sphenodon* mentions in the chapter, 43 of them inside the
Rhynchocephalia section itself.

## What it covers

Adductor mandibulae externus in three layers (superficialis, medialis,
profundus), adductor mandibulae internus pars anterior, pterygoideus and
pterygoideus accessorius, entopterygoideus, levator pterygoidei, levator and
retractor anguli oris, depressor mandibulae, constrictor colli and sphincter
colli, platysma myoides, ceratomandibularis, ceratoglossus, levator bulbi,
depressor palpebrae inferioris, retractor vomeris.

That maps onto `adductor-mandibulae` and its four component records,
`depressor-mandibulae`, `intermandibularis`, `interhyoideus`,
`ceratomandibularis`, `extraocular-muscles` and `levator-anguli-oris`.

## The finding worth having before scoring

**It lands on the record this dataset already flags as contested.** The
`levator-anguli-oris` homology note says its identification is the crux of the
lizard–snake problem. Haas reports that Lakjer (1926) overlooked the muscle in
*Sphenodon* altogether; that Luther, editing Lakjer's paper, disagreed and
described both a levator and a retractor anguli oris, blaming the omission on a
poorly preserved specimen; that Poglayen-Neuwall (1953) figured only one; and
that Haas's own two dissections support Luther — two separate muscles, though
the levator differed substantially between his Basel and London animals.

He also gives the comparative point plainly: in *Sphenodon* the insertion is the
same as in lizards but the origin has **not** shifted to the upper temporal arch,
and the tuatara is the only living animal with two temporal arches in which the
lower one gives origin to any part of the adductor mandibulae complex.

## Measured density

43 attachment statements over the 31-page Rhynchocephalia section, 1.4 per page —
lower than a limb monograph because much of the text adjudicates between earlier
authors rather than describing. The description that is there is per-muscle and
states both ends.

## Mined

**Section V, the synonymy tables: 88 names across ten cranial records.** Haas
lists the major synonyms for every muscle in the chapter, each with the authors
who used it, built on Lakjer (1926), Edgeworth (1935), Kochva (1962) and Secoy's
unpublished dissertation. Vernacular names before 1900 and spelling variants are
omitted; French names are given as Latin equivalents. He follows Luther as
adapted by Lakjer, and notes that this is now the terminology used even for
ceratopsian dinosaurs and dicynodonts.

Two entries in it are worth knowing about on their own. **`M.
temporo-massetericus`** is Osawa's (1898) and Byerly's (1925) name for the
adductor mandibulae complex — the two authors who described the tuatara — so a
reader meeting it in either now lands on the right record. And **`M.
ceratomandibularis`** is given as a synonym of the M. geniohyoideus in six
authors including Osawa, which is a different muscle from the urodele
ceratomandibularis this dataset holds under that name; the collision is now
recorded on both records.

**Twenty rows. §VI is the reason there are not more.**

Haas's *List of forms that have been studied* marks his own material `Haas, this
chapter`, and **exactly five animals carry that mark**: *Sphenodon punctatus*,
*Agama stellio*, *Varanus varius*, *Lanthanotus borneensis* and a *Maticora* sp.
from the Field Museum, Chicago. Everything else across 206 pages is compilation,
however detailed. Four of the five were new to `species.json`.

That check also settles what this chapter cannot do. Against **Ctenosaura
pectinata** Haas gives Oelrich (1956) and Avery & Tanner (1971), not himself — so
the four unscored *Ctenosaura* cranial rows are not closed here, and Oelrich
(1956) remains what they need. The base-layer audit already recorded Johnston (2014)
reading the same primary.

Two of the squamate rows justify the whole section. **Lanthanotus** has no
temporal arch and an elongate temporal region, so Haas could follow the adductor
layers in a lizard shaped like a snake; the dorsal fibres Lakjer had called a
distinct *M. adductor mandibulae externus medialis dorsalis* in snakes turn out to
belong there to the profundus, separated from the medialis by the temporal vein,
and Haas concludes Lakjer's muscle is not distinct. That conclusion is recorded on
the row as Haas's, alongside Lakjer's — it is a disagreement about how to divide
one mass, not a correction the data applies. **Maticora** shows the compressor glandulae to be a
single uninterrupted superficialis looping the venom gland, and shows Radovanović
— who missed the sac — to have misidentified the medialis as an abnormal
superficialis.

Ten rows, all of `sphenodon-punctatus`: the adductor mandibulae complex and its
externus, internus and posterior divisions; the levator and retractor anguli
oris; depressor mandibulae; intermandibularis; the sphincter colli group; the
constrictor internus dorsalis group; and the hypobranchial muscles. The tuatara
went from 1 row to 11.

## Still missing for *Sphenodon*

This is the head only. For the **limbs**, Osawa (1898) is now acquired — see
`papers/1898_Osawa_Rhynchocephalia_Extant_Hatteria-punctata-anatomy.pdf`, whose
`Zur Muskellehre` is a systematic numbered myology of the whole tuatara,
in German and unmined. Günther (1867) is acquired too. **Byerly (1925)**, *The
myology of Sphenodon punctatum*, is the one primary still missing and is not on
archive.org.
