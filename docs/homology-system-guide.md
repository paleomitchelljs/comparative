# The homology correspondence system

How one muscle record states its relationship to another. Field definitions are in
[`SCHEMA.md`](SCHEMA.md); this describes what the relations mean and how to read
them.

---

## What the problem is

A muscle record is a homology group, not a muscle in one animal. In any given
taxon that group may be one muscle or several, and **several is the common case**:
450 of the 1480 occurrence rows carry `parts`, and one carries fifteen. A record
whose name is singular routinely stands for four named muscles in a rat.

`parts` says how a group subdivides **inside** one record. `homology.correspondences`
says how a record relates to **another** record. The two never overlap: if the
muscles are within one homology group it is a division, and if they are in two
groups it is a correspondence.

## The four relations

| relation | Means | Direction |
|---|---|---|
| `serial` | Same series, different segment. `axis` says which series | Symmetric |
| `no-counterpart` | Asserted absence on that axis. No `to` | — |
| `descends-from` | Ancestor → descendant through evolutionary time | Directed, stored on the descendant |
| `corresponds-to-part-of` | This record, or a named part of it, is part of that one | Directed |

### `serial`

Two records occupy the same position in a repeated series. `axis` names the
series:

- **`forelimb-hindlimb`** — the pectoral and pelvic counterparts of one animal.
- **`pharyngeal-arch`** — the constrictor series along the arches. The
  intermandibularis is the arch-1 ventral constrictor, the interhyoideus the
  arch-2, and the branchial constrictors arches 3–7. All three are linked to each
  other.

`basis` qualifies the claim: `topological` asserts only corresponding position,
`developmental` is reserved for correspondences that survive knowing the anlagen.
Diogo & Molnar (2014) reject forelimb–hindlimb serial homology in the strict
ancestral-duplication sense, so `topological` is the default and the burden is on
`developmental`.

**Serial is not genealogical.** Arch 2 is not descended from arch 3, and a
hindlimb muscle is not descended from its forelimb counterpart. If what you mean
is descent, the relation is `descends-from`.

The graph is undirected. Record the edge once and run
`scripts/symmetrise_links.py --write`; the reverse edge carries the axis, basis,
sources and confidence, but not the note, because a note argues one direction.

### `no-counterpart`

An assertion that the series has no member here — the same distinction `present:
"no"` draws against an unrecorded row. The caudofemoralis carries one on the
forelimb–hindlimb axis, and its note calls it a clean falsification of any
expectation of one-to-one fore/hindlimb correspondence.

**Omitting the relation means unrecorded, not absent.**

### `descends-from`

Ancestor to descendant through evolutionary time, and the only relation with a
time direction. It is **stored on the descendant**, pointing back, which is what
lets one muscle name several ancestors — `ischioflexorius` names three. The
forward view, what an ancestral fin muscle gave rise to, is reconstructed by
scanning rather than stored, so the two directions cannot drift apart.

`girdle` is `pectoral` or `pelvic`, because the ancestral paired-fin muscles are
ancestral to both.

### `corresponds-to-part-of`

Partial correspondence: this record, or a named part of it, is part of that one.
It covers both subdivision and partial identity, because those are the same
relation read from opposite ends.

`fromPart` names a part of this record; `toPart` names a part of the target. Both
must be part names that appear on some occurrence of the record that owns them.

## Reading a group

**There is no group object.** One muscle corresponding to a group of others is
several edges sharing a `to`; the inverse is several records naming the same
target. A stored group would need its own identity and would go stale the moment a
record split, so the group is always computed.

To ask *what does this record correspond to*, read its own `correspondences`. To
ask *what corresponds to this record*, scan for edges naming it. The app does both.

## Contested parts

When two records both claim a muscle, the part carries `membership: "disputed"`
and `claimedBy`, naming the other record:

```jsonc
{ "name": "Tensor tympani", "membership": "disputed",
  "claimedBy": "adductor-mandibulae" }
```

`validate.py` requires that one of the two records also carry a
`corresponds-to-part-of` edge between them, so a dispute cannot be asserted from
one side only. Two live cases: the gemelli, claimed by
`puboischiofemoralis-externus` and `ischiotrochantericus`; and the tensor tympani
and tensor veli palatini, claimed by `intermandibularis` and
`adductor-mandibulae`.

## `related` is a different question

`related` sits alongside all of this and means **topologically or developmentally
adjacent** — untyped, undirected, and carrying no claim. It is the largest graph
here, 386 edges across 128 of the 129 records, and it answers "what is next to
this" rather than "what is this the same as".

If you can name the relation and cite a source for it, it is a correspondence. If
you are recording that two muscles sit beside one another, it is `related`.

## Adding one

1. Decide which of the four relations it is. If none fits, it is probably
   `related`, or a division fact belonging in `parts`.
2. `to` must be a different record. A part that subdivides differently between two
   taxa of **one** record is a division fact — put it in `parts` and
   `divisionNote`.
3. Give it `sources` and `confidence`. A correspondence is a homology claim, so it
   ages, and it feeds `homology.authority` through
   `seed_homology_authority.py`. Ninety-four legacy edges carry neither and
   `validate.py` reports that count once; do not add to it.
4. Scope it with `taxa` where the claim is clade-limited, which most are. The
   values are operational taxa from `taxa.json` — `theria`, `monotremata`, not
   `mammalia`.
5. Run `./scripts/build.sh --write`. It closes the serial graph, checks every
   reference and part name, and errors if a `claimedBy` is one-sided.
