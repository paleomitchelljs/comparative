# What is left to mine, and how

239 present occurrences still have no attachment rows. This file lists the
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
| Aves | 40 | forearm 10, hand 7, thigh 7 |
| Anura | 40 | forearm 13, pectoral 8, cranial 7 |
| Lepidosauria | 38 | forearm 8, axial 7, pectoral 7 |
| Testudines | 37 | forearm 13, hand 9, pectoral 5 |
| Caudata | 22 | fin 7, hand 3, pectoral 3 |
| Chondrichthyes | 12 | fin 5, cranial 4, axial 2 |
| Crocodylia | 12 | forearm 5, pelvic 2, thigh 2 |
| Theria | 9 | hand 3, axial 2, foot 2 |
| Tetrapodomorpha (stem) | 9 | pectoral 4, arm 3, forearm 1 |
| everything else | 20 | agnathans, monotremes, stem synapsids, the coelacanth |

**Forearm and hand are the largest regions across every tetrapod column**, and
no single source covers them broadly — it goes one animal at a time.

**This table counts unscored rows, so a new species does not move it.** Anura still
reads 40 after the Sigurdsen pass, because those nine rows were *added* — a second and
third frog, both fully scored — while the eight unscored *Rhinella* rows are still
there. The percentage in `GAPS.md` went 35% to 43%; the gap did not close. Read the two
numbers together: this table is what is left to score in animals already present, and
the percentage is how much of what is present is scored.

Two of these numbers fell without a paper being read. Theria dropped from 25 to 9
and Crocodylia from 18 to 12 because the base-layer pass removed rows attributed to
animals their sources never examined, and Lepidosauria and Caudata lost one or two
the same way. A shrinking gap is not always progress — check whether rows were
scored or deleted.

---

## Ready to mine (density > 4)

| Source | per pg | Would close |
|---|---:|---|
| **Pereyra et al. (2019)** | 4.2 | **Correlates, not rows.** See its reading note |
| **Anderson (2008)** | 3.8 | Cranial nomenclature across gnathostomes — a cross-check, not new rows |

### Run the density check over the whole backlog, not one paper at a time

The check in **How** was written to be run on a paper you are about to open. Run
over all 31 unmined and under-mined sources at once it also *ranks* them, and the
ranking was not what the worklist assumed: **the top two targets were both papers
already in the dataset**, cited for years and never mined out.

| | per pg | state |
|---|---:|---|
| Ziermann et al. (2014) | **4.7** | cited by 15 occurrences, 7 scored — **mined, below** |
| Johnston (2011) | **4.4** | cited by 9 occurrences, **1** scored — **mined, below** |
| Pereyra et al. (2019) | 4.2 | correlates, as recorded |
| Anderson (2008) | 3.8 | cross-check |
| Diogo et al. (2016, marsupials) | 2.7 | worth opening |
| Zhu (2011) · Cuff (2022) · Dearden (2020) · Didier (1987) | 2.0–2.2 | worth opening |

Everything below 2.0 is 20 sources and confirms what this file already says about
them: models, morphometrics, atlases and reviews. **The backlog is smaller than
the source count suggests** — of 32 in-scope uncited sources, four are above the
mixed band, and two of the best targets in the corpus were not in the backlog at
all. Check the papers you have already used before acquiring more.

### Done since this file was written

