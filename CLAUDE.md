# Project notes

Interactive lookup for vertebrate muscle homology and topology. Static site,
no build step, no dependencies. Data in `data/*.json`, app in `assets/`.

## Before committing

```sh
./scripts/build.sh --write               # normalises, derives, validates
for t in tests/*.test.js; do node "$t"; done
```

That is the whole list — the build runs `symmetrise_links`, `doc_counts` and
`validate` in order and exits non-zero on any of them. CI runs it too and fails if
the committed data moves.

**Never type a measured figure into `docs/`.** `doc_counts.py` generates them into
`<!-- counts:… -->` blocks in `README.md` and `docs/STATUS.md`, and it now
*rejects* a percentage written anywhere else under `docs/`. That check exists
because generating the blocks was not enough on its own: an audit found 77
hand-written percentages contradicting a generated table in the same file, one of
them a sentence calling cranial the region to worry about sixty lines under a
table showing it mid-pack. If a figure belongs to a source rather than to this
dataset, mark the paragraph `<!-- pct-ok -->`. `papers/` is exempt: a reading note
records what one pass moved, and history does not go stale.

## Which document does what

Nothing carries two of these jobs.

| File | Job |
|---|---|
| `docs/SCHEMA.md` | The data model. The only definition of any field |
| `docs/METHODS.md` | How to read the data. The only statement of any interpretive rule. **No numbers** |
| `docs/STATUS.md` | Where coverage stands. **Entirely generated** |
| `docs/WORKLIST.md` | What to do next, and the open decisions |
| `docs/MINING.md` | How to mine a paper. Procedure, changes rarely |
| `docs/ROADMAP.md` | Where the interface is going, and why the spine is mass-and-layer |
| `papers/*.md` | What one source says, and what one pass found. Where history lives |

If a rule is stated in two of them, one is wrong and you cannot tell which — so
state it once and link.

## Non-obvious constraints

**A muscle record is a homology group, not a muscle in one animal.** Names belong
to taxon-specific `occurrences`; the record's `name` is just the preferred label.
This is load-bearing — the literature applies one name to non-homologous muscles
and six names to one muscle. See `docs/SCHEMA.md`.

**Never paste source text into `data/`.** Paraphrase and cite. The repo is
public; anatomical facts are free, the sources' expression is not.
`data/raw/` and `papers/extracted/` hold verbatim extractions and are git-ignored
for this reason. Do not commit them or quote from them into the dataset.

**Never commit PDFs.** `.gitignore` excludes `*.pdf` globally. The markdown
reading notes in `papers/` are tracked and are the citable in-repo record.

**`present: "no"` is a claim about an exemplar species, not a clade.** Use
`variable` when a source reports presence in some species of a clade and absence
in others, and say which in `note`. Getting this wrong turns a sampling artefact
into a false evolutionary loss.

**`serial` correspondences are topological unless proven otherwise.** Diogo &
Molnar (2014) reject strict forelimb–hindlimb serial homology. Default
`basis: "topological"`; use `"developmental"` only where the source establishes
shared anlagen; put known anlage mismatches in `caution`.

**Quote disputed muscle names in `name`** — `"'Rhomboideus'"`, `"'Ambiens'"`.
This follows the sources' own convention and the UI renders it verbatim.

**Recency governs homology and does not govern attachment.** An attachment is an
observation and does not age — Cunningham's 1882 thylacine origin and Osawa's
1898 tuatara insertion are worth exactly what a modern one is, and two workers
who each dissected an animal cannot conflict, because they are different rows.
A homology is an interpretation and does age: **where two sources homologise or
synonymise differently, the more recent comparative treatment wins**, and the
older reading goes in the note under its author's name rather than being
deleted. Never let an old descriptive source set which record a muscle lands on
when a newer comparative one covers it.

