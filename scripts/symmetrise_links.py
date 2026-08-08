#!/usr/bin/env python3
"""Make `homology.related` symmetric across the muscle files.

The related-muscle graph is conceptually undirected: if the latissimus dorsi is
adjacent to the subcoracoscapularis, the reverse holds too. Curating both
directions by hand is error-prone, so record the link once in whichever file is
convenient and run this to close the graph.

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

    if not missing:
        print("related graph is already symmetric")
        return 0

    total = sum(len(v) for v in missing.values())
    for target, adds in sorted(missing.items()):
        for add in sorted(adds):
            print(f"  {'add ' if write else 'would add'}  {target} -> {add}")

    if not write:
        print(f"\n{total} back-links missing. Re-run with --write to add them.")
        return 0

    for target, adds in missing.items():
        rel = index[target][1].setdefault("homology", {}).setdefault("related", [])
        rel.extend(sorted(adds))
        rel.sort()

    for path, doc in docs.items():
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")

    print(f"\nadded {total} back-links across {len(FILES)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