**Anderson (2008)** — **opens the holocephalan column**, which is more than the
"cross-check, not new rows" this file predicted. *Hydrolagus colliei* was in
`species.json` with zero occurrences; Anderson's Table 2 is a 13-group × 5-taxon
homology matrix (*Amia*, *Latimeria*, *Squalus*, *Chlamydoselachus*, *Hydrolagus*)
and five rows came straight off it. **The two best are absences with a mechanism.**
The levator arcus palatini is gone because the holocephalan palatoquadrate is fused
to the cranium — autostyly leaves nothing to levate, and Anderson reads it as
secondary loss of a basal gnathostome muscle. The interhyoideus is absent against
its presence in the other four. A muscle lost because its joint was lost is the
cranial counterpart of the therian supracoracoideus moving when the coracoid went.
Also from it: a coracomandibularis in **all five** taxa, which is Anderson's
argument that basal gnathostome jaw depression ran through that muscle directly and
was **not** coupled to the hyoid — the osteichthyan coracohyoideus-through-ligament
system being derived — and a *Hydrolagus* muscle called geniohyoideus by some and
interhyoideus by others, renamed `mandibulohyoideus` because it matches neither.
It gives the chimaera two independent ways to open its jaw.
Adding the second chondrichthyan row **tripped the clade-keyed seed guard**, which
reported `hypobranchial-muscles/chondrichthyes: 2 rows in that clade` and stopped the
build instead of overwriting one. That guard was added after the loon; this is the
first time it has caught something since, and it worked.
Cranial 66% → 63% and Chondrichthyes 47% → 41%, because three of the five rows have
no attachments — Anderson maps names, not sites. Still in it: *Amia calva* and
*Chlamydoselachus anguineus*, neither yet in `species.json`, and the placoderm
reconstruction section.

**Pereyra et al. (2019)** — no rows, as its reading note already said, but it was
**uncited in `data/` until now** and its actual contribution had never been captured.
Their Table 2 classifies Sharpey's fibres at every pectoral and humeral attachment
in three turtles, and the finding is the blanks in it: **nine attachments leave
fibres in one or two of the three species and none at all in the others**, in both
directions. The triceps origin marks the humeral diaphysis in two species and not
the third — same muscle, same bone. So a missing correlate is not a missing muscle,
and that is now measured instead of assumed. Written into
`METHODS.md` and `GAPS.md` §3; `humerus` is flagged `correlate` on this evidence.
It is the strongest argument available for keeping Molnar et al.'s six
stem-tetrapodomorph rows at `uncertain`.

**Johnston (2011)** — Anura 45% → 50%, cranial 63% → 66%. Measured **4.4** per
page. Eight of its nine occurrences were unscored, and the reason was the same one
Zaaf's geckos exposed: **the paper describes two frogs and the dataset held one.**
`attribute_species.py` maps this source to *Ascaphus truei*, so every row landed
there, and *Leiopelma hochstetteri* — four specimens against two, and the fuller
of the two descriptions — had no rows at all. Seven added, six of them scored.
The proof that this was losing data is in the old *Ascaphus* internus row, whose
`origin` prose read "in Leiopelma the origin extends further rostrally than in
Ascaphus": a species difference demoted to a sentence because there was nowhere
to put it. It is now two rows.
**`levator-anguli-oris` is the clean demonstration of the rollup.** Johnston
identifies it in *Ascaphus* — the first record of the muscle in any frog — and does
not find it in *Leiopelma*. The Ascaphus row had been carrying `present: "variable"`,
which is the clade's answer written onto one animal. It is now `yes` against a
sourced `no`, and Anura computes `variable` from the disagreement, which is what
that value is supposed to mean.
Two elements added: `crista-parotica`, the caudal limit of the adductor origin, and
nothing else — the anuran skull was already well enough resolved, which is exactly
the contrast with the agnathan pass below. `palatoquadrate-quadrate` took all four
quadrate attachments without a new element, which is the one-group rule working.
Still in it: the depressor mandibulae and its medial bundle in the cranio-quadrate
passage, the levator bulbi and depressor membranae nictitantis, the petrohyoidei,
and the *Callorhinchus* comparative material beyond the two rows it already carries.

