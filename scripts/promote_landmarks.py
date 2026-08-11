#!/usr/bin/env python3
"""Promote landmarks named in prose into the structured attachment rows.

The audit found rows whose own `origin`/`insertion` text names a landmark —
"olecranon", "deltopectoral crest", "fourth trochanter" — while the structured
row records only the parent bone. That is captured information that never made
it into structure, and it is the difference between "attaches to the humerus"
and "attaches to the deltopectoral crest", which is the whole basis of reading a
muscle off a fossil.

Two guards:

* **Relative references are not attachments.** "distal to the deltopectoral
  crest" locates a muscle by a landmark it does NOT attach to. Promoting those
  would invent attachments.
* **Disjunctions are not conjunctions.** "Meckel's cartilage or the dentary"
  describes different taxa, not two attachments in one animal, so it is left for
  hand curation.

    python3 scripts/promote_landmarks.py           # report
    python3 scripts/promote_landmarks.py --write   # apply
"""

import json
import pathlib
import re
import sys

import speciesmap

ROOT = pathlib.Path(__file__).resolve().parent.parent

# A landmark mentioned after one of these is a positional reference, not an
# attachment site.
RELATIVE = r"(?:distal|proximal|anterior|posterior|medial|lateral|dorsal|ventral|deep|superficial|caudal|cranial)\s+to\s+(?:the\s+)?$"
NEAR = r"(?:near|adjacent to|beside|below|above|behind|in front of|toward[s]?)\s+(?:the\s+)?$"
# Phrases that mark alternatives across taxa rather than joint attachment.
DISJUNCTION = r"\b(?:or|either)\b[^.]{0,40}$"

SKIP = {
    # "Meckel's cartilage OR the dentary and adjacent bones" — taxon alternatives.
    ("adductor-mandibulae", "meckels-cartilage"),
    ("adductor-mandibulae", "dentary"),
}


def main(write: bool) -> int:
    skel = json.loads((ROOT / "data/skeleton.json").read_text())
    els = {e["id"]: e for e in skel["elements"]}

    landmarks = {}
    for e in skel["elements"]:
        parent = els.get(e.get("partOf") or "")
        if parent and parent.get("kind") in ("bone", "cartilage"):
            landmarks[e["id"]] = [e["label"].lower()] + [s.lower() for s in e.get("synonyms", [])]

    docs, promoted, skipped = {}, [], []
    for path in sorted(ROOT.glob("data/muscles-*.json")):
        doc = json.loads(path.read_text())
        docs[path] = doc
        for m in doc["muscles"]:
            holders = [(m, "consensus", m.get("consensus") or {})]
            holders += [(o, speciesmap.clade_of(o), o) for o in m.get("occurrences", [])]
            for holder, label, textsrc in holders:
                att = holder.get("attachments")
                if not att:
                    continue
                for side in ("origin", "insertion"):
                    prose = str(textsrc.get(side) or (m.get("consensus") or {}).get(side) or "")
                    low = prose.lower()
                    rows = att.get(side, [])
                    have = {r.get("landmark") for r in rows}
                    for row in list(rows):
                        bone = row.get("element")
                        if row.get("landmark"):
                            continue
                        for lid, phrases in landmarks.items():
                            if els[lid].get("partOf") != bone or lid in have:
                                continue
                            if (m["id"], lid) in SKIP:
                                continue
                            for ph in phrases:
                                for hit in re.finditer(re.escape(ph), low):
                                    before = low[:hit.start()]
                                    if re.search(RELATIVE, before) or re.search(NEAR, before):
                                        skipped.append((m["id"], label, lid, "relative reference"))
                                        break
                                    if re.search(DISJUNCTION, before):
                                        skipped.append((m["id"], label, lid, "disjunction"))
                                        break
                                    row["landmark"] = lid
                                    have.add(lid)
                                    promoted.append((m["id"], label, side, bone, lid))
                                    break
                                if row.get("landmark"):
                                    break
                            if row.get("landmark"):
                                break

    print(f"{len(promoted)} landmarks promoted into structured rows:")
    for mid, label, side, bone, lid in promoted:
        print(f"    {mid:36} {label:12} {side:9} {bone} -> {lid}")
    if skipped:
        print(f"\n{len(skipped)} left alone:")
        for mid, label, lid, why in skipped:
            print(f"    {mid:36} {label:12} {lid:24} {why}")

    if not write:
        print("\nDry run. Re-run with --write to apply.")
        return 0

    for path, doc in docs.items():
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"\nrewrote {len(docs)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