Enforced, not just stated. `sources.json` carries `homologyScope: true` on
sources whose stated purpose includes homology, synonymy or nomenclature across
**more than one taxon** — Diogo *et al.* throughout, Winterbottom, Hattori &
Tsuihiji, Blotto, Johnston, and the *Biology of the Reptilia* synonymies.
Describing one animal superbly does not qualify. `seed_homology_authority.py`
writes `homology.authority` as the most recent such source cited on the record,
and `validate.py` **errors** if it drifts. So after adding a comparative source
to any record, re-run:

```sh
python3 scripts/seed_homology_authority.py --write
```

Opt a record out with `basis: "curated"` plus a `note` giving the reason — the
only good one being that the newer source does not examine the taxa the record
turns on. See `docs/METHODS.md`.

**Skeletal elements are homology groups, like muscles.** One element, per-taxon
names in `taxonNames`. Never create a second element because a taxon calls it
something else — that is how hyomandibula and stapes ended up as separate rows,
making the shark's depressor hyomandibulae and the mammal's stapedius look like
they attached to different bones. `derivedFrom` is for genuine fission
(scapulocoracoid -> scapula + coracoid), not for renaming.

**Attachments are element/side/landmark rows, not strings.** `element` is
always the bone; subsites go in `landmark` and must be `partOf` that bone. Every
id resolves to `data/skeleton.json`. A muscle on several sides or landmarks of
one bone gets several rows.

**Never invent a `side`.** Absent means unrecorded. The same goes for a taxon's
attachments: leaving an occurrence without `attachments` correctly reads as "not
recorded", whereas copying the consensus asserts an observation nobody made.

**A source that describes a clade is not a specimen.** Where a paper generalises
rather than dissecting — Winterbottom's teleost synonymy — the species record gets
`generalised: true` and every row on it `speciesBasis: "generalised"`. Do not reach
for `source`, which means a single-species study, or invent a plausible exemplar.
The validator enforces it both ways.

**Rebuild with `./scripts/build.sh --write`,** which normalises, derives and then
validates. It is a fixed point — CI runs it and fails if the committed data
changes.

**Mining a paper means editing `data/*.json`. Do not write a script to do it.**
Seven single-source seed scripts used to run inside the build, each holding a
paper's rows as a Python literal. Once the rows were committed the literal was a
stale second copy, and because each assigned its fields unconditionally, every
build replayed it over later curation — `linea-alba` over a corrected
`body-wall`, `median` over a curated `median-anterior-interosseous`, citations
dropped off rows since scored against a second source. They are retired. What
each one argued now lives in the reading note for its source.

The steps that remain either normalise a field into its structured form or derive
one that is computable, and they **fill rather than sync**: a field is written
only where the row has none, and `sources` is a union. `docs/SCHEMA.md` is the
guide to adding rows by hand.

**Regenerate analysis exports with `scripts/export_matrix.py`.** `export/` is
git-ignored — it is derived, never a source of truth.

**`related` is an undirected graph.** Record a link once, then run
`symmetrise_links.py --write`. Do not hand-curate both directions.

**`derivatives` is a DIRECTED graph and must not be symmetrised.** It runs from
an ancestral fin muscle to its tetrapod descendants. The app computes the reverse
edge by scanning, so tetrapod records carry no ancestry field. Keep it curated in
`data/muscles-fin.json` only.

**Three link types, three meanings — don't conflate them.**
`related` = topologically or developmentally adjacent, undirected.
`derivatives` = ancestor → descendant through evolutionary time, directed.
`homology.serial` = forelimb ↔ hindlimb within one animal, topological not
genealogical, and rejected as strict serial homology by Diogo & Molnar (2014).

**`muscleCount` in `taxa.json` is the source's published count for its exemplar
species**, not a count of records in this dataset. The two differ. Do not
"fix" the discrepancy.

## Regenerating source extractions

```sh
# all PDFs -> papers/extracted/*.txt  (git-ignored)
for f in papers/*.pdf; do pdftotext -layout "$f" "papers/extracted/$(basename "$f" .pdf).txt"; done

# Werneburg 2011 Appendix 1 -> structured JSON (git-ignored)
python3 scripts/extract_werneburg_appendix.py
```

Requires `pdftotext` (poppler) and the PDFs present locally.
