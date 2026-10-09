# The muscle simulator

`simulator.html` draws a schematic skeleton for up to four taxa side by side, with
their muscles attached. You pick a joint and a movement, or a single muscle, and
every panel moves. The comparison table underneath says which muscles shorten,
which stretch, and where a source records a muscle as absent.

## What it claims, and what it does not

The anatomy comes from the cited papers: which muscles exist, where each attaches,
and the action each is credited with. The geometry does not. Outlines, lever arms
and ranges of motion are illustrative. What stops that from drifting is
`tests/sim.test.js`: every drawn muscle carries an `expect` list (the action its
source states) and the test moves every joint and checks that the geometry
reproduces it. A landmark nudged for looks cannot quietly reverse a muscle.

A muscle's action is **derived**, not stored. Shortening it moves whichever joints
change its length, in whichever direction shortens it, the same way
`jointgraph.py` derives the joints a muscle spans from its attachments.

## Files

| File | Job |
|---|---|
| `assets/sim/engine.js` | Kinematics. No DOM; the page and the test load the same file |
| `assets/sim/sim.js` · `sim.css` · `simulator.html` | The page |
| `data/sim/index.json` | Regions, the joint vocabulary, and the comparative muscle groups |
| `data/sim/<region>-<species>.json` | One model: one region of one animal |

## A model

Segments in a parent chain, degrees of freedom (DOFs) that move them, landmarks
pinned to segments, and muscles as paths through landmarks. The first landmark of
a path is the origin, the last the insertion. DOF ids (`jaw`, `hyoid`, ...) are
shared across models and defined once in `index.json`, which is why one button
drives every animal that has that joint.

A muscle the source records but the model cannot draw has `paths: []` and a
`reason`. A muscle a source reports absent has `status: "absent"`. Both appear in
the table; neither is guessed at. Muscle `record` is the homology group in
`data/muscles-*.json`, or `null` where the dataset has parked the row.

## Adding a taxon

1. Write `data/sim/<region>-<species>.json`, copying the nearest existing model.
2. List it under the region's `models` in `index.json`.
3. Give every drawn muscle an `expect` from its source, then run
   `node tests/sim.test.js`. A failure means the drawing contradicts the paper.

## Adding a region

Add the region to `index.json` with `status: "available"`, its `joints`, its
`groups`, and the `records` files its muscles live in, then write models. The
engine and page need no change. Planned regions: pectoral girdle, forelimb,
pelvic girdle, hindlimb.

## Known limits

- Lateral view only; z is used for length, never drawn.
- Upper-jaw protrusion is a slide of the palatoquadrate complex, not a hinge,
  because a hinge cannot make the preorbitalis protrude it.
- Transverse sheets (intermandibularis, gill constrictors) are chords from a
  lateral point to the midline or between raphes, so their shortening is a
  dorsoventral squeeze or a sling flattening, not a lateral measurement.
- A muscle contracting alone is unopposed; it shows direction of pull, not
  equilibrium.
- Muscles are scored from one source table per animal. Where the dataset has not
  yet filed a muscle for that animal the detail card says so.
