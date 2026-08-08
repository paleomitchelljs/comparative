# Vertebrate muscle homology and topology

An interactive lookup for vertebrate muscles. Type a muscle name — or a synonym
from a hundred-year-old paper, or a bone — and get:

1. **Origin**
2. **Insertion**
3. **Action**
4. **Innervation**
5. **Occurrences** across 15 taxa from hagfish to placentals
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

To publish: enable GitHub Pages on the `main` branch, root directory. The site is
static and works as-is.

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

79 muscle records, 486 taxon occurrences, 21 sources, 15 operational taxa.

| Region | Records | Principal source |
|---|---|---|
| Cranial | 9 | Werneburg 2011; Ziermann & Diogo 2019; Ziermann et al. 2014 |
| Pectoral girdle and arm | 21 | Abdala & Diogo 2010; Molnar et al. 2018 |
| Forearm and hand | 27 | Abdala & Diogo 2010; Ercoli et al. 2014 |
| Pelvic girdle and hindlimb | 22 | Diogo & Molnar 2014; Bishop & Pierce 2024 |

Coverage is uneven by design: it follows the papers in `papers/`. The tetrapod
pectoral and forelimb is densest because Abdala & Diogo (2010) tabulate six taxa
against every muscle. Cranial records are organised by pharyngeal arch and are
broader but shallower.

## Two views

**Muscles** — search and filter by region, taxon, or homology confidence.

**Attachments** — the topology index, inverted. Each skeletal element lists every
muscle that originates from and inserts on it. Answers "what attaches to the
coracoid?" directly.

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
assets/                 app.js, styles.css — vanilla, no dependencies
data/
  taxa.json             operational taxa + the topology that orders them
  sources.json          bibliography
  muscles-*.json        muscle records, split by region
  raw/                  git-ignored: verbatim extractions, curation aids only
docs/SCHEMA.md          data model and how to add records
scripts/
  validate.py           schema + referential integrity. Exits non-zero on error
  symmetrise_links.py   closes the related-muscle graph
  extract_werneburg_appendix.py   parses Werneburg 2011 Appendix 1 from the PDF
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
python3 scripts/validate.py              # must exit clean before committing
python3 scripts/symmetrise_links.py --write
```

The validator checks that every source key resolves, every taxon reference
resolves, every `related` and `serial.forelimb` link points at a real muscle,
no taxon appears twice in one muscle's occurrences, and every enum value is
legal. It also warns about present-but-uncited rows and never-cited sources.

Adding a muscle means editing one JSON file and reloading the page. See
[`docs/SCHEMA.md`](docs/SCHEMA.md).

## Known gaps

- **Fish and fossil coverage is thin.** Chondrichthyan and actinopterygian rows
  exist mainly as outgroup polarity for cranial muscles. The Devonian
  tetrapodomorph column is limited to the pectoral muscles Molnar et al. (2018)
  reconstruct.
- **Cranial records are coarse.** The adductor mandibulae is one record covering
  a complex that Werneburg (2011) resolves into a dozen units in turtles alone.
  `scripts/extract_werneburg_appendix.py` produces the structured source data for
  splitting it further.
- **No axial musculature.** Epaxial and hypaxial series are entirely absent.
- **No muscle architecture data.** Several sources in `papers/` (Allen et al.
  2014; Ercoli et al. 2014; Fahn-Lai et al. 2020) report PCSA, fascicle length
  and mass fractions. The schema has no field for these yet.
- **Monotreme and stem-synapsid rows are sparse** relative to the detail
  available in Gambaryan et al. (2015).
