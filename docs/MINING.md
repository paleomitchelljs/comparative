# What is left to mine, and how

273 present occurrences still have no attachment rows. This file lists the
sources that could close them, ranked by whether they will actually work.

Regenerate the numbers with `python3 scripts/doc_counts.py --write`. The
density figures below come from the check described in **How** — rerun it on any
new PDF before planning work around it.

---

## How: check the paper before you open it

The single most useful lesson of the last few passes. Four papers in a row failed
to deliver what their titles promised, and one line predicts it:

```sh
f="papers/SOME_PAPER.pdf"
pdftotext -layout "$f" /tmp/t.txt
echo "$(grep -ciE 'origin|insert' /tmp/t.txt) mentions / $(pdfinfo "$f" | awk '/Pages/{print $2}') pages"
```

Divide. The number is **origin/insertion mentions per page**:

| per page | What it is | What to do |
|---|---|---|
| **> 4** | A descriptive myology | Mine it. This is where rows come from |
| **2 – 4** | Mixed. Descriptions exist but are thin or buried in tables | Worth opening; expect a slower pass |
| **< 2** | Not a descriptive paper — a model, a morphometric study, an atlas, a review | Do **not** plan rows around it. It may still be valuable for architecture, correlates or nomenclature |

Four more things to check before scoring:

1. **Ligatures.** Older PDFs use `ﬂ` and `ﬁ`, which break every grep. Replace
   them first or you will conclude a paper has no flexors.
2. **Column order.** Two-column PDFs interleave under `pdftotext`. Use plain
   `pdftotext` (no `-layout`) if reading order matters, `-layout` if table
   columns matter. Check that a heading actually sits above its own text — in
   Widrig et al. the deltoid section is half somebody else's muscle.
3. **Whether the tables are text.** Grep for a caption, then for a row of it.
   Molnar et al.'s Tables 2 and 4–6 — the homology table and the three
   character mappings, the tables this file had named as the only route into
   the fossil column — extract as captions with nothing under them, because
   they are images. Four rows of pdftotext output between a caption and the
   next paragraph means the table is a picture and the prose is the route.
4. **The species.** Every row needs one. If the paper dissects an animal the
   corpus does not list, add it to `data/species.json` first.

**The species has to be named in the row's own prose.**
`attribute_species.py` reattributes every occurrence from scratch on each build,
and its first rule is the binomial in `note`, `attachmentNote`, `divisionNote` or
`name`. A source keyed to one primary species — Molnar et al. to *Eusthenopteron
foordi* — will pull every unnamed row of its clade onto that species and the
validator will then reject the duplicates. So write the binomial into the row,
and name **other** fossil taxa by genus alone, or the row migrates to whichever
one it mentions first.

## How: scoring a row

1. Find the muscle's record and the occurrence for that species — or add one.
2. `attachments` is `{origin: [row], insertion: [row]}`, a row being
   `{element, side?, landmark?}`. Element ids come from `data/skeleton.json`.
3. **Never invent a side.** Absent means unrecorded.
4. Put the reasoning, the caveats and the species-level differences in
   `attachmentNote`. That is where the argument lives.
5. `./scripts/build.sh --write` then `python3 scripts/validate.py`.

The validator will reject an attachment to a bone the species lacks. It has been
right every time so far — trust it and write the disagreement into the note
rather than working around it.

## How: bridging nomenclature

Most sources use their own names. Do not map by eye. **Abdala & Diogo (2010)
Tables 1–3** give six taxon columns with explicit *sensu* equivalences and are
the bridge for the forelimb; that is how the crocodylian manus was scored from
Meers. Where no published equivalence exists, say so in the note — as
`extensores-digitorum-breves` does.

---

## The gap

| Clade | Unscored | Concentrated in |
|---|---:|---|
| Aves | 43 | forearm 10, hand 7, thigh 7 |
| Lepidosauria | 41 | forearm 8, axial 7, cranial 7, pectoral 7 |
| Anura | 40 | forearm 13, pectoral 8, cranial 7 |
| Testudines | 37 | forearm 13, hand 9, pectoral 5 |
| Caudata | 27 | fin 7, cranial 4 |
| Theria | 25 | axial 9, cranial 9 |
| Crocodylia | 18 | axial 6, forearm 5 |
| Chondrichthyes | 12 | fin 5, cranial 4 |
| Tetrapodomorpha (stem) | 9 | pectoral 4, arm 3 |
| everything else | 21 | agnathans, actinopterygians, monotremes |

**Forearm and hand are the largest regions across every tetrapod column**, and
no single source covers them broadly — it goes one animal at a time.

---

## Ready to mine (density > 4)

| Source | per pg | Would close |
|---|---:|---|
| **Jones et al. (2019)** | 6.3 | Aves cranial, contrast CT of a pigeon head |
| **Springer & Johnson (2015)** | 5.9 | Branchial arch muscles in eels — outgroup detail for the constrictor records |
| **Sigurdsen et al. (2012)** | 4.3 | Anura pectoral and forelimb |
| **Ziermann & Diogo (2013)** | 4.2 | Caudata cranial, with development — the axolotl |
| **Pereyra et al. (2019)** | 4.2 | **Correlates, not rows.** See its reading note |
| **Anderson (2008)** | 3.8 | Cranial nomenclature across gnathostomes — a cross-check, not new rows |
| **Bauer (1997)** | 3.6 | Urodele jaw openers on CN VII |
| **Sánchez et al. (2019)** | 3.4 | Theria forearm and hand, in felids. Short but dense |

