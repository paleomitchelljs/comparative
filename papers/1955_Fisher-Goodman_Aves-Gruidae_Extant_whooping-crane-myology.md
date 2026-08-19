# Fisher & Goodman (1955) — The myology of the whooping crane, *Grus americana*

*Illinois Biological Monographs* 24. 156 pp.
Source key: `fisher-goodman-1955`

## Why it was reached for

Aves is the largest gap in the dataset (48 unscored occurrences) and was
**source-limited**: its rows cite a synonymy survey (Abdala & Diogo), a penguin,
a plate atlas, and two musculoskeletal models, none of which states an attachment
in prose. This is a complete myology of a **flying neognath**, with formal
`Origin.—` and `Insertion.—` paragraphs. On paper it is the answer.

## The OCR is not the constraint. A search pattern was.

**An earlier version of this note said this paper could not be bulk-extracted.
That was wrong, and the way it was wrong is worth keeping.**

It reported 83 recoverable `Origin.—` paragraphs and concluded the scan had eaten
the rest. But the OCR spells that heading four ways — `Origin.—`, `Origin —`,
`Origin—`, and the same three for `Insertion` — and a pattern anchored on the first
has **49% recall for origins and 38% for insertions**. Searching for any of the
four returns **115 origin and 115 insertion paragraphs**. The missing half was
never missing.

The named casualty was checkable, and it survives intact. The note said the
insertion of M. extensor metacarpi radialis was lost to noise. It is on the page:
the fused tendon "continues across the anterior surface of the wrist and deep to
the tendon of M. tens. pat. longus," then attaches "to the proximal side of the tip
of the extensor process of metacarpal I[I]". The heading above it reads
`Insertion —tThe`, which the strict pattern skips.

**Actual state of the scan.** 135 of the 142 text-bearing pages are clean prose.
Seven are garbled: pp. 11, 15, 16, 60, 61, 64, 98. Those read as page images, the
same treatment the Diogo tables and the Gheție plates needed. What looked like
noise on the good pages is the figure legends, which are printed sideways and
collapse into the right margin of the text layer — the descriptive column beside
them is unaffected.

**What is actually here.** 193 indented `M.` headings, 116 of them carrying an
explicit origin paragraph, spanning cranial, hyoid and tongue, pectoral, arm,
forearm, hand, tail, pelvic, thigh, leg, foot and axial.

**It does not close the unscored Aves rows, and an earlier note here implied it
would.** All 41 of those sit on *Gallus* (30), *Struthio* (10) and *Gavia* (1).
This paper describes a crane, so it cannot score them — WORKLIST is right that
Abdala & Diogo's synonymy is what those *Gallus* rows are stuck on. What it does
is build a **second fully scored avian column**, which is the thing the roadmap
actually needs: a shift is computable only where two taxa are scored for the same
muscle.

The general lesson is the one Gheție taught in the other direction: **check the
recall of the pattern before concluding the text is not there.** A negative result
from a grep is a fact about the grep.

## Two findings from the pages that did survive

**The extensor digitorum communis has a second, feather-linked attachment.** Its
origin tendon sends a wide vinculum posteriorly to insert along a line on the
postero-anconal corner of the ulna, *just anterior to the row of papillae for the
secondary feathers*. An aponeurotic attachment tied directly to the flight-feather
apparatus, and the sort of thing a cross-tetrapod record cannot express without a
per-taxon note.

**The flexor digitorum profundus uses the pisiform process as a pulley** rather
than as an insertion — its tendon hooks around the anterior aspect of the process
on the way to the metacarpus.

## Nomenclature warning

1955 avian terms throughout, and the digit numbering differs from modern usage:
`M. abductor alae digiti II [abductor pollicis]`, `M. flexor digiti IV
[flexor digiti III]`. The bracketed alternatives in the text are the authors' own
cross-references and are the safest bridge. Abdala & Diogo's Table 1 *Gallus*
column is the other bridge, but its column offsets shift page to page in the
extracted layout, so it needs reading rather than grepping.

## Scored (6)

`extensor-digitorum` and `flexor-digitorum-longus` from an earlier pass, plus four
from the forearm block, all on *Grus americana* with origin and insertion rows:

| Record | Origin | Insertion |
|---|---|---|
| `extensor-antebrachii-carpi-radialis` | ectepicondylar prominence | processus extensorius of the carpometacarpus |
| `supinator` | ectepicondylar prominence | radius, dorsal and anterior faces |
| `anconeus` | ectepicondylar prominence | ulna, anterior and dorsal faces |
| `flexor-carpi-ulnaris` | medial surface of the internal humeral condyle | postero-proximal edge of the os cuneiform (the avian ulnare) |

The bridge for the first was already in the dataset: the *Gavia* and *Cygnus* rows
on that record are named "Extensor metacarpi radialis", which is this paper's term
exactly. `carpometacarpus`'s own element note already said its processus
extensorius carries that insertion.

**Anconal and palmar are dorsal and ventral** in this paper's usage, and the rows
are translated accordingly.

## Deliberately not mapped yet

- **The pronators.** This paper has M. pronator brevis and M. pronator longus, both
  from the internal humeral condyle onto the radius. The dataset's avian rows are
  *pronator superficialis* and *pronator profundus* (Gavia, Cygnus). Brevis/longus
  does not map onto superficialis/profundus by name, and this paper gives no
  bracketed cross-reference for them, so guessing would put an observation on the
  wrong record. Needs a source that states the synonymy.
- **The hand.** M. interosseus dorsalis and ventralis, M. abductor alae digiti II,
  M. flexor digiti IV, M. abductor major digiti II and M. extensor brevis digiti I
  are all described with full attachments, but the digit numbering is the 1955
  scheme and the receiving records (`intermetacarpales`, `dorsometacarpales`,
  `flexores-breves-profundi`) need the numbering settled first.
- **The pectoral, arm, pelvic, thigh, leg, foot, tail, cranial and axial blocks.**
  All legible, none read at row level.
