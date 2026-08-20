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

## Mined in full

**Every muscle this paper describes with an origin paragraph is now extracted** —
111 of them — and the paper should not need reading again except to check this
pass. That was the point of the pass: the reading is the expensive part.

| | |
|---|---|
| Muscles with an origin paragraph | 111 |
| Filed as *Grus americana* occurrences | 43 rows, covering 61 of those muscles |
| Parked in `observations.json` | 50 |

Aves went from 118 present / 77 scored to **155 / 114**, and *Grus americana*
from 6 occurrences to 43. The crane is now the best-scored bird in the dataset
and the second scored avian column the roadmap needs.

### Filed

Wing and girdle: `pectoralis`, `supracoracoideus`, `sternocoracoideus`,
`latissimus-dorsi`, `rhomboideus`, `serratus-anterior`, `subcoracoscapularis`,
`deltoideus-scapularis`, `coracobrachialis`, `protractor-pectoralis`,
`biceps-brachii`, `triceps-brachii`, and the six forearm records from the earlier
pass.

Hindlimb: `caudofemoralis`, `iliofibularis`, `ischiotrochantericus`,
`adductor-femoris`, `femorotibialis`, `extensor-iliotibialis`, `ischioflexorius`,
`fibularis-group`, `tibialis-anterior`, `gastrocnemius`,
`extensor-digitorum-longus-hl`, `flexor-digitorum-longus-hl`.

Axial and tail: `rectus-abdominis`, `transversus-abdominis`, `obliquus-internus`,
`iliocostalis`, `levator-costae`, `caudal-musculature`.

Cranial: `depressor-mandibulae`, `levator-arcus-palatini`, `interhyoideus`,
`hypobranchial-muscles`, `thyroarytenoideus`, `adductor-mandibulae-externus`,
`adductor-mandibulae-internus`.

**Anconal and palmar are dorsal and ventral** in this paper's usage, and the rows
are translated accordingly.

**One convention the validator enforced.** The cnemial crest is `partOf: tibia`,
and `fusedFrom` is deliberately not containment in this schema, so an avian crest
attachment is not reachable through the `tibiotarsus`. Four rows were rewritten
onto `tibia`, which is what the dataset's other avian rows already do.

### Parked, and why

Nothing was skipped. What could not be filed is in
[`data/observations.json`](../data/observations.json) with its full origin and
insertion prose and a note saying what would settle it:

| Blocked on | n | What it is |
|---|---:|---|
| `no-record` | 20 | The avian neck, the tracheal and lingual muscles, the propatagial complex — groups this dataset has no record for. Boumans et al. (2015), uncited in `papers/`, would build the cervical set |
| `nomenclature` | 19 | 1955 names with no stated modern equivalent: the pronators, the hand under the old digit numbering, the pelvic set. Hudson et al. (1972) or Vanden Berge & Zweers's *Myologia* would state the synonymy |
| `division` | 11 | Named subdivisions whose record already carries a *Grus* row for another part, and the avian perforated flexor system |

One row is parked because **its heading did not survive the scan** — it prints as
"M. spinalis cervicis" twice, but the block beneath is a subvertebral muscle
arising from the transverse processes, not the spinalis cervicis, which is
described separately. The text is kept intact rather than guessed at.