### Done since this file was written

**McKitrick (1991)** — Aves 30% → 42%, thirteen rows for *Gavia immer* CM 2320 plus
one sourced absence in *Pelecanoides garnoti*, the supinator. Measured at 6.0 per
page rather than the 6.3 recorded here, which is close enough that the check did its
job. Two lessons beyond the rows: her pars metapatagialis inserts into the **humeral
feather tract**, another muscle end no fossil can record; and adding a second avian
species exposed that `seed_occurrence_attachments.py` was keyed on clade and
silently overwrote whichever same-clade row came last. Still in it: *Gavia stellata*,
*Pelecanoides garnoti* in full, and the girdle muscles.
**Molnar et al. (2018)** — Tetrapodomorpha (stem) 0% → 79%, from 7 occurrences to
42 across four species. Not from the supplementary tables this file had named:
they are not in the PDF, and Tables 4–6 are images. The route was **§III**, the
per-taxon review of correlates, read against the confidence gradient in §V and
the conclusions — which is also what forced four of the seven existing rows down
from `inferred` to `uncertain`. Still to take from it: *Pederpes finneyae*,
*Ichthyostega* and *Panderichthys*, all described in the same section.
**Huber et al. (2011)** — Chondrichthyes 5% → 37%, cranial from 10 unscored to 4.
**Schreiweis (1982)** — five *Eudyptes* rows; Aves 13% → 28%.
**Zaaf et al. (1999)**, second gecko — Lepidosauria to 62%, ten of the twenty-one
pairs disagreeing.

## Worth opening (2 – 4)

Diogo et al. (2016, marsupials) · Zhu (2011, turtle plastron, thesis) ·
Dearden et al. (2020, chondrichthyan cranial, preprint) · Didier (1987,
holocephalan, thesis) · Cuff et al. (2022) · Naumann et al. (2017)

## Not row sources (< 2), and what they are for instead

| Source | Actually for |
|---|---|
| **Blotto et al. (2020)** | Anuran hand and foot. 157 pp with its own revised nomenclature and active disagreements with Abdala & Diogo — needs a dedicated bridging pass, not a quick one |
| **Fisher & Goodman (1955)** | The avian column entire — but the scan is uneven: 83 of ~328 headings have a recoverable Origin paragraph and plate-facing pages OCR to noise. **A cleaner scan would unblock Aves more than any other single acquisition** |
| Collings & Richards (2019) | Anuran hindlimb — DICE-CT, data largely in figures |
| Lowie et al. (2018) | Morphometrics. Zero O/I mentions |
| Wiseman (2021), Demuth (2022, 2023), Cuff (2022) | Musculoskeletal models — attachments are 3D coordinates |
| Mathou (2023), Gyambibi & Lemelin (2013) | Architecture data |
| Lemelin & Diogo (2016), Richardson (2022), Molnar & Diogo (2021) | Reviews and framing |
| Schlough, OSU Extension, Jacob & Pescatore, Lőw et al. | Dissection vocabulary — synonyms, as Campbell (2007) supplied for the rat |

---

## Acquisitions the corpus needs

Two columns are empty for want of a paper, not for want of a pass:

- **A mammalian cranial myology.** All ten therian cranial rows were guesses on a
  cheetah and are gone; nothing in `papers/` dissects a mammal's head. This would
  restore the masseter/temporalis, digastric, facial-expression and middle-ear
  cases, which are the best arch-identity teaching material in the dataset.
- **Crocodylian trunk musculature.** The axial crocodylian rows came from
  Schilling's cladogram, not from a crocodile. Boumans et al. (2015) would restore
  the avian *neck*, but nothing here covers either trunk.

## Also outstanding

- **Species-level rows the old model could not hold.** Schreiweis (1982) is a
  penguin and Martins et al. (2019) are threadsnakes; both were previously
  refused for being too derived to represent their clade. Under species scoring
  that objection is gone — roughly 30 rows.
- ~~**54 occurrences attributed `speciesBasis: "default"`.**~~ Cleared: 22
  re-attributed to the animal their source names, 31 lifted out of the base layer
  as review-level clade claims. `GAPS.md` §7 has the accounting. **The `DEFAULT`
  chip should now never appear** — if one does, a new row was added without naming
  its species in prose and without a mapping in `attribute_species.py`.
- **18 flagged correlates with no muscle on them** (`GAPS.md` §3). Pereyra et al.
  (2019) and Hattori & Tsuihiji (2021) are the way in.
- **Architecture is entered for three species.** Zaaf et al. (1999) Tables 4–6
  would add the first lepidosaur, but it is two species × two specimens and the
  `architecture` block holds one — a schema decision first.
