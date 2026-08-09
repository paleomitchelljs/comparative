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

## Attachments

An attachment is a row of **bone → side → landmark**. A muscle touching several
sides or landmarks of one bone gets several rows.

- On a **muscle**, `attachments` is the consensus.
- On an **occurrence**, it is what a source records for that taxon.

Only the second is evidence of a shift. Where a taxon has no attachments on
record the consensus is shown and marked *inherited* — that means nobody has
recorded it, not that it is known to match. Inherited rows naming a bone the
taxon lacks are dropped rather than asserted.

**Attachment shifts are computed**, by diffing each taxon's recorded attachments
against the earliest taxon with data. The diff is hierarchy-aware: `humerus →
greater tubercle` is a refinement in resolution, not a muscle moving.

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
