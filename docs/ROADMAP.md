# Path to a visual, clickable interface

Target: click a region or muscle group → drill into subdivisions → see how the
group changes along the phylogeny.

---

## The organising question

The obvious candidate for the primary structure is **origin/insertion points**.
I think that's the wrong spine, and the two papers added in August 2026 —
Diogo et al. (2016) and Mansuit & Herrel (2021) — supply the alternative.

### Why attachments shouldn't be the spine

**1. Attachments are the most labile thing about a muscle.** This is Abdala &
Diogo's own headline finding. The abductor pollicis longus attaches to digit 2
in anurans because digit 1 is gone; the abductor digiti minimi attaches to
digit 4 in urodeles because digit 5 is gone. The muscle finds the most radial or
most ulnar digit *available*. Index on attachment and these muscles change
address between clades — precisely where you most want an unbroken thread.

**2. The skeleton itself doesn't persist.** The coracoid disappears in therians,
taking the supracoracoideus origin onto the scapula with it. The fourth
trochanter goes with caudofemoralis reduction. The operculum is anuran-only.
Fin radials have no tetrapod counterpart at all. An index whose nodes evaporate
partway along the tree cannot show change along the tree.

**3. Attachments don't nest.** "Click a region, get subdivisions" needs a
partition hierarchy. Muscles × bones is a bipartite graph — great for lookup,
which is why the Attachments view already exists, but there is nothing to
drill *down* through.

**4. It would require a skeletal ontology spanning lamprey to human.** Making
bones the spine means a normalised, cross-taxon element vocabulary with its own
homology decisions. That is a multi-year project (cf. Uberon, VSAO) and it is
not this project.

### What to use instead: developmental mass and layer

Two independent papers converge on the same scheme.

**Diogo et al. (2016)** reconstruct the ancestral paired fin as five muscles in
the gnathostome LCA and six in the osteichthyan LCA, defined by **mass**
(dorsal/adductor vs ventral/abductor) crossed with **layer** (superficialis vs
profundus), plus two axial-margin muscles (pterygialis cranialis and caudalis).
Every tetrapod appendicular muscle is a subdivision of that set.

**Mansuit & Herrel (2021)** then bin *every* appendicular muscle in *every*
taxon from bichir to horse into exactly four cells — abductor superficialis,
abductor profundus, adductor superficialis, adductor profundus — and extract a
real evolutionary signal: fish appendages are deep-dominated, tetrapod limbs are
superficial-dominated, and appendage muscle mass rises from <1% to >1.7% of body
mass across the transition.

That is empirical validation that these cells are a workable unit of comparison
across the whole range this project covers. Three further points in its favour:

- **Innervation confirms it independently.** Dorsal-mass derivatives take the
  radial and axillary nerves; ventral-mass derivatives take the median, ulnar
  and musculocutaneous. The dataset already records this on every record, and it
  is why `mass` is trustworthy in a way that `attachment` is not.
- **It is already in the data.** `mass` on every limb record, `arch` on every
  cranial record, `layer` on the fin records.
- **It roots the drill-down at the ancestral state**, which is exactly the
  starting point for showing change along a tree.

### Proposed hierarchy

```
L0  Body region       head │ pectoral appendage │ pelvic appendage │ axial (future)
L1  Developmental origin
      appendicular      mass: dorsal (adductor→extensor) │ ventral (abductor→flexor) │ axial-derived
      cranial           arch: 1 │ 2 │ 3–7 │ extraocular │ hypobranchial
L2  Layer              superficialis │ profundus │ preaxial │ postaxial │ primaxial
L3  Segment            girdle │ stylopod │ zeugopod │ autopod
L4  Muscle             the homology group (current record)
L5  Occurrence         one taxon's version of it
```

Each level partitions the level above, so it drills. And because L1–L3 are
conserved while L4–L5 are where change happens, the phylogeny view has somewhere
stable to hang the changes off.

**A caveat the sources forced.** Johnston (2011, 2014) shows that for the jaw
adductors the reverse holds: he explicitly rejects trigeminal-branch position as
a homology criterion in favour of *where a component inserts* into the inverted U
of the folded sheet. So attachment beats innervation there. The general claim is
not "innervation wins" but "use whichever signal is stable in the system you are
in" — labile attachment in the limb, labile nerve topography in the jaw.

**Origin/insertion keeps a real job** — just not this one. It becomes (a) the
cross-cutting index it already is, and (b) the *drawing instruction* for the
diagram: the edge you render between a muscle and a skeletal element. It is what
you draw, not what you navigate.

---

## Phases

Each phase is independently shippable and leaves the site working.

### Phase 1 — hierarchy fields and the attachment model — **DONE**

`segment` on all 92 records; `layer` on 41 of 77 appendicular ones, inherited
through `derivatives` from the ancestral fin muscle where Diogo et al. (2016)
support it and left blank otherwise.

Went further than planned, on the project owner's steer that attachment change is
itself data and that bone-first is how students reason. `data/skeleton.json` now
holds 121 attachment sites with a `partOf` hierarchy, per-taxon presence and
osteological-correlate flags, and attachments are `{element, side, landmark}`
rows rather than flat strings.

### Phase 2 — hierarchical and bone-first browse — **DONE**

Two views shipped: **Skeleton** (bone-first drill-down with a taxon selector) and
**Mass & layer** (the L0→L3 hierarchy). Attachment shifts are computed by diffing
per-taxon rows, hierarchy-aware so that a move to a finer landmark reads as a
refinement rather than a transition.

