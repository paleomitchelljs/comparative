# Didier (1987) — Myology of the ratfish *Hydrolagus colliei*

Honors thesis, Illinois Wesleyan University. Source key: `didier-1987`

An undergraduate thesis: a description to check, not an authority. The extracted
text is OCR and noisy; the muscle entries (origin, insertion, comments) read
cleanly.

## What it is

Three preserved male *Hydrolagus colliei* dissected over a month, plus one female
*Squalus acanthias* for comparison. The jaw, hyoid, trapezius, branchial,
hypobranchial and pectoral muscles are each given an origin, an insertion and a
comment on how earlier authors (Vetter 1878, Luther 1909, Shann 1919, Edgeworth
1935) named them. The thesis argues that the holocephalan jaw adductors lie in
front of the orbit, as in no other living fish, and that the labial cartilages may
be remnants of the palatoquadrate.

## Accounting

The thesis describes 28 muscles of one animal and names two more (the middle and
lower mesio-ventral retractors) in its figures without describing them. All 30 are
rows in `data/observations/hydrolagus-colliei__didier-1987.json`: 12 filed on a
record and 18 parked, the two figure-only ones parked with no attachments because
none are stated.

## Decisions worth keeping

- **The adductor is split three ways and only two are filed.** Didier's pars
  orbitalis and posterior go on `adductor-mandibulae`, as Huber et al. (2011) did
  for this animal. The pars nasalis is parked: Luther calls it the *preorbitalis*,
  the dataset has no record for that muscle, and nothing here equates the
  holocephalan part with the shark one.
- **Interhyoideus and the hyoid constrictors are parked, not filed.** Didier's
  hyoideus inferior has the same attachments as Huber's interhyoideus for this
  animal, while Anderson (2008) finds no interhyoideus. Two sources describe a
  muscle and one denies the homology, so it stays parked.
- **The trapezius pair is filed on `protractor-pectoralis`** on Didier's own
  statement that Edgeworth calls them the cucullaris superficialis and profundus,
  which is also how Huber's cucullaris rows for this animal sit there.
- **The levator anguli oris posterior inserts on the lower-lip skin** in Didier and
  on the superior maxillary cartilage in Huber. Both are kept on the same record.

## Elements added

`prelabial-cartilage` (with a `possibly-corresponds-to` edge to
`premaxillary-cartilage`), `postorbital-ridge` and `postcranial-ridge`
(chondrocranial ridges, not the dermal `postorbital`), `head-clasper-plate`,
`hyoid-rays`, `metapterygium`.

## Not done

- Not checked against the figures.
- The text discusses *Squalus* and the dipnoan *Lepidosiren* (from Bemis & Lauder)
  only for comparison; no rows are taken from them.
