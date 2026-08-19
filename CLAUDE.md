# Project notes

Interactive lookup for vertebrate muscle homology and topology. Static site,
no build step, no dependencies. Data in `data/*.json`, app in `assets/`.

## Before committing

```sh
python3 scripts/validate.py              # must exit 0
python3 scripts/symmetrise_links.py --write
python3 scripts/doc_counts.py --write    # after ANY change under data/
for t in tests/*.test.js; do node "$t"; done
```

`doc_counts.py` rewrites only the `<!-- counts:… -->` blocks in `README.md` and
`docs/GAPS.md`. **The prose around them is hand-written and it drifts** — an audit
found the claim "inheriting is the majority case, 69 of Theria's 81 muscles"
repeated across `METHODS.md`, `README.md` and two source comments long after it
had inverted to 185 of 593 cells. If you change the shape of the data, grep the
docs for the figure you just moved; the generated blocks will not catch it.

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

**Rebuild with `./scripts/build.sh --write`,** which runs the migrations and
seeds in dependency order and then validates. It is a fixed point — CI runs it
and fails if the committed data changes.

**The seeds fill, they do not sync.** A seed writes a field only where the
occurrence has none, and `sources` is a union. They used to assign
unconditionally, so every build replayed each script's embedded copy over later
curation: `linea-alba` over a corrected `body-wall`, `median` over a curated
`median-anterior-interosseous`, and citations dropped off rows that had since
been scored against a second source. **So editing a seed script no longer
changes data that already exists.** To revise a seeded row, edit the JSON — that
is the copy under curation and the one the build now preserves.

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
