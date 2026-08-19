# What to do next

Curated, and kept short. The measured picture is in [`STATUS.md`](STATUS.md) —
read the generated tables there rather than any figure written into prose here.
How to actually do the work is in [`MINING.md`](MINING.md).

---

## This is an acquisition problem, not a mining problem

The corpus has very nearly exhausted its descriptive sources. Of the rows still
unscored, most cite only sources that structurally cannot yield a species-level
attachment:

| source | why it cannot be scored |
|---|---|
| Abdala & Diogo (2010) | Synonymy. Its specific attachment statements are outnumbered several times over by hedged ones — "usually inserts onto the humerus". Its generalisations belong in `consensus` |
| Diogo & Molnar (2014) | Same shape |
| Diogo et al. (2016) | Homology hypotheses; the attachments are in the supplementary tables, already mined |
| Allen et al. (2021), Hutchinson et al. (2015) | Musculoskeletal models, not descriptions |
| Johnston (2014) | Does not dissect *Ctenosaura* — the figure is after Oelrich (1956) |

What remains in hand is single figures per source. The way forward is to acquire
descriptive myologies, not to re-read what is here.

## Acquisition targets

Ranked by in-text citations across the extracted corpus, weighted by how often the
citation sits near attachment language. `#ours` is how many of our papers cite it.

| #ours | Work | What it would close |
|---:|---|---|
| 18 | **Edgeworth FH (1935). The Cranial Muscles of Vertebrates** | The canonical cranial monograph across all vertebrates, and the spine under most of what the modern papers cite |
| 9 | **Walker WF (1973). The locomotor apparatus of Testudines.** *Biol. Reptilia* 4 | **Acquired.** Turtle limb myology, 100 pp — the Testudines forelimb rows that cite only Abdala & Diogo |
| 6 | **Dunlap DG (1960). The comparative myology of the pelvic appendage in the Salientia** | Anuran pelvis and thigh, the thinnest tetrapod column |
| 6 | Russell AP & Bauer AM (2008). *Biol. Reptilia* 21 | **Acquired.** Lepidosaur limbs, and the tuatara |
| 8 | Francis ETB (1934). The Anatomy of the Salamander | Caudata's classic; what the reference column rests on |
| 7 | Gaupp E (1896). Anatomie des Frosches | The classic anuran reference |
| 4 | Ribbing L (1907, 1938) | Historical backbone for the forearm, the largest region by occurrence count |
| 2 | Ogushi K (1911–13) | Turtle myology in German, and Werneburg's own backbone — would let a real turtle species be scored rather than a catalogue |
| 2 | Hudson GE, Schreiweis DO, Wang SYC (1972) | Avian myology; Aves has the largest single clade gap |
| 2 | Lakjer T (1926) | The sauropsid jaw adductor monograph — three cranial columns at once |

