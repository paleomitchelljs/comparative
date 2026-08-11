# What is left to mine, and how

277 present occurrences still have no attachment rows. This file lists the
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

Three more things to check before scoring:

1. **Ligatures.** Older PDFs use `ﬂ` and `ﬁ`, which break every grep. Replace
   them first or you will conclude a paper has no flexors.
2. **Column order.** Two-column PDFs interleave under `pdftotext`. Use plain
   `pdftotext` (no `-layout`) if reading order matters, `-layout` if table
   columns matter. Check that a heading actually sits above its own text — in
   Widrig et al. the deltoid section is half somebody else's muscle.
3. **The species.** Every row needs one. If the paper dissects an animal the
   corpus does not list, add it to `data/species.json` first.

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
| Chondrichthyes | 18 | cranial 10, fin 5 |
| Crocodylia | 18 | axial 6, forearm 5 |
| everything else | 28 | mostly fossil and agnathan columns |

**Forearm and hand are the largest regions across every tetrapod column**, and
no single source covers them broadly — it goes one animal at a time.

---

## Ready to mine (density > 4)

| Source | per pg | Would close |
|---|---:|---|
| **Molnar et al. (2018)** | 7.1 | The stem-tetrapodomorph column, currently 0% — its Tables S1–S6 are the only route |
| **McKitrick (1991)** | 6.3 | Aves forelimb, from a loon. A third neognath |
| **Jones et al. (2019)** | 6.3 | Aves cranial, contrast CT of a pigeon head |
| **Springer & Johnson (2015)** | 5.9 | Branchial arch muscles in eels — outgroup detail for the constrictor records |
| **Sigurdsen et al. (2012)** | 4.3 | Anura pectoral and forelimb |
| **Ziermann & Diogo (2013)** | 4.2 | Caudata cranial, with development — the axolotl |
| **Pereyra et al. (2019)** | 4.2 | **Correlates, not rows.** See its reading note |
| **Anderson (2008)** | 3.8 | Cranial nomenclature across gnathostomes — a cross-check, not new rows |
| **Bauer (1997)** | 3.6 | Urodele jaw openers on CN VII |
| **Sánchez et al. (2019)** | 3.4 | Theria forearm and hand, in felids. Short but dense |

### Done since this file was written

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

## Also outstanding

- **Species-level rows the old model could not hold.** Schreiweis (1982) is a
  penguin and Martins et al. (2019) are threadsnakes; both were previously
  refused for being too derived to represent their clade. Under species scoring
  that objection is gone — roughly 30 rows.
- **54 occurrences attributed `speciesBasis: "default"`.** Guesses. Find them in
  the JSON or by the `DEFAULT` chip in the occurrence table.
- **18 flagged correlates with no muscle on them** (`GAPS.md` §3). Pereyra et al.
  (2019) and Hattori & Tsuihiji (2021) are the way in.
- **Architecture is entered for three species.** Zaaf et al. (1999) Tables 4–6
  would add the first lepidosaur, but it is two species × two specimens and the
  `architecture` block holds one — a schema decision first.
