# How to read this dataset

Everything the interface used to say inline. Kept here so the pages can be about
muscles.

---

## Sourcing

Every anatomical statement is a paraphrase of a cited source, not a verbatim
quotation. Every homology claim is a hypothesis attributed to a named author.
Confidence labels (`well-supported`, `moderate`, `contested`, `uncertain`)
reflect the strength of support reported in the literature, not certainty.

## Presence states

| State | Means |
|---|---|
| `yes` | The cited source examined this taxon and found the muscle |
| `no` | The source examined this taxon and did not find it |
| `variable` | Found in some species of the clade and not others |
| `uncertain` | The source flags the identification as unresolved |
| `inferred` | A fossil reconstruction — bracket-and-osteological-correlate, not an observation |

`no` is a claim about the exemplar species, **not the clade**. Abdala & Diogo
(2010) document several muscles present in one lizard and absent in another; that
is what `variable` is for.

## Skeletal elements

Elements are homology groups, like muscles. One element, different names in
different taxa: the hyomandibula of a shark, the columella of a lizard and the
stapes of a mammal are one record, and the interface shows whichever name fits
the taxon you have selected. Where an ancestral element *split* — the
scapulocoracoid into scapula and coracoid — the descendants are separate records
linked by `derivedFrom`.

`presence` records where an element is absent, which is what lets the interface
say a muscle's attachment *had to move* rather than silently dropping a row.
Attaching a muscle to an element its taxon lacks is a validation error.

## Attachments

An attachment is a row of **bone → side → landmark**. A muscle touching several
sides or landmarks of one bone gets several rows.

- On a **muscle**, `attachments` is the consensus.
- On an **occurrence**, it is what a source records for that taxon.

Only the second is evidence of a shift. Where a taxon has no attachments on
record the consensus is shown and marked *inherited* — that means nobody has
recorded it, not that it is known to match. Inherited rows naming a bone the
taxon lacks are dropped rather than asserted.

**A fusion must never break the homology of what fused.** There are two ways to
honour that, and which one applies depends on the source.

*Score the components* where the source decomposes the compound. The salamander
pubo-ischiac plate is recorded as `pubis` plus `ischium`, because Walthall &
Ashley-Ross gloss the plate that way and the muscles can be assigned to each.
Giving the plate a record of its own would put the salamander's
puboischiofemoralis on a different bone from every other tetrapod's — the same
mistake as splitting the hyomandibula from the stapes.

*Record the compound with `fusedFrom`* where the source treats it as the unit of
observation. Hattori & Tsuihiji record avian attachments on the tarsometatarsus;
splitting those across distal tarsals and metatarsals would assert which
component a muscle reaches when the source does not say. So the tarsometatarsus,
tibiotarsus and pygostyle are elements in their own right, each naming what went
into it.

What they must **not** be is `partOf` a component, which is how all three were
filed until they were migrated. `partOf` means containment within one bone and
the attachment diff reads it that way, so a bird inserting on the tarsometatarsus
compared against a crocodylian inserting on the metatarsals reported as a
*refinement* — one author being more precise than another. It is a bone that has
absorbed its neighbours. The diff now reports that as its own category, and
because it is a change in the skeleton rather than in where the muscle attaches,
it does not count as a substantive shift.

`derivedFrom` runs the other way, for genuine fission (scapulocoracoid into
scapula and coracoid). `fusions.csv` exports both directions as one character.

**Where a source's term is ambiguous, no landmark is asserted.** A muscle whose
origin is described as the femoral "crista ventralis" is scored as `femur` /
ventral, not as the fourth trochanter; a "spine of the tibia" as `tibia` /
anterior, not the cnemial crest. Each identification is plausible and
unestablished, and asserting it would manufacture an osteological correlate that
no source claims.

**Attachment shifts are computed**, by diffing each taxon's recorded attachments
against the earliest taxon with data. The diff is hierarchy-aware: `humerus →
greater tubercle` is a refinement in resolution, not a muscle moving.

## What correlates can and cannot do

An osteological correlate locates an attachment. It does not size the muscle.
Leavey et al. (2024) find that bone lengths and pelvic crest sizes are generally
not reliable predictors of muscle size across 30 frog species, and report
many-to-one form-function mapping. Treat a correlate as evidence that a muscle
attached there, not as a measurement of it.

