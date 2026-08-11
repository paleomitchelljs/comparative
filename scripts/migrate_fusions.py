#!/usr/bin/env python3
"""Record fused skeletal elements as fusions rather than as containment.

    python3 scripts/migrate_fusions.py           # report
    python3 scripts/migrate_fusions.py --write   # apply

`docs/METHODS.md` says a fused element is scored as its components. The
salamander pubo-ischiac plate follows that, because Walthall & Ashley-Ross gloss
the plate as pubis plus ischium and the muscles can be assigned to each. Three
avian elements did not follow it: the tibiotarsus, tarsometatarsus and pygostyle
each had a record of their own, hung off a component with `partOf`.

`partOf` means containment, and the attachment diff reads it that way. A bird
inserting on the tarsometatarsus, compared against a crocodylian inserting on
the metatarsals, therefore reported as a REFINEMENT — the same category as
humerus to greater tubercle, i.e. one author being more precise than another.
It is nothing of the kind: it is the same attachment on an element that has
absorbed its neighbours. Worse, the fusion event itself was nowhere in the data.
Birds carried both `tibia` (present) and `tibiotarsus` (present), with no
statement that the first is inside the second.

So `fusedFrom` — the inverse of `derivedFrom`, and directed the same way through
time. Deleting these three records and decomposing the attachments was the other
option and is worse: Hattori & Tsuihiji record attachments ON the tarsometatarsus,
and splitting those across distal tarsals and metatarsals would assert which
component a muscle reaches when the source does not say.

The rule the two cases share, stated properly: never let a fusion break the
homology of what fused. Score components where the source decomposes the
compound; record the compound with `fusedFrom` where the source treats it as the
unit of observation. Either way the components stay findable.
"""

import json
import pathlib
import sys

import speciesmap

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKELETON = ROOT / "data" / "skeleton.json"
MUSCLE_FILES = sorted(ROOT.glob("data/muscles-*.json"))

# element id -> (components, note). The components are the elements that lost
# their independence, not everything nearby: metatarsal I stays free in birds
# and is not claimed here.
FUSIONS = {
    "tibiotarsus": (
        ["tibia", "astragalus", "calcaneum"],
        "Tibia fused with the proximal tarsals (astragalus and calcaneum)."),
    "tarsometatarsus": (
        ["distal-tarsals", "metatarsals"],
        "Distal tarsals fused with metatarsals II-IV. Metatarsal I remains "
        "free, so the metatarsal series is not wholly absorbed."),
    # One element series coalescing rather than distinct elements merging. The
    # single-component form says exactly that.
    "pygostyle": (
        ["caudal-vertebrae"],
        "The distal caudal vertebrae fused into a single plate."),
}


def main():
    write = "--write" in sys.argv
    doc = json.loads(SKELETON.read_text())
    by_id = {e["id"]: e for e in doc["elements"]}

    problems = []
    for eid, (components, _) in FUSIONS.items():
        if eid not in by_id:
            problems.append(f"{eid}: no such element")
        for c in components:
            if c not in by_id:
                problems.append(f"{eid}: component '{c}' is not an element")

    if problems:
        for p in problems:
            print(f"  ERROR {p}")
        return 1

    changed = []
    for eid, (components, note) in FUSIONS.items():
        e = by_id[eid]
        want_parent = e.pop("partOf", None) if write else e.get("partOf")
        already = e.get("fusedFrom") == components
        if already and not want_parent:
            continue
        changed.append(f"{eid}: fusedFrom {components}"
                       + (f", dropping partOf '{want_parent}'" if want_parent else ""))
        if write:
            e["fusedFrom"] = components
            # Say it once. The element's presence block already carries the
            # taxa, and the existing note already carries the anatomy; this
            # only adds what `partOf` used to imply and no longer does.
            if not e.get("transformation"):
                e["transformation"] = note

    for line in changed:
        print(f"  {line}")

    # A compound was reachable as a `landmark` while it hung off a component by
    # `partOf` — tibialis anterior in Aves inserted on
    # {element: metatarsals, landmark: tarsometatarsus}. That row said the bird
    # attaches to a named spot on the metatarsal series. It attaches to the
    # tarsometatarsus, which is a bone in its own right; promote it to
    # `element` and drop the component it was filed under.
    moved = []
    muscle_docs = {path: json.loads(path.read_text()) for path in MUSCLE_FILES}
    for path, mdoc in muscle_docs.items():
        for m in mdoc["muscles"]:
            holders = [("consensus", m)] + [
                (speciesmap.clade_of(o), o) for o in m.get("occurrences", [])]
            for tag, holder in holders:
                att = holder.get("attachments") or {}
                for side_key in ("origin", "insertion"):
                    for row in att.get(side_key, []):
                        lm = row.get("landmark")
                        if lm not in FUSIONS:
                            continue
                        moved.append(
                            f"{m['id']}/{tag} {side_key}: "
                            f"{row.get('element')} > {lm}  ->  element {lm}")
                        if write:
                            row["element"] = lm
                            row.pop("landmark", None)

    for line in moved:
        print(f"  MOVED {line}")

    if write and (changed or moved):
        if changed:
            SKELETON.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
            print(f"\nwrote {SKELETON.relative_to(ROOT)}")
        if moved:
            for path, mdoc in muscle_docs.items():
                path.write_text(json.dumps(mdoc, indent=2, ensure_ascii=False) + "\n")
            print(f"rewrote {len(moved)} attachment row(s)")
    elif not changed and not moved:
        print("  all three fusions already recorded, no attachment rows to move")
    else:
        print("\n(dry run — pass --write to apply)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