### Phase 3 — phylogeny view — **DONE**

Shipped as the **Phylogeny** view. Branch states are optimised by **Fitch
parsimony** over the topology in `taxa.json` (`assets/phylogeny.js`), not read off
the tip states. Across all 92 muscles it infers 22 gains and 15 losses over 26
informative characters.

Three decisions that the honest reading forced, all surfaced in the interface:

- **Missing data constrains nothing.** A taxon with no occurrence row is left
  unscored. Treating absence of data as absence of the muscle would invent losses
  across the whole fish end of the tree, where sampling is thinnest.
- **`variable`, `uncertain` and `inferred` are scored polymorphic**, not forced
  to presence or absence. `variable` means a source found the muscle in some
  species of a clade and not others; `inferred` is a fossil reconstruction.
- **Equivocal placements are marked, not hidden.** Where the root state is
  ambiguous — both states cost the same number of steps — the convention used is
  *absent at the root*, since muscles are acquired rather than primitively
  universal. Flip that and gains become losses elsewhere at identical cost. 19 of
  the 37 inferred changes are equivocal in this sense and carry a `?`.

`tests/fitch.test.js` covers the optimisation, and runs in CI. It exists because
the first implementation silently reported "no change" whenever the root state
was ambiguous — the one failure mode that looks like a clean result.

<details><summary>Original plan</summary>

The presence data is **already a character matrix**: 86 muscles × 16 taxa, with
states `yes │ no │ variable │ uncertain │ inferred`. The topology is already in
`taxa.json`. So:

- Render the tree from `taxa.json` (SVG, rectangular cladogram — ~16 tips, small).
- For a selected hierarchy node, annotate each branch with **gains**, **losses**
  and **subdivisions**. Subdivisions come free from the `derivatives` edges added
  with the fin muscles.
- Show the muscle-count trajectory per branch. Diogo et al. (2016) hand us the
  numbers — 10 → 12 → 35 → 30 → 107 — and they are already in `taxa.json` as
  `muscleCount`. The counterintuitive result (the big jump is *before* the
  sarcopterygian LCA, not after) is worth making the default view.

**Two honest caveats.**

First, this is character *mapping*, not ancestral state *reconstruction*. Doing
it properly means parsimony or likelihood optimisation over the tree. Displaying
naive gains/losses without saying so would overstate what the data support. Label
the view accordingly, or implement Fitch parsimony — it is maybe 60 lines for
binary characters on a fixed topology and would be defensible.

Second, `variable` and `inferred` are not binary states. `variable` means the
source found the muscle in some species of the clade and not others — mapping it
as either presence or absence is wrong. Render it as a distinct branch state.

</details>

### Phase 4 — the clickable anatomical diagram

The big lift, and where origin/insertion finally drives the visuals.

**Recommendation: schematic, not accurate.** Anatomically faithful figures for
16 taxa × 4 regions is not a realistic hand-drawing job, and inaccurate art that
looks accurate is worse than an obvious diagram. Draw one **schematic
appendage** — girdle, stylopod, zeugopod, autopod as blocks — and one schematic
head with the arches as bands. Then:

- Clickable zone per segment → drills into the L3 node.
- Muscles drawn as bands between their `attachments.origin` and
  `attachments.insertion` blocks, coloured by `mass`, hatched by `layer`.
- A taxon selector redraws the same schematic with that taxon's muscles present,
  so switching taxa *is* the visualisation of change.

This works because the schematic's blocks are the L3 segments — conserved — while
the bands are the muscles — variable. The diagram inherits the hierarchy rather
than fighting it.

Prerequisite: the `attachments` vocabulary needs a controlled term list mapping
each element to a segment block. Currently it is free strings kept consistent by
convention. Perhaps 40 terms; a `data/skeleton.json` with
`{element, segment, appendage, taxaPresent}` would do it.

### Phase 5 — muscle architecture

Closes the gap Mansuit & Herrel name explicitly. Add an optional `architecture`
block (mass fraction, PCSA, fascicle length, pennation) at occurrence level.
Several sources are already in `papers/`: Allen et al. 2014, Ercoli et al. 2014,
Fahn-Lai et al. 2020, Klinkhamer et al. 2017. Mansuit & Herrel's reference list
identifies the rest (Huby et al. 2021 for *Latimeria*; Dick & Clemente 2016 and
Cieri et al. 2020 for varanids; Payne et al. 2005 for horse).

Unlocks the deep→superficial investment shift as a quantitative view over the
same four-cell classification.

---

## Suggested order

Phases 1, 2 and 3 are done. Remaining: **5 → 4**.

See [`GAPS.md`](GAPS.md) for the measured picture. The short version: the
presence matrix is dense (92 × 16, complete) so **phase 3 needs no new data**,
but per-taxon attachments cover only 13% of occurrences and are absent entirely
for fish, fossil taxa, the hand and the foot — so **phase 4 should be scoped to
the pectoral girdle and arm** until that improves, or it will draw the consensus
and label it as sixteen different animals.

## What would change my mind about the spine

If the project's centre of gravity moved toward **osteological correlates for
fossil reconstruction** — "given this scar on this humerus, which muscle?" —
then attachment-first becomes correct, because the bone is the observation and
the muscle is the inference. Molnar et al. (2018) is organised that way, and
their Tables S1–S6 are character matrices of osteological correlates.

That is a coherent second product sharing the same dataset. It is not the one
described here, and trying to serve both from one hierarchy would compromise
both.