Actions are structured as well as written out: every muscle carries `actions`
pointing at `data/joints.json`, where a joint records which bone surfaces
articulate. Because joints are stored as ordered pairs they form a graph over
the skeleton, so the joints a muscle crosses are **derived** from its
attachments rather than asserted — and a stated action can then be checked
against them. Four muscles act on joints they do not span, all of them through
another muscle's tendons; the check reports rather than corrects, because the
graph cannot follow a tendon.

Innervation is now structured as well as written out: every muscle carries
`nerves` pointing into `data/nerves.json`, where nerves are homology groups with
a `partOf` chain to the plexus. Because the dorsal/ventral division is inherited
down that chain, the dataset can check a limb muscle's nerve against its
limb-bud `mass` — the two should agree, and the validator says so when they do
not. See [`SCHEMA.md`](SCHEMA.md).

Conversely, several sources here weight **attachment geometry over innervation**
where nerve topography turns out to be labile: Johnston (2011, 2014) on the jaw
adductors, Winterbottom (1973) on the same complex in teleosts, and Hattori &
Tsuihiji (2021) on the pedal muscles. Elsewhere — the limb masses, the
epaxial/hypaxial division — innervation is the stable signal and attachment is
the labile one. The dataset does not rank the criteria globally; it records which
one each source relied on and why.

For the conceptual background on what a homology claim is, Richardson (2022)
reviews the theories and models in play.

## Homology and serial correspondence

Muscle records are **homology groups**, not muscles-in-an-animal. The same muscle
carries six names across Abdala & Diogo's Table 1; the same name is applied to
non-homologous muscles (twelve human hindlimb names are used for non-homologous
anuran muscles). Names are therefore attributes of taxon-specific occurrences.

Forelimb ↔ hindlimb `serial` correspondences follow Diogo & Molnar (2014) and
denote **topological** equivalence only. That paper rejects serial homology in
the strict ancestral-duplication sense, and several correspondences are flagged
where the developmental anlagen are known to differ.

Quoted muscle names (`'Rhomboideus'`, `'Palmaris longus'`, `'Ambiens'`) follow
the sources' own convention for a name whose homology is not established.

---

## The phylogeny view

Branch states are optimised by **Fitch parsimony** over the fixed topology in
`taxa.json` — not read off the tip states. Three consequences:

**Missing data constrains nothing.** A taxon with no occurrence row is left
unscored. Treating absence of data as absence of the muscle would invent losses
wherever sampling is thin, which is most of the fish end of this tree.

A record scored in only one taxon is the mirror of this: it optimises as a gain on
that branch, which is the correct parsimony statement given the data but reads
like an apomorphy. Several intrinsic pedal muscles are currently in that state,
scored from *Taricha torosa* alone. Each says so in its occurrence note.

**Polymorphic tips.** `variable`, `uncertain` and `inferred` are scored as
{absent, present} rather than forced either way. None is an observation of
presence, and none should push a transition onto a branch by itself.

**Equivocal placements**, marked `?`. Where the state at the root is itself
ambiguous, both states cost the same number of steps, and a convention decides
where the change is drawn. The convention used is **absent at the root**, since
muscles are acquired rather than primitively universal. Flip that assumption and
the gains become losses elsewhere at identical cost. Currently 19 of 37 inferred
changes are equivocal in this sense.

**One topology, no support.** The tree is a pragmatic consensus — including
Abdala & Diogo's placement of turtles as archosauromorphs — and the counts would
change under a different one. No branch supports are computed.

`tests/fitch.test.js` covers the optimisation and runs in CI.

### Muscle counts

The per-appendage counts plotted under the tree are Diogo et al. (2016) figures
for their exemplar species, **not** counts of records in this dataset. The two
differ and should not be reconciled.

The comparison worth making: *Polypterus* → *Latimeria* is a jump of 23;
*Latimeria* → *Ambystoma* excluding the autopod is a jump of 20. Most of the
fin-to-limb change had already happened before the sarcopterygian last common
ancestor.

---

## Views

**Muscles** — search by name, synonym, taxon-specific name, or bone.

**Skeleton** — bone-first. Drill down through the skeleton, see what originates
and inserts at each level, optionally as recorded in one taxon. Elements a taxon
lacks are flagged rather than hidden.

**Mass & layer** — developmental origin → layer → proximodistal segment. The axis
that survives deep transitions.

**Phylogeny** — gains and losses along the tree, as above.

---

See also [`SCHEMA.md`](SCHEMA.md) for the data model and [`GAPS.md`](GAPS.md) for
measured coverage.
