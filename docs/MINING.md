# How to mine a paper

Procedure. What is left to mine is in [`WORKLIST.md`](WORKLIST.md); how much is
covered is in [`STATUS.md`](STATUS.md). This file should change rarely.

---

## Extract everything the source states

**The rule this file is built around.** A mining pass reads a paper once. Anything
that pass leaves behind has to be found again by reading the paper again, and the
reading is the expensive part — so the goal is that **no source ever needs a second
intensive pass except to check the first one.**

The thing that used to break this was homology. An occurrence lives inside a muscle
record, so filing an observation meant deciding which homology group it belonged
to. When the source's name could not be matched to a record — an older
nomenclature, a taxon-specific name, a division the record does not make — the
honest options were to guess, or to skip it. Guessing puts an observation on the
wrong record, which is the worst failure this dataset has. Skipping loses the
reading.

So there is a third place to put it. A row in the study's own extraction file,
[`data/observations/`](../data/observations/), with `record: null`. It holds **what a source says about a muscle in an animal, before anyone has decided
which record it belongs to**: the source's own name for the muscle, the species,
the attachments, and a `blockedBy` saying what is missing. Those rows are held to
the same attachment rules as an occurrence — elements must resolve, landmarks must
sit inside their element, the taxon must actually have the bone — because a parked
row with a bad element is not parked, it is wrong.

They carry **no coverage weight**. They are not occurrences, they move no `%att`,
and `STATUS.md` reports them separately as mining already done.

**In practice:**

1. Score what maps onto a record cleanly.
2. Put everything else in the same file with `record: null`, a `blockedBy` and a `blockedNote`
   naming what would settle it — usually a specific paper.
3. When the synonymy is settled, set `muscle` on the row. The validator then warns
   until it is promoted into that record, so a resolved observation cannot sit
   there unnoticed.

**Do not park what you can file**, and do not file what you would be guessing at.
The validator warns if a record already carries an occurrence for the same source,
species and name.

---

## Check the paper before you open it

The single most useful lesson of the mining passes so far. Papers fail to deliver
what their titles promise, and one line predicts it:

```sh
f="papers/SOME_PAPER.pdf"
pdftotext -layout "$f" /tmp/t.txt
echo "$(grep -ciE 'origin|insert|ursprung|ansatz|entspringt|inserirt|naissance|insertion' /tmp/t.txt) \
  mentions / $(pdfinfo "$f" | awk '/Pages/{print $2}') pages"
```

**The language terms are not optional.** This check used to grep `origin|insert`
only, and on a German source that is a test of what language the paper is in.
Osawa (1898) on the tuatara scores **0.06 English mentions per page** across 211
pages — "not a descriptive paper, do not plan rows around it" — while its German
attachment vocabulary appears 314 times. The dataset already holds **63 scored
rows** from it, so the metric was refuted by data already committed. Four of the
ten works in `WORKLIST.md`'s acquisition table are in German.

German is also more compact than English — one *entspringt* does the work of
"takes its origin from" — so read a German figure as worth roughly twice its
number against the thresholds below.

Divide. The number is **origin/insertion mentions per page**:

| per page | What it is | What to do |
|---|---|---|
| **> 4** | A descriptive myology | Mine it. This is where rows come from |
| **2 – 4** | Mixed. Descriptions exist but are thin or buried in tables | Worth opening; expect a slower pass |
| **< 2** | Not a descriptive paper — a model, a morphometric study, an atlas, a review | Do **not** plan rows around it. It may still be valuable for architecture, correlates or nomenclature |

**Run it over the whole backlog at once, not one paper at a time.** Run that way
it also *ranks*, and the ranking has twice put a paper the dataset was already
citing above every unmined paper in `papers/`. A citation is not a mining: a
source can be cited on fifteen rows and have its attachment data untouched.

Four more things to check before scoring:

1. **Ligatures.** Older PDFs use `ﬂ` and `ﬁ`, which break every grep. Replace them
   first or you will conclude a paper has no flexors.
2. **Column order.** Two-column PDFs interleave under `pdftotext`. Use plain
   `pdftotext` if reading order matters, `-layout` if table columns matter. Check
   that a heading actually sits above its own text.
3. **Whether the tables are text.** Grep for a caption, then for a row of it. Four
   rows of output between a caption and the next paragraph means the table is a
   picture and the prose is the route.
4. **The species.** Every row needs one. If the paper dissects an animal the corpus
   does not list, add it to `data/species.json` first.

## Check the methods section, every time

**A citation records where a claim was read, not where it was observed.** Four
sources in a row turned out to be cited here for an animal they never examined,
and it is invisible from the citation count — the row has a species, a source and
a plausible note, and only the paper's own methods section disproves it.

