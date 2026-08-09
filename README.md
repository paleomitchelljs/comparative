# Vertebrate muscle homology and topology

An interactive lookup for vertebrate muscles. Type a muscle name — or a synonym
from a hundred-year-old paper, or a bone — and get:

1. **Origin**
2. **Insertion**
3. **Action**
4. **Innervation**
5. **Occurrences** across 16 taxa from hagfish to placentals
6. **Homologies** — what the muscle is called in each group, how well the
   correspondence is supported, and who disagrees

Every claim carries a citation to the primary literature in `papers/`.

## Running it

No build step, no dependencies. It does need a web server, because browsers block
`fetch` on `file://` URLs:

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deployment

Deployed to GitHub Pages by `.github/workflows/pages.yml` on every push to
`main`. **One-time setup:** repository *Settings → Pages → Source →* **GitHub
Actions**.

Actions rather than "deploy from branch" for one reason: it gates the deploy on
`scripts/validate.py`. A broken cross-reference in `data/` produces a page that
loads and then renders wrong, which is worse than a failed build. The workflow
also refuses to publish if the related-muscle graph is asymmetric or if a PDF has
crept into git.

## The problem this solves

The comparative myology literature has no stable nomenclature. Abdala & Diogo
(2010) list the coracobrachialis under six different naming schemes. Their
Tables 1–3 exist precisely to translate between Gaupp, Howell, Walthall &
Ashley-Ross, Meers and Kardong. Going the other way, the same *name* is applied
to non-homologous muscles: Diogo & Molnar (2014) identify twelve human hindlimb
muscle names — "gluteus maximus", "sartorius", "semitendinosus", "adductor
magnus" and others — that anuran authors apply to muscles which are not
homologous to the human ones.

So the search index includes **every synonym and every taxon-specific name**, and
tells you which one matched. Searching `dorsalis scapulae` returns both the
deltoideus scapularis and the latissimus dorsi, because different authors have
used that name for both.

The underlying record is a **homology group**, not a muscle-in-an-animal. Names
are attributes of taxon-specific occurrences. See [`docs/SCHEMA.md`](docs/SCHEMA.md)
for why that matters.

## What's in it

108 muscle records, 202 skeletal elements, 59 sources, 16 operational taxa.

Every PDF in `papers/` is accounted for in `data/sources.json`, including two
declared out of scope. Measured coverage and what is still missing:
[`docs/GAPS.md`](docs/GAPS.md).

| Region | Records | Principal source |
|---|---|---|
| Cranial | 15 | Werneburg 2011; Johnston 2011, 2014; Ziermann & Diogo 2019 |
| Axial | 13 | Schilling 2011; Cieri 2018 |
| Ancestral paired fin | 9 | Diogo et al. 2016; Winterbottom 1973 |
| Pectoral girdle and arm | 21 | Abdala & Diogo 2010; Molnar et al. 2018 |
| Forearm and hand | 27 | Abdala & Diogo 2010; Ercoli et al. 2014 |
| Pelvic girdle and hindlimb | 22 | Diogo & Molnar 2014; Bishop & Pierce 2024 |

Coverage is uneven by design: it follows the papers in `papers/`. The tetrapod
pectoral and forelimb is densest because Abdala & Diogo (2010) tabulate six taxa
against every muscle. Cranial records are organised by pharyngeal arch and are
broader but shallower.

### The fin region is the root, not another region

`data/muscles-fin.json` holds the ancestral paired-fin muscles — five per fin in
the gnathostome LCA, six in the osteichthyan LCA (Diogo et al. 2016) — from
which the entire tetrapod appendicular musculature is derived by subdivision.
Each carries `derivatives`, so a record links forward to the tetrapod muscles it
became, and every tetrapod muscle shows what it came from.

This matters for more than completeness: it is the natural root of the drill-down
hierarchy proposed in [`docs/ROADMAP.md`](docs/ROADMAP.md), and it corrects the
textbook claim that fish fins had only two muscle masses.

## Interface

Methodological notes live in [`docs/METHODS.md`](docs/METHODS.md), not on the
pages — the interface is for muscles. Filters are collapsed by default behind the
**Filters** button; the count on the button shows how many are active.

## Four views

**Muscles** — search and filter by region, taxon, or homology confidence.

**Skeleton** — bone-first, and the pedagogical entry point: drill down through
the skeleton (pectoral girdle → scapula → acromion), see what originates and
inserts at each level, and optionally restrict to one taxon. Elements that taxon
lacks are flagged rather than hidden, so "the coracoid is gone, therefore this
muscle had to move" is visible rather than inferred.

Elements are homology groups: the hyomandibula, columella and stapes are one
record shown under the selected taxon's own name, so the shark's depressor
hyomandibulae and the mammal's stapedius are visibly on the same bone.

**Mass & layer** — the homology spine: developmental origin (dorsal/ventral mass,
or pharyngeal arch) → layer → proximodistal segment. This is the axis that
survives deep transitions, since every tetrapod limb muscle is a subdivision of
an ancestral fin mass.

**Phylogeny** — where muscles were gained and lost along the tree, optimised by
Fitch parsimony rather than read off the tip states. Missing data constrains
nothing; `variable` and `inferred` tips are scored polymorphic; and placements
that depend on the root-state convention are marked equivocal rather than
presented as results. Also plots the published per-appendage muscle counts, where
the striking result is that most of the fin-to-limb change had already happened
*before* the sarcopterygian last common ancestor.

### Attachments carry the structure

An attachment is a row of **bone → side → landmark**, and a muscle touching
several sides or landmarks of one bone gets several rows:

