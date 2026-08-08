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

**Origin/insertion keeps a real job** — just not this one. It becomes (a) the
cross-cutting index it already is, and (b) the *drawing instruction* for the
diagram: the edge you render between a muscle and a skeletal element. It is what
you draw, not what you navigate.

---

## Phases

Each phase is independently shippable and leaves the site working.

### Phase 1 — complete the hierarchy fields *(small, mechanical)*

Add to every muscle record:

- `layer` — currently only on the 7 fin records. Needs assigning across the other
  79. Mostly determinable from existing `subregion` text ("ventral superficial",
  "deep dorsal", "superficial palmar layer").
- `segment` — `girdle │ stylopod │ zeugopod │ autopod`. Almost entirely derivable
  from `region`: pectoral/pelvic → girdle, arm/thigh → stylopod, forearm/leg →
  zeugopod, hand/foot → autopod. Write it explicitly anyway; the cranial and fin
  records need hand assignment.

Extend `validate.py` with both enums. **Nothing else in this plan works without
this**, and it unblocks everything else.

### Phase 2 — hierarchical browse *(no new data)*

Replace the flat sidebar facets with a nested, collapsible tree following L0→L3,
each node showing its muscle count. Clicking a node filters the list; clicking
through to L4 opens the record that already exists.

This alone satisfies "click a region or muscle group and it brings you to small
subdivisions". Worth shipping before anything visual.

### Phase 3 — phylogeny view *(the "changes along the phylogeny" ask)*

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

1 → 2 → 3 → 5 → 4.

Phase 4 is the most visible but the most expensive, and it depends on both the
hierarchy fields (1) and the skeletal vocabulary. Phases 2 and 3 deliver most of
the stated goal — drill-down plus phylogenetic change — with no new data
collection at all.

## What would change my mind about the spine

If the project's centre of gravity moved toward **osteological correlates for
fossil reconstruction** — "given this scar on this humerus, which muscle?" —
then attachment-first becomes correct, because the bone is the observation and
the muscle is the inference. Molnar et al. (2018) is organised that way, and
their Tables S1–S6 are character matrices of osteological correlates.

That is a coherent second product sharing the same dataset. It is not the one
described here, and trying to serve both from one hierarchy would compromise
both.
