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

### Never drop an attachment for want of somewhere to put it

**If the source states an attachment, it gets recorded.** Not having a record for
the muscle is what `record: null` is for; not having an *element* for the thing it
attaches to is not a reason to score one end and lose the other. Add the element.

`epipubic-cartilage-anuran` and `dorsal-fascia-anuran` were both added on
2026-08-20 after a pass scored only the iliac end of three *Xenopus* attachments —
a muscle running to the cartilaginous epipubis, and two whose whole origin is on
the dorsal fascia. The reasoning at the time was that using the existing
`epipubic-cartilage` would assert a homology the paper does not make, and it would
have; but the conclusion was wrong. **A new element plus a `possibly-corresponds-to`
edge records the observation and the open question at once**, which is what that
relation exists for, and it is how `epipubic-cartilage` and `epipubic-bone` are
already handled.

The asymmetry is the whole argument. Fixing a homology call later costs an edit.
Recovering a dropped attachment costs reading the paper again — and the paper is
cited from `sources.json`, so anything you *did* record can always be checked, but
only if it is there to check.

There is almost nothing this rule does not reach. Three cases used to be handled
in prose and are now rows — see [`SCHEMA.md`](SCHEMA.md#attachments--element--side--landmark-rows):

- **An attachment onto another muscle** gets `{"muscle": "<record-id>"}` instead of
  an element. Liparini's ambiens pars II ends on the femoro-tibialis; *Xenopus*'s
  latissimus dorsi ends on two thigh muscles; every anuran tensor fasciae latae
  ends on the cruralis. A muscle inserting on another's aponeurosis is the same
  observation as two sharing a tendon.
- **An either/or the source refuses to resolve.** Prefer the least specific element
  that contains both candidates — the two possible PIFI 1 origins are both iliac,
  so the row says `ilium`. Where the candidates sit on different bones, list both
  with `alternative: true`.
- **An attachment located only to a bone.** Score the bone. Springer & Johnson
  could not determine where on the cleithrum *Anguilla*'s PCl arises; the row is
  `{"element": "cleithrum"}`, and the absent `side` and `landmark` already say the
  rest is unrecorded.

What remains genuinely unscorable is only **what the source does not state at
all** — and an empty `attachments` reads as unrecorded, which is true and useful.
Do not confuse it with the case above: "could not determine the site" is a stated
bone, not a missing attachment.

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

### Then divide by the rows the source already carries

Density alone says which papers are worth reading. **Density over rows held says
which have been read badly**, and that is the more useful list while Task 4 is
open. Count filed rows per source out of `data/observations/`, divide the density
by it, and sort:

```sh
python3 - <<'PY'
import os, re, json, collections, subprocess
rs = json.load(open('data/remine-status.json'))['sources']
src = {s['key']: s for s in json.load(open('data/sources.json'))['sources']}
filed = collections.Counter()
for f in os.listdir('data/observations'):
    d = json.load(open('data/observations/' + f))
    filed[d['source']] += sum(1 for r in d['observations'] if r.get('record'))
out = []
for key, ent in rs.items():
    if ent['status'] in ('remined', 'verified', 'blocked-no-source'):
        continue
    pdf = src.get(key, {}).get('pdf')
    txt = pdf and 'papers/extracted/' + pdf[:-4] + '.txt'
    if not txt or not os.path.exists(txt):
        continue
    t = open(txt, errors='ignore').read().replace('ﬂ', 'fl').replace('ﬁ', 'fi')
    n = len(re.findall(r'origin|insert|ursprung|ansatz|entspringt|inserirt|naissance', t, re.I))
    pages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(
        ['pdfinfo', 'papers/' + pdf], capture_output=True, text=True).stdout).group(1))
    # German is about twice as compact; see the table above.
    dens = n / max(pages, 1) * (2 if len(re.findall(r'ursprung|ansatz|entspringt|inserirt', t, re.I)) > 20 else 1)
    out.append((dens / max(filed[key], 1), dens, filed[key], key))
for r in sorted(out, reverse=True)[:15]:
    print(f"{r[0]:7.1f}  density {r[1]:5.1f}  filed {r[2]:4d}   {r[3]}")
PY
```

**A high-density paper holding almost no rows is the signal.** It found both of
the 2026-08-20 re-mines: Freitas et al., 100 attachment statements in 11 pages
against one filed row, and Liparini & Schultz, 300 in 29 against one. In each case
the reading note gave a reason for the small yield, and in each case the reason was
wrong. Read the note, then check it against the paper before believing it — see
`MIGRATION-STATE.md` for what the two excuses were.

This is a query, not a table, deliberately: the answer changes every time a source
is mined, and a copy of it in a document would be stale within a pass.

Four more things to check before scoring:

1. **Ligatures.** Older PDFs use `ﬂ` and `ﬁ`, which break every grep. Replace them
   first or you will conclude a paper has no flexors.
2. **Column order — and the advice that used to be here was wrong.** Two-column
   PDFs interleave under `pdftotext`, and this file used to say "use plain
   `pdftotext` if reading order matters". **That does not work**: on a two-column
   page the plain output alternates between the columns line by line, so a heading
   sits above its neighbour's text either way. Following it cost Widrig et al.
   forty-two of forty-five muscles, on a note that concluded the paper needed
   "the figures, or a column-aware extraction".

   A column-aware extraction is one command. `-layout` already keeps both columns
   side by side on every line, so **slice each page at the column boundary and read
   the left half, then the right**:

   ```sh
   python3 - <<'PY'
   CUT = 73          # find it by eye: where the right column's first character sits
   for page in open(TXT, errors='ignore').read().split('\f'):
       lines = page.split('\n')
       print('\n'.join(l[:CUT].rstrip() for l in lines))
       print('\n'.join(l[CUT:].rstrip() for l in lines))
   PY
   ```

   Find `CUT` from one page, or take the mode of the positions where a run of
   spaces ends. It worked on Widrig (73), Hattori & Tsuihiji (70), Ercoli (72) and
   Jayaram (52) — every two-column paper tried so far. Figure captions stay
   scrambled; the running text comes out clean.

   **A tooling verdict expires.** Three notes in this repo have now claimed a paper
   could not be extracted and been wrong. Retest before planning around one.
3. **Whether the tables are text.** Grep for a caption, then for a row of it. Four
   rows of output between a caption and the next paragraph means the table is a
   picture and the prose is the route.
4. **The species.** Every row needs one. If the paper dissects an animal the corpus
   does not list, add it to `data/species.json` first.
5. **The elements.** Score the attachment the source states, and if the thing it
   attaches to has no element, **add one** — see the recipe below. Never drop an
   end for want of a bone.

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

   **Where the animal already has an occurrence on that record from another
   study, write only what your study says.** The join unions the attachments and
   appends your paragraph after the existing one; it keeps the established `name`
   and records yours in `data/mapping/`. Do not restate the other source's
   reading, and do not edit the other source's file to match yours. If your study
   contradicts it on something structural — how many parts, whether the muscle is
   present — the build stops and names both sources, because that is a decision
   somebody has to take and write down.
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

## Six fields a row can carry that a row could not carry before

All are in [`SCHEMA.md`](SCHEMA.md) in full. They exist because a mining pass kept
having something true to say and nowhere to put it, so **check this list before
demoting anything to prose.**

| Field | Use it when | Do not |
|---|---|---|
| `stage` | The source distinguishes larva from adult. An occurrence is one per (record, species, **stage**), so both get rows | Read absent as "adult". Absent means the source did not distinguish, which is nearly every row |
| `fusedWith` | The source says a muscle is present but **not separable** from a named neighbour | Score it `present: "no"`. A fused muscle is not an absent one, and the build will refuse the contradiction |
| `covers` | The source's name is an umbrella over **several records** — `deltoid`, `digastric`. The row carries no observation, only the name | Give it attachments or a `blockedBy`. It is an index entry and nobody is stuck |
| `division` + `parts` | The source names several muscles inside one record | Hand-write `parts[].attachments`. See below |
| `after` | The source is **reporting someone else's** dissection | Put two workers on one occurrence — it holds one `after` |
| `speciesBasis: "generalised"` | The source describes a clade and dissected nobody | Reach for it because you are unsure which animal. That is `source` or a missing species record |

**Part attachments are derived, and hand-authoring `parts` costs you them.** Write
**one row per muscle the source names**, all pointing at the same `record`, each with
its own attachments; declare `division` on one of them; and the join gives every part
its own origin and insertion. If you also write a `parts` list by hand, the join reads
your named row as the *umbrella* — the `Masseter, temporalis and the pterygoids` case —
and excludes it from the breakdown, so one muscle silently loses its attachments. This
bit twice in one day. Declare `division`, write the rows, leave `parts` alone.

## Adding a skeletal element

The rule is in the section above: never drop an attachment for want of a bone. The
mechanics:

```jsonc
{ "id": "preopercle", "label": "Preopercle", "kind": "bone",
  "region": "cranial", "segment": "cranial", "partOf": "neurocranium",
  "correlate": true,
  "presence": { "default": "no", "present": ["actinopterygii"],
                "sources": ["jayaram-etal-1983"],
                "note": "What it is, and what needed it." } }
```

- `partOf` is containment, and a landmark must sit inside its element — the check is
  on the whole chain, so `{"element": "mandible", "landmark": "coronoid-process-mandible"}`
  works because the process is `partOf` the mandible.
- `presence.default: "no"` plus a `present` list for anything clade-restricted;
  `"yes"` for something general. **Under-claim.** Adding a taxon later is an edit;
  asserting a bone into an animal that lacks it is an error the validator will catch
  only if somebody attaches a muscle to it.
- `kind` from the file's own list — `bone`, `cartilage`, `ligament`, `fascia`,
  `aponeurosis`, `membrane`, `soft`, `group`. Soft-tissue attachment sites are
  legitimate: `linea-alba`, `spermatic-cord`, `plantar-aponeurosis`.
- Keep `elements` sorted by `id`.
- **Check the name is not already taken by something else.** `operculum` in this file
  is the amphibian otic operculum; a fish gill cover is `opercle`. `palatine` is the
  tetrapod dermal bone; the teleost one is `autopalatine`. Two structures sharing a
  word is how a dilator operculi nearly ended up in a salamander's ear.

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

## Mining as a delegated job

A pass splits cleanly into a part that parallelises and a part that does not, and the
split is by file rather than by judgement.

**Private to one source — write these freely:**

- `data/observations/<species>__<source>.json` — one file per animal
- `papers/<source>.md` — the reading note

Two people mining two sources never contend for either.

**Shared — do not write these:**

- Anything generated: `data/muscles-*.json`, `data/mapping/`, `data/aliases.json`,
  `docs/STATUS.md`, `README.md`. `./scripts/build.sh --write` regenerates all of them
  **from the whole dataset**, so two passes running it produce conflicts on files
  nobody edited, and a careless merge yields a `muscles-*.json` matching neither.
- `data/skeleton.json`, `data/species.json`, `data/remine-status.json`,
  `docs/MIGRATION-STATE.md` — shared, and the first is re-sorted whole on every edit.

So a delegated pass **requests** rather than writes: put the elements and species it
needs at the top of its reading note, as a list with the `partOf`, `presence` and
one-line note each would carry, and let whoever integrates apply them and run the
build once. Run `python3 scripts/validate.py` to check your own rows if you like —
it is read-only — but not `build.sh --write`.

### The one rule that matters more than the others

**Never assign a `record` you cannot cite a bridge for.** Quote the sentence — from
the source itself, from a synonymy in the record, or from a `homologyScope` paper —
or write `record: null` with `blockedBy` and say what would settle it.

A parked row costs somebody an edit later. A wrongly filed one puts an observation in
the wrong homology group, which is the worst failure this dataset has and is nearly
invisible once made: the row validates, renders, and reads as evidence. Parking is
cheap and it is not a failure — `record: null` exists precisely so that a pass can be
exhaustive without guessing.

Three signs you are guessing rather than bridging: the names simply look alike; you
have joined two synonymies to reach a third; or the only argument is that the muscle
is nearby. All three have produced errors in this repo.

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