**Most of the top of this list is old, and that is an opportunity.** *Biology of
the Reptilia* is free and complete at
[carlgans.org](https://carlgans.org/biology-reptilia-full-content/) — the viewer
serves one PDF per page at `https://carlgans.org/wp-content/bor/{VV}/BotR{VV}-page{N}.pdf`,
where `N` is the PDF page and the offset differs per volume (in vol. 4 it is +9).
Fetch a range and `pdfunite` it. Edgeworth, Lakjer, Ogushi, Gaupp, Francis and
Ribbing are all old enough to be plausible on the Biodiversity Heritage Library or
archive.org. Four of the ten are in German — a real cost, but Werneburg, Johnston
and Diogo are all reading them, and this dataset is currently reading those
authors' readings of them.

## Two columns are empty for want of a paper

- **A mammalian cranial myology.** Nothing in `papers/` dissects a mammal's head.
  This would restore the masseter/temporalis, digastric, facial-expression and
  middle-ear cases, which are the best arch-identity teaching material available.
- **Crocodylian trunk musculature.** Nothing here covers it. Boumans et al. (2015)
  would restore the avian *neck*, but neither trunk.

## Catalogued and not yet mined

`validate.py`'s `never cited` warnings are the live list — a catalogued source is
a promise, and the warning is what stops the promise being forgotten. The ones
worth reaching for first, by what they would close:

| Source | Would close |
|---|---|
| **Collings & Richards (2019)** | Anuran pelvis and hindlimb in a walking rather than jumping frog |
| **Bauer (1997)** | Urodele jaw openers on CN VII |
| **Cole et al. (2011)** | Developmental origin for the pelvic fin muscles, which the fin records mostly assert topologically |
| **Diogo & Abdala (2007); Diogo (2008)** | The osteichthyan half of the pectoral and cranial homology arguments the tetrapod records rest on |
| **Lowie et al. (2018)** | Lizard forelimb flexors — Lepidosauria's largest remaining region gap |
| **Sánchez et al. (2019)** | Felid forearm and hand. The therian forelimb is scored from a mustelid, and the cat is the animal most labs use |
| **Gyambibi & Lemelin (2013); Lemelin & Diogo (2016)** | Primate forearm and hand |
| **Diogo et al. (2016, marsupials)** | Whether the therian rows are therian or merely eutherian |
| **Mathou et al. (2023)** | Architecture for the axial column, which has none |
| **O'Reilly et al. (2000); Reilly & White (2003)** | Axial function, and the epipubic bone — see the open decision below |
| **Didier (1987); Zhu (2011)** | Holocephalan myology and turtle plastron reduction. Both unpublished theses — check, do not defer to |
| **Schlough; Lőw et al.; OSU Extension; Jacob & Pescatore** | Dissection vocabulary for mustelid, frog, salmonid and chicken, as Campbell (2007) supplied for the rat |

### Sources that are in the corpus and are not row sources

Worth knowing before planning a pass around one:

| Source | Actually for |
|---|---|
| **Ghetie et al. (1976)** | A plate atlas — labelled figures in four languages, no myological prose. Not an attachment source, but the plates *are* legible as images and state species, name, presence, layer and face for four birds. Mostly a **turkey** book: 35 of its 52 captioned myology plates. See its note |
| **Fisher & Goodman (1955)** | The avian column entire, but the scan is uneven and plate-facing pages OCR to noise. **A cleaner scan would unblock Aves more than any other single acquisition** |
| **Blotto et al. (2020)** | Anuran hand and foot, 157 pp with its own revised nomenclature and active disagreements with Abdala & Diogo — needs a dedicated bridging pass |
| Wiseman (2021), Demuth (2022, 2023), Cuff (2022) | Musculoskeletal models — attachments are 3D coordinates |
| Mathou (2023), Gyambibi & Lemelin (2013) | Architecture data |
| Lemelin & Diogo (2016), Richardson (2022), Molnar & Diogo (2021) | Reviews and framing |

## Reading notes

**Every cited source has one.** That was the thinnest layer in the repository and
it is now closed, and `validate.py` keeps it closed: a cited source with no `notes`
pointer warns, and a pointer to a file that does not exist is an error. So this is
a regression check rather than a backlog.

A catalogued but uncited source is exempt — it is a promise, not yet a debt, and
its note gets written when it is mined.

> Where a mining pass produces a finding worth keeping, it belongs in that
> source's reading note. The pass-by-pass narrative that used to live in
> `docs/GAPS.md` §2 is in git history at `85360ce:docs/GAPS.md`; fold each
> paragraph into its source's note when you next touch that source. Those
> paragraphs each name several sources, which is why they were not distributed
> mechanically.

## `papers/toadd/` is empty

Ten PDFs went through it. Six were byte-identical duplicates of tracked sources and
were deleted — including `SCtZ-0341-Hi_res.pdf`, which was not a better Schreiweis
scan but the same file. The other four are in `papers/`, in `sources.json`, and each
has a reading note. What came of them:

**Gambaryan et al. (2002), monotreme hind limb — mined.** Density 8.0, and the
richest source added to this repository in some time: two species dissected and
described separately, the hind limb column for Monotremata where there had been
none, four new skeletal elements and two corrections to existing ones. See the
reading note.

**The other three are not row sources**, and the density check said so before any of
them was opened for scoring — 1.7, 1.1 and 1.9 origin/insertion mentions per page
against the threshold of 4.

- **Regnault & Pierce (2018)** models the echidna shoulder. Its methods section is
  the reason it yields nothing: the specimen was kept intact and **never dissected**,
  and the muscle attachments were read off Gambaryan et al. (2015)'s figures by
  placing markers at the centroid of each shaded area by eye. It is not an
  independent treatment of that shoulder, and this document said it was until the
  methods were read.
- **Diogo et al. (2008)** on the head and neck across sarcopterygians turned out to
  be a row source after all, once its four homology schemes were read as page
  images rather than as text. **Twenty-five rows on eight records** for *Timon
  lepidus*, *Ornithorhynchus anatinus* and *Rattus norvegicus* — presence, division
  and parts, no attachments, because the tables give none. See the reading note.
- **Diogo et al. (2009)** on primate facial muscles is cited on `interhyoideus`. It
  is close to a complete kit for splitting that record into fifteen or twenty, with
  a proposed mammalian nomenclature and 300 synonyms — but see below.

### What the four opened up

- **A facial-muscle expansion is now sourced but still blocked.** Diogo et al. (2009)
  would supply the names, the presence table and the synonymy. It is blocked on the
  same missing paper as before — nothing in `papers/` dissects a mammal's head — and
  on a schema fact worth knowing first: facial muscles mostly end in skin, so the
  muscles most characteristic of the group are the ones an attachment schema can say
  least about.
- **Two cranial records are now one row where their source is fifteen.**
  `interhyoideus` carries the whole mammalian facial musculature in a single
  occurrence per taxon, and `branchial-constrictors` carries the pharyngeal and
  laryngeal muscles the same way. Diogo et al. (2008) Tables 2 and 3 resolve both
  across nine taxa, and Diogo et al. (2009) resolves the facial half muscle by
  muscle through the primates. **Splitting them is the same decision twice**, and
  it is blocked on the same thing: nothing in `papers/` dissects a mammal's head,
  so the new records would carry names and homologies with no attachments beneath
  them. Worth deciding deliberately rather than drifting into.

- **Figures in a PDF are readable; text extraction is not the only route.** The
  Diogo tables were called unreadable in this document for one pass because
  `pdftotext` returns only their footnotes. They read cleanly as page images, with
  dense ones cropped. Anything else in the corpus written off as figure-only —
  **Ghetie et al. (1976), the plate atlas that is the corpus's only chicken
  source** — deserves the same second look before it is called unmineable.
- **Gambaryan et al. (2002) leaves two things unscored.** It describes no obturator
  internus in either animal, so `ischiotrochantericus` is untouched — absence of
  mention is not absence. And its Table 1 gives a "calculated force" in a unit that
  cannot be right (it states 1 dyn = 10⁵ N, a mangled 10⁻⁵, which would put the
  largest muscle in the table under a hundredth of a newton), so no force figure
  from it is entered anywhere. The relative muscle weights in the same table are
  unambiguous and are quoted in the rows.

## Open decisions

These are judgement calls the data is currently carrying, each waiting on a
specific source rather than on effort.

**The tensor tympani is on two records' worth of evidence and one record.** It and
the tensor veli palatini are scored as parts of the human mylohyoid row on
`intermandibularis`, which is where Gest's tables put them. Diogo et al. (2008),
Table 1, derive both from the **adductor mandibulae** instead — from the A2-PVM
bundle they identify in *Latimeria*, *Ambystoma* and *Timon* — and place them on
their adductor row for all five mammals they examined. Nothing about arch identity
turns on it: both fields are mandibular-arch, both take CN V, and the teaching pair
of tensor tympani against stapedius survives either reading. What turns on it is
which record a student finds the muscle under, and this dataset currently answers
that twice. Both records now carry `corresponds-to-part-of` edges naming the other, and both
parts carry `membership: "disputed"` with `claimedBy`, so the dispute is
queryable rather than prose. **What remains is the decision itself**: which record
should hold the muscle, or whether holding it on both is the honest answer.

The date does not settle this one. `intermandibularis`'s computed authority is
Ziermann & Diogo (2019), which is more recent than 2008 but is **a chapter on head
muscle development in fishes** and takes no position on a mammalian muscle. That is
exactly the condition `docs/METHODS.md` describes for opting a record out with
`basis: "curated"`. Deciding it means reading Diogo et al. (2008)'s Table 1 against
whatever the most recent mammalian treatment says, and it is a re-assignment of the
dataset's flagship arch-identity example, so it is left as a decision rather than
made in passing.

**`epipubis` groups two things that may not be one.** It holds the turtle's
cartilaginous epipubic process and the mammalian epipubic bone, on position: both
are the anterior process of the pubis and both take hypaxial and adductor
attachments. That is the usual reading, but neither source cited on the element
demonstrates the homology, and the mammalian element is not uniform even within
Cunningham's three marsupials — a large paired bone in the cuscus, a cartilaginous
nodule in the thylacine. **Reilly & White (2003)** is in `papers/`, unmined, and is
the source that bears on it. Until it is read, splitting the record stays live.

**~~Dick & Clemente (2016) is mapped to an animal it never names.~~ Settled.** Its
six rows are on `varanidae-generalised`, and the source is out of `SOURCE_SPECIES`.
Table 1 carries no per-muscle provenance, so there was no species to recover. See
the reading note.

**Osteological correlates with no muscle on them.** Each is a landmark a
palaeontologist reads first, and the dataset says nothing about what pulls on it.
Two of them are orphans *on purpose* — the supinator crest and the zygomatic arch
each used to carry a muscle through a consensus row no occurrence supported, and
removing those rows was correct. Closing them needs a therian forelimb source and
a mammalian cranial source. The rest are usually not missing observations but
unfinished passes: three closed at once when Hattori & Tsuihiji was finally mined
for rows rather than for its landmark vocabulary. **The fastest way to find the
muscle is normally to reopen the source the correlate came from.**

**Architecture is entered for three species and the schema holds one specimen.**
Zaaf et al. (1999) Tables 4–6 would add the first lepidosaur, but it is two species
× two specimens. A schema decision comes first. Roadmap phase 5.

**Species-level rows the old model could not hold.** Schreiweis (1982) on a penguin
and Martins et al. (2019) on threadsnakes were both once refused as too derived to
represent their clade. Under species scoring that objection is gone — roughly 30
rows.
