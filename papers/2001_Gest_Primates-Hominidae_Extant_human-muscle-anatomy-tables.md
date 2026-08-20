# Gest — Medical Gross Anatomy: Anatomy Tables (muscles)

## Citation

Gest TR. *Medical Gross Anatomy — Anatomy Tables: muscles*. Texas Tech University
Health Sciences Center. Teaching resource, web. Origin, insertion, action,
innervation and arterial supply for 279 human muscles across seven regions.

No PDF is held. This is a web resource and the repository has no archived
snapshot of it, which is the one real risk attached to the source: the rows in
`data/` are the only in-repo record of what it said. A stable archive link is
worth adding.

## What it is

The distillation of human gross anatomy as taught from the dissecting room. The
attachments in it are dissection-derived in exactly the sense the comparative
monographs in this corpus are — the difference is that the human body is the most
dissected animal there has ever been, so the table states a condition confirmed
across a vastly larger sample than any single-specimen description here rests on.
It is treated accordingly: **its statements about human anatomy carry the same
weight as any other dissection-based source in this dataset.**

The one thing it is not is a comparative source. It describes one animal and
makes no homology claims across taxa, so it carries no `homologyScope` — the
same standing as Cunningham (1882) on the thylacine or Osawa (1898) on the
tuatara. Where a later comparative treatment homologises differently, that
treatment governs the homology and Gest still governs the attachment, which is
the general rule in this repository and not a judgement about this source.

## Why the human column exists

**To be the baseline.** It is the anatomy most readers already carry, and every
other column can be read against it. Pick *Homo sapiens* in the taxon selector
and the shoulder reads *supraspinatus and infraspinatus* where a lizard reads
*supracoracoideus*, the jaw reads *masseter, temporalis and the pterygoids* where
a shark reads *adductor mandibulae*, and the pelvic floor turns out to be tail
musculature.

## Scored

105 occurrence rows across 105 records and all five muscle files — the whole
human column, and Gest is the sole source on every one of them.

| Region | Rows | | Region | Rows |
|---|---:|---|---|---:|
| forearm | 19 | | pectoral | 13 |
| axial | 15 | | foot | 12 |
| cranial | 11 | | hand | 9 |
| leg | 8 | | pelvic | 7 |
| thigh | 7 | | arm | 4 |

83 rows are scored `yes` with full attachments, innervation and action; it also
supplied `division` for 38 rows — 34 `divided`, 4 `heads`.

**17 rows are scored `present: "no"`, and they are the most useful thing the
source gave.** An absence stated against a table of 279 muscles is an observation,
not a silence, and these are the rows that let a human column participate in the
phylogeny view instead of dropping out of it. The pattern they trace is a hand
that has lost muscles a foot kept: no `flexor-accessorius-lateralis` in the hand
while the foot keeps it as quadratus plantae, no `contrahentium-caput-longum` in
either, no `pronator-profundus-pes` because a human leg has no pronator — the
tibia and fibula do not rotate on each other.

**5 rows are `uncertain`, and all five are the same problem**: the human
interossei are one set of muscles that the comparative scheme resolves into
several records (`flexores-breves-profundi`, `intermetacarpales`,
`dorsometacarpales`, and their pedal counterparts). They are scored once, on the
record that carries them, and the others say so rather than double-counting.

## Where a human name is not the muscle this dataset calls by that name

This is the source's sharpest contribution and it is a nomenclature problem, not a
reliability one. Human clinical names collide with comparative ones:

- **`levator-anguli-oris`** — a human has a muscle of that name. It is not this
  record. The row is `present: "no"` and says why.
- **The human sartorius is deliberately given no home**, because Diogo & Molnar
  (2014) reject the equation with the reptilian 'ambiens' that would give it one.
  `ambiens` is scored absent in humans with the note about the muscle it is not.
- **The erector spinae group is regional labelling, not muscle identity.** Gest's
  iliocostalis, longissimus, spinalis and semispinalis are subdivisions of one
  segmentally supplied field running from the top of the neck to the sacrum.

Getting these three wrong would put a human muscle on a record it is not
homologous with, which is the failure mode the whole dataset is built to avoid.

## Relevance to comparative anatomy teaching

The reference column. Its value is not that it is unusual but that it is the one
anatomy a student already has, so every comparative statement in the dataset can
be delivered as a difference from it. The 17 absences are the teaching material:
each one is a muscle some other vertebrate has and the reader does not, which is
a more memorable fact than a list of what humans do have.

## Two files removed, 2026-08-20 — a human table cited on a cheetah and a rat

**Gest describes 279 human muscles and examines no other animal.** It was cited on
three non-human occurrences:

- *Acinonyx jubatus* on `cricoarytenoideus-lateralis`, sourced to **this table
  alone**. Its own `speciesBasis` was `default` — the schema's word for "nothing
  better, the clade's first exemplar, and a guess" — and its note is written about
  a *human* row: "Diogo et al. (2008) Table 3 gives this muscle only to the rat
  ... so the human row here rests on the descriptive source". A human observation
  had landed on a cheetah. The occurrence is deleted; nothing is lost, because the
  human reading it describes is in the table and will be filed under *Homo
  sapiens*.
- *Rattus norvegicus* on `musculus-uvulae` and `vocalis`. Both also cite
  `diogo-etal-2008-head`, which genuinely covers the rat, so removing this source
  leaves both rows properly sourced by the survey that made the observation.

Fifth instance of the failure `MINING.md` opens with, after Werneburg, Johnston,
Cieri and Molnar.

## Scope of the human re-mine — measured, not estimated

`muscles_alpha.html` is the complete alphabetical table and the one to work from;
the seven regional files are subsets of it. Parsed, it holds **272 muscles**, each
with origin, insertion, action, innervation, arterial supply and a comment column.

| | |
|---|---:|
| Muscles in the table | 272 |
| Already carrying a row of that name | 48 |
| Missing, and an existing record's id, name or synonym matches | 25 |
| **Missing, and no record matches by name** | **199** |

The dataset holds 116 rows on *Homo sapiens* from this source, under 94 distinct
names, so the gap is not a few stragglers — **it is most of the human body**.

The 199 are not all hard. Many will map on inspection: `deltoid` onto the
deltoideus records, `extensor carpi radialis longus` and `brevis` onto
`extensor-antebrachii-carpi-radialis`, the four `rectus capitis posterior` and
`obliquus capitis` muscles onto the suboccipital part of the epaxial series. But
**each is a homology call**, which is the expensive part and cannot be batched.
Expect to park a real fraction on `no-record`: the human table is finer than this
dataset's records in the hand, the foot, the perineum and the larynx.

To reproduce the diff, parse `<tr>` rows out of `muscles_alpha.html`, take cells
`[name, origin, insertion, action, nerve, artery, comment]`, normalise the name to
lowercase letters and spaces, and compare against the `name` fields in
`data/observations/homo-sapiens__gest-anatomy-tables.json`.

**Do not paste the table's prose into `data/`.** It is a copyrighted teaching
resource; paraphrase the attachments into element rows as everywhere else, and let
the citation carry the rest.
