# Haas (1973) — Muscles of the jaws and associated structures in the Rhynchocephalia and Squamata

*Biology of the Reptilia* **4** (Morphology D), ch. 5, pp. 285–490. Academic Press.

Source key: `haas-1973`.

## What was acquired

Same mechanism as volume 21: one PDF per page from
[carlgans.org](https://carlgans.org/biology-reptilia-full-content/), **offset +9
for volume 4** (chapter page 1 is `page10`). 31 pages fetched, 31 returned as
PDFs, no Cloudflare interstitials.

| chapter pp. | PDF pages | what |
|---|---|---|
| 285–310 | 294–319 | I. Introduction, and **II. Rhynchocephalia** — A. Introduction, B. Description of the Muscles (290–310), C. Discussion |
| 472–476 | 481–485 | V. Synonymies of Muscles Discussed |

**Not fetched**: III. Lacertilia and IV. Ophidia, chapter pp. 311–471 — roughly
160 pages on squamates and snakes. **Page 1 of the local PDF is chapter page
285.**

## Why this one

`sphenodon-punctatus` has been in `species.json` since the species layer was
built and carried **one row** — the M. anconaeus quartus, and that only because
Russell & Bauer (2008) mention it while describing *Iguana*. Nothing in the
corpus described a tuatara.

This does, for the head. Haas **dissected two specimens himself**, in Basel and
London, and the description is his own rather than a compilation: where earlier
workers disagree he says which he found and why. 43 *Sphenodon* mentions across
28 muscle headings in 31 pages.

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

43 attachment statements over 31 pages, 1.4 per page — lower than a limb
monograph because much of the text adjudicates between earlier authors rather
than describing. The description that is there is per-muscle and states both
ends.

## Still missing for *Sphenodon*

This is the head only. For the **limbs**, the primary descriptions Russell &
Bauer cite are Byerly (1925), *The myology of Sphenodon punctatum* (University of
Iowa Studies in Natural History 11), Miner (1925), Osawa (1898) and Günther
(1867). See `docs/MINING.md` for which of those are reachable.
