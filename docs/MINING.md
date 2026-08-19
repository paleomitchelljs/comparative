# How to mine a paper

Procedure. What is left to mine is in [`WORKLIST.md`](WORKLIST.md); how much is
covered is in [`STATUS.md`](STATUS.md). This file should change rarely.

---

## Check the paper before you open it

The single most useful lesson of the mining passes so far. Papers fail to deliver
what their titles promise, and one line predicts it:

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

## Scoring a row

1. Find the muscle's record and the occurrence for that species — or add one.
2. `attachments` is `{origin: [row], insertion: [row]}`, a row being
   `{element, side?, landmark?}`. Element ids come from `data/skeleton.json`.
3. **Never invent a side.** Absent means unrecorded.
4. Put the reasoning, the caveats and the species-level differences in
   `attachmentNote`. That is where the argument lives.
5. `./scripts/build.sh --write`, which validates at the end.

The validator will reject an attachment to a bone the species lacks. It has been
right every time so far — trust it, and write the disagreement into the note
rather than working around it.

**Edit the JSON. Do not write a script.** Seven single-source seed scripts used to
hold rows as Python literals and were retired for it; see `CLAUDE.md`.

**The species has to be named in the row's own prose.** `attribute_species.py`
re-derives attribution on every build, and its first rule is the binomial in
`note`, `attachmentNote`, `divisionNote` or `name`. A source keyed to one primary
species will otherwise pull every unnamed row of its clade onto that species. So
write the binomial into the row, and name **other** fossil taxa by genus alone, or
the row migrates to whichever one it mentions first.

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
