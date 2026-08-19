#!/usr/bin/env python3
"""Make the undirected homology links symmetric across the muscle files.

The related-muscle graph is conceptually undirected: if the latissimus dorsi is
adjacent to the subcoracoscapularis, the reverse holds too. Curating both
directions by hand is error-prone, so record the link once in whichever file is
convenient and run this to close the graph.

Two graphs are closed here and they are not the same graph. `homology.related` is
untyped adjacency. `homology.correspondences` with `relation: "serial"` is a
homology claim on a stated axis, and only that relation is symmetric — a
`descends-from` edge reversed says the descendant is the ancestor, and a
`corresponds-to-part-of` edge reversed says the whole is the part. Those two are
left strictly alone.

    python3 scripts/symmetrise_links.py          # report what would change
    python3 scripts/symmetrise_links.py --write  # apply
"""

import json
import pathlib
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = sorted(ROOT.glob("data/muscles-*.json"))


def main(write: bool) -> int:
    docs = {path: json.loads(path.read_text()) for path in FILES}

    # muscle id -> (path, record)
    index = {}
    for path, doc in docs.items():
        for m in doc["muscles"]:
            index[m["id"]] = (path, m)

    missing = defaultdict(set)
    for mid, (_, m) in index.items():
        for ref in m.get("homology", {}).get("related", []):
            if ref not in index:
                print(f"  skip  {mid} -> {ref} (unknown muscle)")
                continue
            back = index[ref][1].setdefault("homology", {}).get("related", [])
            if mid not in back:
                missing[ref].add(mid)

    # serial correspondences: (target, axis) -> {(source, basis)}
    ser_missing = defaultdict(set)
    for mid, (_, m) in index.items():
        for e in (m.get("homology", {}).get("correspondences") or []):
            if e.get("relation") != "serial":
                continue
            ref, axis = e.get("to"), e.get("axis")
            if ref not in index:
                print(f"  skip  {mid} =={axis}=> {ref} (unknown muscle)")
                continue
            back = [b for b in (index[ref][1].get("homology", {}).get("correspondences") or [])
                    if b.get("relation") == "serial" and b.get("to") == mid
                    and b.get("axis") == axis]
            if not back:
                ser_missing[(ref, axis)].add((mid, e.get("basis"),
                                              tuple(e.get("sources") or ()),
                                              e.get("confidence")))

    if not missing and not ser_missing:
        print("related and serial graphs are already symmetric")
        return 0

    total = sum(len(v) for v in missing.values()) + sum(len(v) for v in ser_missing.values())
    for target, adds in sorted(missing.items()):
        for add in sorted(adds):
            print(f"  {'add ' if write else 'would add'}  related  {target} -> {add}")
    for (target, axis), adds in sorted(ser_missing.items()):
        for add, *_ in sorted(adds):
            print(f"  {'add ' if write else 'would add'}  serial   {target} =={axis}=> {add}")

    if not write:
        print(f"\n{total} back-links missing. Re-run with --write to add them.")
        return 0

    for target, adds in missing.items():
        rel = index[target][1].setdefault("homology", {}).setdefault("related", [])
        rel.extend(sorted(adds))
        rel.sort()

    # The reverse of a serial edge carries the axis, the basis, and the source
    # and confidence of the forward edge — the claim is symmetric, so whatever
    # supports it supports it both ways. The `note` does not come across: a note
    # argues one direction and does not survive being turned round.
    for (target, axis), adds in ser_missing.items():
        cs = index[target][1].setdefault("homology", {}).setdefault("correspondences", [])
        for src, basis, sources, conf in sorted(adds):
            e = {"relation": "serial", "to": src, "axis": axis}
            if basis:
                e["basis"] = basis
            if sources:
                e["sources"] = list(sources)
            if conf:
                e["confidence"] = conf
            cs.append(e)
        cs.sort(key=lambda e: (e["relation"], e.get("to") or "",
                               e.get("fromPart") or e.get("toPart") or ""))

    for path, doc in docs.items():
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")

    print(f"\nadded {total} back-links across {len(FILES)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
