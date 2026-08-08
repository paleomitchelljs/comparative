#!/usr/bin/env python3
"""Restructure `attachments` from flat id lists into element/side/landmark rows.

Before:
    "insertion": ["deltopectoral-crest"]

After:
    "insertion": [
      { "element": "humerus", "side": "anterior", "landmark": "deltopectoral-crest" }
    ]

A muscle attaching to several sides or landmarks of one bone gets several rows,
which the flat list could not express. Where the old value was already a
landmark (an element with a `partOf` bone), it is lifted so the bone is named
explicitly and the landmark sits under it — that is what makes the bone-first
drill-down work at every level of resolution.

`side` is left null unless SIDES below records it from a source. A null side
means unrecorded, not "no side".

    python3 scripts/migrate_attachment_rows.py           # report
    python3 scripts/migrate_attachment_rows.py --write   # apply
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# (element, landmark or None) -> side. Only well-documented positions; anything
# absent stays null rather than being invented.
SIDES = {
    ("humerus", "deltopectoral-crest"): "anterior",
    ("humerus", "greater-tubercle"): "proximal",
    ("humerus", "lesser-tubercle"): "proximal",
    ("humerus", "lateral-epicondyle"): "distal",
    ("humerus", "medial-epicondyle"): "distal",
    ("humerus", "supracondylar-ridge"): "distal",
    ("ulna", "olecranon"): "proximal",
    ("ulna", "coronoid-process-ulna"): "proximal",
    ("ulna", "supinator-crest"): "proximal",
    ("radius", "radial-tuberosity"): "proximal",
    ("scapula", "supraspinous-fossa"): "lateral",
    ("scapula", "infraspinous-fossa"): "lateral",
    ("scapula", "subscapular-fossa"): "medial",
    ("scapula", "scapular-spine"): "lateral",
    ("scapula", "acromion"): "distal",
    ("scapula", "coracoid-process"): "anterior",
    ("femur", "greater-trochanter"): "proximal",
    ("femur", "lesser-trochanter"): "proximal",
    ("femur", "fourth-trochanter"): "posterior",
    ("femur", "trochanteric-fossa"): "proximal",
    ("femur", "linea-aspera"): "posterior",
    ("femur", "femoral-condyles"): "distal",
    ("tibia", "tibial-tuberosity"): "proximal",
    ("ilium", "iliac-crest"): "dorsal",
    ("ischium", "ischial-tuberosity"): "posterior",
    ("sternum", "sternal-keel"): "ventral",
    ("mandible", "coronoid-process-mandible"): "dorsal",
    ("mandible", "retroarticular-process"): "posterior",
    ("tarsals", "calcaneum"): "posterior",
    ("carpals", "pisiform"): "medial",
    ("carpals", "ulnare"): "lateral",
    # Whole-bone attachments with a documented aspect.
    ("scapula", None): "lateral",
    ("coracoid", None): "ventral",
    ("suprascapula", None): "dorsal",
}


def main(write: bool) -> int:
    skel = json.loads((ROOT / "data/skeleton.json").read_text())
    by_id = {e["id"]: e for e in skel["elements"]}

    def lift(ref):
        """Return (element, landmark) for a raw id.

        A subsite is promoted so its parent BONE is named and the subsite sits
        under it: deltopectoral-crest -> (humerus, deltopectoral-crest). Only a
        parent that is itself a bone or cartilage counts. A bone whose parent is
        a grouping ("scapula" within "pectoral-girdle", "pisiform" within
        "carpals") is a bone in its own right and stays as the element."""
        e = by_id.get(ref)
        if not e:
            return ref, None
        parent = by_id.get(e.get("partOf") or "")
        if parent and parent.get("kind") in ("bone", "cartilage"):
            return parent["id"], ref
        return ref, None

    def convert(lst):
        rows, seen = [], set()
        for ref in lst or []:
            if isinstance(ref, dict):        # already migrated
                rows.append(ref)
                continue
            element, landmark = lift(ref)
            key = (element, landmark)
            if key in seen:
                continue
            seen.add(key)
            row = {"element": element}
            side = SIDES.get((element, landmark)) or SIDES.get((element, None))
            if side:
                row["side"] = side
            if landmark:
                row["landmark"] = landmark
            rows.append(row)
        return rows

    docs, n_rows, n_landmarks, n_sides = {}, 0, 0, 0
    for path in sorted(ROOT.glob("data/muscles-*.json")):
        doc = json.loads(path.read_text())
        docs[path] = doc
        for m in doc["muscles"]:
            for holder in [m] + list(m.get("occurrences", [])):
                att = holder.get("attachments")
                if not att:
                    continue
                for side_key in ("origin", "insertion"):
                    if side_key not in att:
                        continue
                    rows = convert(att[side_key])
                    att[side_key] = rows
                    n_rows += len(rows)
                    n_landmarks += sum(1 for r in rows if r.get("landmark"))
                    n_sides += sum(1 for r in rows if r.get("side"))

    print(f"{n_rows} attachment rows "
          f"({n_landmarks} carry a landmark, {n_sides} carry a side)")

    if not write:
        print("\nDry run. Re-run with --write to apply.")
        return 0

    for path, doc in docs.items():
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"rewrote {len(docs)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