**Ziermann et al. (2014)** — Myxini 0% → 33%, Petromyzontida 0% → 33%,
Chondrichthyes 37% → 47%, cranial 58% → 63%. Measured **4.7** per page. Reached
because it topped the re-ranked backlog while sitting inside the dataset already:
eight of its fifteen occurrences had no attachments, and the two taxa it alone can
serve were the only zeroes left in `GAPS.md` §2. **Four elements added** —
`extrabranchial-cartilages`, `taenia-longitudinalis`, `lingual-cartilage` and the
`scapular-process` landmark — because the agnathan head is almost absent from
`skeleton.json` and that, not effort, is what had blocked the column.
Two mis-citations found on the way in, both of the kind §7 of `GAPS.md` is about:
the **depressor hyomandibulae was on the wrong shark**, described by Ziermann et al.
only in *Leucoraja erinacea* and in a discussion explicitly about batoids, while
their *Squalus* hyoid section lists no depressor at all; and **both extraocular rows
cited this paper, which contains no extraocular content whatever** — zero hits for
*extraocular*, *eye muscle* or *oculomotor* in 32 pages. Those moved to Fritzsch
(2023), which is what they were describing, and which supplies a new sourced
absence: *Myxine* has **no extraocular muscles and no ocular motor neurons**, the
only vertebrate group of which that is true.
**What the pass is really a record of is muscle that does not reach bone.** The
hagfish constrictor branchiarum ends on the mesentery, the surface of the heart and
the fascia of the branchial pouches, and only its anterior fibres reach cartilage.
The lamprey hypobranchial series ends on a median raphe and on other muscles, and
is left unscored **with the reason written into the note** rather than filled from
the shark's rows. The shark cucullaris has no origin row — fascia at the front,
girdle at the back. Half the work here was deciding what not to score.
Still in it: *Hydrolagus colliei* and *Mustelus laevis* in full, the mandibular and
hyoid series for both cyclostomes, and the branchial basket of *Leucoraja*.

