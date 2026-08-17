# Walker (1973) — The locomotor apparatus of Testudines

*Biology of the Reptilia* 4 (Morphology D), pp. 1–100. `walker-1973`.
Free from the [Gans Collections and Charitable Fund](https://carlgans.org/biology-reptilia-full-content/).

## Why this is the acquisition that mattered

It was ranked first by a citation sweep over the whole corpus — nine of our papers
cite it, with 106 mentions in attachment context — and independently named by the
mining passes, which found that **31 of Testudines' 34 unscored rows cited only
Abdala & Diogo's synonymy**. Turtles were not under-mined; the corpus simply had no
descriptive turtle myology. This is it: 100 pages, 212 attachment statements, and a
per-muscle synonymy running back to Bojanus (1819–21).

## The species, and why it is the right one

**Walker's type is *Pseudemys scripta elegans*** — the red-eared turtle, now
***Trachemys scripta elegans***. That is the animal this dataset had already chosen
as its Testudines exemplar. After four sources in a row turned out to be cited for
animals they never examined, this one lands on the species the rows were already
standing on. The turtle column was right; it was waiting for its source.

Compared throughout against his own dissections of *Testudo graeca*, *Geochelone
elephantopus*, *Trionyx spiniferus*, *Caretta caretta* (pelvic), *Lepidochelys
kempii* (pectoral), *Pelomedusa subrufa* and *Chelodina longicollis*.

## What the shell does to a shoulder

The finding that reshaped `skeleton.json`. Turtle forelimb muscles originate from
the **shell**, and no other tetrapod has one, so the elements did not exist here:

- **Pectoralis** — from much of the anterior **plastron**, an arc from the
  midventral line just behind the acromion's plastral attachment, back and
  laterally to the bridge; onto the flexor border of the lateral humeral process.
- **Deltoideus** — a third of its origin is shell: anterior **scapular prong**,
  anterior **acromion**, and the median **epiplastron** with adjacent
  **entoplastron**.
- **Latissimus dorsi** — from the **carapace**, along a line from the scapular
  articulation out over the first pleural plate.
- **Teres major** — anterior surface of the dorsal half of the scapular prong and
  the suprascapular cartilage, converging with latissimus on a *common* tendon.

Seven elements added: `carapace`, `plastron`, `epiplastron`, `entoplastron`,
`scapular-prong`, `humerus-lateral-process`, `humerus-medial-process`. The turtle
humerus carries two proximal processes rather than the tubercles of other amniotes,
and Walker reads the distal shift of the lateral process in sea turtles as
increasing the adductor moment arm.

## And a third clade for the acromion

Walker names the acromion as a discrete ramus of the triradiate turtle scapula and
puts **two** muscles on it — the deltoideus on its anterior surface, the anterior
head of the supracoracoideus on its ventral surface and posterior border.
`acromion` was scored mammal-only until this month; it is now Monotremata, Theria,
Crocodylia, Aves and Testudines. **Twice now a descriptive source has contradicted
that record's scoring**, which is a reasonable argument that the remaining
unscored clades are unrecorded rather than absent.

## Scored so far

**Pectoral:** `pectoralis`, `deltoideus-scapularis`, `teres-major`.
**Arm:** `triceps-brachii`, `coracobrachialis`, `biceps-brachii`, `brachialis`.

Testudines 35% → 48%, pectoral 78% → 80%, arm 72% → 78%.

Two divisions came with the arm pass. The **coracobrachialis** splits into magnus
and brevis, the brevis inserting into the intertubercular fossa. The **biceps** is
double in most turtles but single in *Testudo*, *Dermochelys* and *Lepidochelys* —
and Walker (1947) showed from *Chrysemys* development that the complex starts as
one mass and splits later, so the single condition is unsplit rather than lost.
That is a division-state difference with an ontogenetic argument attached, which is
exactly what the `division` field exists to hold.

One nice piece of topology the rows cannot express: in *Pseudemys* the scapular
head of the triceps arises by a tendon that **perforates the latissimus–teres major
tendon**. Two rows on this animal are physically threaded through each other.

**Deliberately partial.** The arm, forearm and hand series are still open — Walker
describes them in the same detail, and they are the remaining ~28 Testudines rows.
The deltoideus row carries an origin and **no insertion**, because the passage that
gives the origin does not state where it ends; that is the source's shape, not a
gap in the reading.