Werneburg (2011) was carrying ten rows on *Trachemys scripta*; his animal is
*Emydura subglobosa* and his appendix is a catalogue across turtles. Johnston
(2014) was carrying four on *Ctenosaura pectinata*; his specimens are ten snakes
and a tuatara, and the *Ctenosaura* figure is Oelrich's. Cieri (2018) was carrying
a row on *Iguana* for a muscle he names as one that *Varanus* has and *Iguana*
lacks.

Two rules fall out of this:

- **A paper that describes N animals should produce N columns.** The loon, the
  second gecko, Johnston's two frogs, Sánchez's three cats and Gambaryan's three
  monotreme genera were each held as one row until someone checked. Where a source
  describes two animals and records no difference between them, that is an
  observation of sameness in two animals rather than a description of one — both
  get rows.
- **A paper that generalises across a clade is not a specimen.** The species
  record gets `generalised: true` and every row on it `speciesBasis:
  "generalised"`. Do not reach for `source`, which means a single-species study,
  and do not invent a plausible exemplar. The validator enforces it both ways.

## A mining pass, end to end

**One file per study per animal.** A paper describing three animals gets three
files; you write one per animal and the accounting closes per file.

1. **Open or create `data/observations/<species>__<source>.json`.** The species is
   half the filename, so nothing has to be inferred. Add the species to
   `data/species.json` first if it is not there — `Genus sp.` if the source names
   no species.
2. **Add a row per muscle the study describes for that animal**:

   ```jsonc
   { "name": "M. extensor metacarpi radialis",   // the SOURCE's name, verbatim
     "region": "forearm",                        // with `name`, the key
     "record": "extensor-antebrachii-carpi-radialis",  // or null, see 3
     "present": "yes",
     "attachments": { "origin": [ … ], "insertion": [ … ] },
     "attachmentNote": "…",
     "after": "Miner 1925" }                     // if the study is reporting
   ```
3. **`record: null` where you cannot assign it**, plus `blockedBy` and a
   `blockedNote` saying what would settle it. That is not failure — it is the row
   being kept instead of dropped, which is the whole point.
4. `attachments` is `{origin: [row], insertion: [row]}`, a row being
   `{element, side?, landmark?}`. Element ids come from `data/skeleton.json`.
5. **Never invent a side.** Absent means unrecorded.
6. Put the reasoning, the caveats and the species-level differences in
   `attachmentNote`. That is where the argument lives.
7. **Close the accounting**: state how many muscles the paper describes and show
   it equals filed plus parked, in the reading note.
8. Set the source's `status` in `data/remine-status.json` — `remined` only once 7
   is true. The file's own `status` must match, and `validate.py` errors if it
   does not.
9. `./scripts/build.sh --write`, which regenerates `muscles-*.json` and validates.

**Never edit `data/muscles-*.json`.** It is generated from the observations by
step 0 of the build, and any edit there is overwritten on the next run.

The validator will reject an attachment to a bone the species lacks. It has been
right every time so far — trust it, and write the disagreement into the note
rather than working around it.

**Edit the JSON. Do not write a script.** Seven single-source seed scripts used to
hold rows as Python literals and were retired for it; see `CLAUDE.md`. The file to
edit is `data/observations/<species>__<source>.json` — `muscles-*.json` is
generated from it and any edit there is overwritten by the next build.

**The extraction file declares the species.** It is half the filename —
`grus-americana__fisher-goodman-1955.json` — so a row cannot land on the wrong
animal by inference, which is what `attribute_species.py` existed to prevent and
occasionally caused. Write the binomial into the prose anyway where the source
names it: it is the evidence that the file is named correctly.

**Where a source names a genus and not a species**, use a `Genus sp.` record —
`lacerta-sp`, `heloderma-sp`. That is a real animal nobody identified further, and
it is not the same as `generalised: true`, which means the source described a clade
and dissected nobody.

## Bridging nomenclature

Most sources use their own names. **Do not map by eye.** Abdala & Diogo (2010)
Tables 1–3 give six taxon columns with explicit *sensu* equivalences and are the
bridge for the forelimb; that is how the crocodylian manus was scored from Meers.
Where no published equivalence exists, say so in the note — as
`extensores-digitorum-breves` does.

Where the source's own term is ambiguous, assert nothing: a femoral "crista
ventralis" is scored as `femur` / ventral rather than as the fourth trochanter,
because the identification is plausible, unestablished, and asserting it would
manufacture an osteological correlate no source claims.

## Writing the reading note

Every mined source gets one, in `papers/`, named after its PDF and linked from
its `sources.json` entry's `notes` field. It carries what the paper says, which
animals it examined, what was scored from it, **and what was deliberately not
scored and why**. A pass that produced a finding about the source belongs here
rather than in a status document — this is the record that survives.

## Regenerating extractions

```sh
for f in papers/*.pdf; do pdftotext -layout "$f" "papers/extracted/$(basename "$f" .pdf).txt"; done
python3 scripts/extract_werneburg_appendix.py
```

Both outputs are git-ignored: they are verbatim source text, and this repository
is public.
