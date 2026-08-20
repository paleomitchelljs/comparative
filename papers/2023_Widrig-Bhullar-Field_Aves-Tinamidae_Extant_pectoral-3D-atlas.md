# Widrig, Bhullar & Field (2023) — 3D atlas of tinamou pectoral morphology

*Journal of Anatomy*. doi:10.1111/joa.13919. Open access.
Source key: `widrig-etal-2023`

## Why it was reached for

Aves is the largest gap in the dataset and Fisher & Goodman (1955), the obvious
source, turned out to be an uneven scan that has to be read page by page. This is
modern, open access, contrast-enhanced CT of *Nothoprocta pentlandii*, with clean
text and current avian nomenclature — the highest yield per effort left in the
avian corpus.

Scored: **21 rows on 12 records**, plus one parked. Three came from the first pass —
`scapulohumeralis-anterior`, `scapulohumeralis-posterior`, `deltoideus-clavicularis`
— and 18 more once the column problem below turned out not to be one.

### The girdle and arm, mined 2026-08-20 — sections 3.2.1 to 3.2.22

Both latissimus parts and the metapatagial slip, both coracobrachiales, the two
deltoid parts the first pass missed, supracoracoideus, pectoralis and its propatagial
slip, sternocoracoideus, subscapularis, subcoracoideus, both triceps heads, biceps
and brachialis. Five rows worth reading on their own:

- **The supracoracoideus tendon through the triosseal canal.** The muscle that raises
  the wing arises below the centre of mass and pulls upward through a pulley made of
  three bones. One row, and it is the whole flight apparatus.
- **M. subcoracoideus does not touch the coracoid.** It runs dorsally past it from the
  internal rostral spine of the sternum, merges with the subscapularis and inserts
  with it. A muscle named for a bone it has left.
- **Two muscles end in the patagium rather than on the skeleton**: the pectoralis pars
  propatagialis, and the deltoideus pars propatagialis, which does not insert at all —
  it becomes the propatagial ligament.
- **The latissimus dorsi pars caudalis ends on skin and on two other muscles**, one of
  them the scapulotriceps, scored as a muscle attachment.
- **The biceps brachii can only be half confirmed, and it is the half that matters.**
  Widrig et al. resolve the humeral head from the bicipital crest and cannot find the
  coracoid tendon that Hudson et al. (1972) and Suzuki et al. (2014) report. A
  coracoid origin is the plesiomorphic amniote condition and a humeral head is the
  neognath novelty, so a palaeognath with both is the intermediate — and this scan
  sees one of the two.

**`after` is not set on the latissimus rows**, and the reason is a schema limit worth
recording: the three parts report different workers, they merge into one occurrence,
and an occurrence carries one `after`. The build refused the conflict, correctly. The
attributions live in each part's prose.

**M. expansor secundariorum is parked** on `no-record`. It spreads the secondary
remiges and no non-avian tetrapod has anything to correspond to it; filing it means
first deciding whether feather muscles get records at all.

### Still to do — sections 3.2.23 to 3.2.45

Twenty-three antebrachial and manual muscles, from the pronators to the alular and
interosseous groups. Many are avian novelties that will park; the pronators,
supinator, the carpal extensor and flexor groups and extensor digitorum communis map
onto records this dataset holds. The source stays `not-started` until they are done.

## ~~Why only three: the columns interleave~~ — overturned 2026-08-20

The verdict was: the PDF is two-column, `pdftotext` interleaves adjacent
descriptions, the block under `3.2.12 | M. deltoideus pars major` is half
scapulohumeralis cranialis and half a triosseal-canal description, and anything
scored from it would be a guess. So only descriptions that identify themselves in
their own first clause were used, and the rest were said to need "the figures, or a
column-aware extraction".

**A column-aware extraction is one line.** The `-layout` output already keeps the
two columns side by side on every line. Slice each page at character 73, print the
left half then the right half, and all 45 muscle sections come out clean, complete
and self-consistent — no new tool, no figures, no re-download.

Read that way, section 3.2.12 is a single coherent paragraph: a fleshy origin on the
medial acrocoracoid process, possibly extending onto the connective tissue round the
triosseal canal, insertion on the dorsocaudal proximal humeral shaft. Nothing is
interleaved. **The interleaving was in the reading, not in the file.**

**Third instance of a tooling verdict that expired**, after Liparini & Schultz —
whose note also named the fix and was not run — and Fisher & Goodman, where a grep's
recall was mistaken for the absence of text. A tooling claim is a claim about a tool
at a moment, and it should be retested before it is planned around.

## The finding worth keeping

**The avian clavicular deltoid takes a furcular origin.** M. deltoideus pars minor
arises from the lateral acrocoracoid process of the coracoid *and the acromial
process of the furcula*. This record is the clavicular deltoid across tetrapods;
in birds the clavicles are fused into the furcula, so the homology is carried by a
bone that no longer exists as a pair. That is the fusion machinery in
`skeleton.json` earning its place on a muscle record rather than only on an
element.

## A word-collision the validator caught

The **"acromial process of the furcula" is not the scapular acromion.** Scoring it
as `landmark: acromion` failed on the parent: the furcular process is not part of
the scapula. Two different structures sharing a word, and the containment check is
what separated them. The row is scored on the furcula with the detail in the note.

**The second half of that reasoning has since been overturned.** This note used to
add that the row also failed because "the acromion is correctly recorded as absent
in birds". It was not correct. Widrig et al. describe the tinamou **scapular**
acromion projecting cranially in the same paper, Schreiweis (1982) gives three
penguin muscles an origin on the acromial process of the scapula, and Meers (2003)
names it repeatedly in crocodylians; the element is now scored present in Aves and
Crocodylia. The furcular/scapular distinction stands on its own and never needed
the presence argument — which is the lesson, since a correct conclusion was being
propped up by a wrong premise and the pair travelled together for several passes.

## Not covered by this paper

`protractor-pectoralis` (the avian occurrence is cucullaris capitis/cervicis, a
neck muscle outside a pectoral atlas) and `rhomboideus`. Neither appears in the
muscle list.