| Taxon | Type | Bone | Side | Landmark |
|---|---|---|---|---|
| Caudata | origin | Coracoid | ventral | — |
| Caudata | origin | Scapula | lateral | — |
| Theria | origin | Scapula | lateral | Supraspinous fossa |
| Theria | origin | Scapula | lateral | Infraspinous fossa |

Because attachments are recorded per taxon, **shifts are computed rather than
asserted** — each taxon is diffed against the earliest one with data on record.
The diff is hierarchy-aware, so `humerus → greater tubercle` reads as a
refinement in resolution, not as a muscle moving.

## How to read the tables

- **`present: no`** means the cited source examined that taxon and did not find
  the muscle. It does not mean the muscle is absent from the whole clade —
  Abdala & Diogo document several muscles present in one lizard and absent in
  another. `variable` marks that case explicitly.
- **`inferred`** marks fossil taxa. These are bracket-and-osteological-correlate
  reconstructions, not observations. Treat them as hypotheses.
- **Confidence labels** reflect the strength of support reported in the sources,
  not certainty. `contested` means named authors actively disagree; the record
  says who.
- **Serial correspondences** between fore- and hindlimb follow Diogo & Molnar
  (2014) and assert *topological* equivalence only. That paper rejects
  forelimb–hindlimb serial homology in the strict ancestral-duplication sense,
  and several correspondences are flagged where the developmental anlagen are
  known to differ.
- **Quoted muscle names** (`'Rhomboideus'`, `'Palmaris longus'`, `'Ambiens'`)
  follow the sources' own convention for marking a name whose homology is not
  established.

## Repository layout

```
index.html              the app
assets/
  app.js                search, list, detail, navigation
  skeleton.js           bone-first browse, hierarchy browse, attachment diffing
  styles.css            vanilla CSS, light/dark
data/
  taxa.json             operational taxa + the topology that orders them
  sources.json          bibliography
  skeleton.json         attachment-site ontology: partOf, presence, correlates,
                        per-taxon names for homologous elements
  muscles-*.json        muscle records, split by region
  raw/                  git-ignored: verbatim extractions, curation aids only
docs/
  SCHEMA.md             data model and how to add records
  ROADMAP.md            path to the visual interface
scripts/
  build.sh              runs the whole data build in dependency order
  validate.py           schema + referential integrity. Exits non-zero on error
  export_matrix.py      long-format CSVs for downstream analysis
  extract_werneburg_appendix.py  parses Werneburg 2011 Appendix 1 into 78 units
  migrate_attachments.py         free strings -> skeleton ids
  migrate_attachment_rows.py     ids -> element/side/landmark rows
  assign_hierarchy.py            segment + layer
  seed_occurrence_attachments.py taxon-specific attachments
  symmetrise_links.py            closes the related-muscle graph
  extract_werneburg_appendix.py  parses Werneburg 2011 Appendix 1 from the PDF
export/                 git-ignored: generated CSVs
papers/                 reading notes (tracked); PDFs (NOT tracked)
```

## PDFs are not in this repository

`.gitignore` excludes `*.pdf` and the `papers/extracted/` and `data/raw/`
directories. The markdown reading notes in `papers/` are tracked; the copyrighted
PDFs they summarise are not, and neither is any verbatim text extracted from
them.

Dataset entries are paraphrased from their sources rather than copied.
Anatomical facts are not copyrightable, but the sources' expression is, and this
repository is public.

## Maintaining it

```sh
./scripts/build.sh --write     # migrations + seeds in order, then validate
python3 scripts/export_matrix.py   # regenerate the analysis CSVs
```

The build scripts are idempotent, so re-running is always safe.

The validator checks that every source key resolves, every taxon reference
resolves, every `related` and `serial.forelimb` link points at a real muscle,
no taxon appears twice in one muscle's occurrences, and every enum value is
legal. It also warns about present-but-uncited rows and never-cited sources.

Adding a muscle means editing one JSON file and reloading the page. See
[`docs/SCHEMA.md`](docs/SCHEMA.md).

## Where this is going

[`docs/ROADMAP.md`](docs/ROADMAP.md) sets out the path to a visual, clickable
interface — drill down from a region into subdivisions, and see how a group
changes along the phylogeny. Short version: the spine should be **developmental
mass and layer**, not attachment points, because attachments are the most labile
attribute a muscle has and the bones themselves come and go along the tree.
Origin/insertion becomes what you *draw*, not what you navigate.

## Known gaps

- **Cranial records are coarse.** The adductor mandibulae is one record covering
  a complex that Werneburg (2011) resolves into a dozen units in turtles alone.
  `scripts/extract_werneburg_appendix.py` produces the structured source data for
  splitting it further.
- **No muscle architecture data.** Mansuit & Herrel (2021) frame this gap and
  name the sources that hold the numbers; several are already in `papers/`
  (Allen et al. 2014; Ercoli et al. 2014; Fahn-Lai et al. 2020). The schema has
  no field for these yet — roadmap phase 5.
See [`docs/GAPS.md`](docs/GAPS.md) for the measured version. In short:
taxon-specific attachments cover 18% of present occurrences — complete for the
lungfish and coelacanth, **zero for the hand, leg and foot**; `side` is on 30% of
rows and `landmark` on 11%; `layer` resolves for 53% of appendicular muscles;
architecture data exists for four muscles (cheetah forelimb) with the pipeline in
place for more; there is still no axial musculature.
- **The stem-tetrapodomorph column is pectoral-only**, limited to what Molnar et
  al. (2018) reconstruct.
- **Monotreme and stem-synapsid rows are sparse** relative to the detail
  available in Gambaryan et al. (2015).
