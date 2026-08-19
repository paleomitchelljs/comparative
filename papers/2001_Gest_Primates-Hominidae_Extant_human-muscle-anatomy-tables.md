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