**Sánchez et al. (2019)** — forearm 55% → 58%, Theria 86% → 88%. Nine rows and three
species: *Panthera onca*, *Leopardus pardalis*, *Leopardus geoffroyi*. Measured 3.3 per
page; "short but dense" was right, because almost every statement is a comparison
between the three. Three rows exist purely to hold a disagreement — five palmaris longus
tendons in the jaguar and ocelot against four in Geoffroy's cat, one lateral digital
extensor belly against two, a more proximal abductor digiti I longus origin against a
less proximal one. **The third mis-mapped species this session**: it was pinned to *Felis
catus*, which appears in it twice as a comparison. And a caution worth keeping: THE HAND
REGION DID NOT MOVE, because the paper's hand content sits on forearm-region records. A
forelimb paper is not automatically a hand paper.
**Bauer (1997)** — cranial 57% → 58%, and the dataset's 127th muscle record. Reached
because Ziermann & Diogo flagged the **ceratomandibularis** as variable across urodeles
and there was nowhere to put it. Measured 3.5 per page against 3.6, the closest the
figure has come. Two rows for *Necturus maculosus*: the ceratomandibularis, which opens
the jaw by pulling against the hyobranchial apparatus rather than the skull and reaches
the gonial only THROUGH A LIGAMENT, and a `divided` depressor mandibulae against the
axolotl's `single` on the same record. Two elements added — `gonial` and
`hyomandibular-ligament` — and three earlier descriptions corrected in the note rather
than scored. Still in it: the larval condition, *Proteus*, and five more salamanders
that would turn the ceratomandibularis' variability into scored disagreement.
**Springer & Johnson (2015)** — Actinopterygii 46% → 50%. One row, for *Protanguilla
palau*, and it is the largest single occurrence in `branchial-constrictors`: fifteen
units against ten in the axolotl and two in the shark. Measured 5.3 per page, close to
the 5.9 recorded. The absences are characters here too — obliquus dorsalis 3, adductores
1-3, recti 1 and 2 and R4Cm are all recorded absent, and the paper's nine anguilliform
synapomorphies are what the attachments were gathered for. **It forced the branchial
basket into the skeleton**: `epibranchials`, `pharyngobranchials` and `hypobranchials`
are now elements, because a rectus dorsalis running from one epibranchial onto the
PRECEDING one cannot be expressed against a single `branchial-arches` group. The
ceratobranchial did not get a new element — the ray-finned fishes joined
`cornu-branchiale`, which already held it for turtles and salamanders, with a
`taxonNames` entry. Five more eel species are described in full and still unmined.
**Sigurdsen et al. (2012)** — Anura 35% → 43%. Seven rows for *Leiopelma
hochstetteri* and two for *Xenopus laevis*, and one correction: **the paper examines no
*Rhinella*,** yet both rows citing it sat on *Rhinella arenarum* because
`attribute_species.py` had borrowed Abdala & Diogo's anuran exemplar for it. Its
figured frogs are *Leiopelma* and *Ascaphus*. Measured 3.8 per page, not 4.3. It also
fixes the nomenclature three records depend on — anuran "deltoid" = caudate
procoracohumeralis = amniote deltoideus clavicularis; anuran "dorsalis scapulae" =
amniote deltoideus scapularis — and it puts a real disagreement on the board:
`subcoracoscapularis` is `no` in *Leiopelma* against `yes` in *Rhinella*, so Anura now
computes as `variable`. **What is left in it is *Triadobatrachus*, and it is blocked on
structure rather than effort: there is no stem-salientian operational taxon.** Adding
one — with *Prosalirus*, *Czatkobatrachus*, *Amphibamus* and *Doleserpeton* — is the
`taxa.json` topology change that pass would need.
**Ziermann & Diogo (2013)** — cranial 46% → 56%, Caudata 70% → 76%. Seven rows for
*Ambystoma mexicanum*, reached because an audit found it cited for five rows with none
of them scored. Measured **3.3** per page, not the 4.2 recorded here, which put it in
the mixed band — and the band's description held: the attachments are there but buried
in a developmental narrative. It is the only source in the corpus giving LARVAL AND
ADULT attachments for one animal, and four muscles move between them (Meckel's
cartilage to the dentary, and the pseudotemporalis origin dorsally off the
palatoquadrate onto the parietal and the first vertebrae). Two differentiation events
run backwards here — the pseudotemporalis profundus and the levator hyoideus both
become integrated into another muscle by adulthood. Next for this column: **Bauer
(1997)** on the ceratomandibularis, which this paper reports as variable across
urodeles.
**Jones et al. (2019)** — cranial 35% → 46%, Aves 42% → 49%. Ten rows and 33 named
parts for one *Columba livia*, which gave the avian cranial column its first
attachment data of any kind. Measured 5.0 per page against the 6.3 recorded here, and
still easily worth it: the structure matters more than the density, because every
muscle carries an explicit Origin / Path / Insertion / Function. Two rules got their
first real workout — the postorbital process scored on the squamosal because birds
have no postorbital bone and the validator would rightly have refused it, and the
protractor pterygoidei et quadrati placed on `levator-arcus-palatini` with the note
saying the homology rests on position and CN V rather than on any source here. Still
in it: the neck muscles, and the ligaments that carry part of the depressor mandibulae
origin.
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
- **Dick & Clemente (2016) is mapped to an animal it never names.** Six hindlimb
  rows carry its Table 1, which is a compilation "of the varanid hindlimb" from
  four earlier papers, two of them on non-varanids. The mapping is flagged in
  `attribute_species.py` and argued in `GAPS.md` §7; the disposition is a
  decision, not a lookup fix.
- **18 flagged correlates with no muscle on them** (`GAPS.md` §3). Pereyra et al.
  (2019) and Hattori & Tsuihiji (2021) are the way in.
- **Architecture is entered for three species.** Zaaf et al. (1999) Tables 4–6
  would add the first lepidosaur, but it is two species × two specimens and the
  `architecture` block holds one — a schema decision first.
