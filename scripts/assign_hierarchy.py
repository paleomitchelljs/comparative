#!/usr/bin/env python3
"""Populate `segment` and `layer` on muscle records (roadmap phase 1).

`segment` is deterministic from `region` — a forearm muscle is a zeugopod muscle
by definition — so it is assigned everywhere.

`layer` is NOT guessed. It is assigned only where the existing `subregion` text
states it outright ("ventral superficial", "deep palmar layer"). Everything else
is reported for manual assignment against a source, because superficial/deep
membership is a claim about developmental layering, not a labelling convenience.

    python3 scripts/assign_hierarchy.py           # report
    python3 scripts/assign_hierarchy.py --write   # apply
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

REGION_SEGMENT = {
    "cranial": "cranial", "axial": "axial", "fin": "fin",
    "pectoral": "girdle", "arm": "stylopod", "forearm": "zeugopod", "hand": "autopod",
    "pelvic": "girdle", "thigh": "stylopod", "leg": "zeugopod", "foot": "autopod",
}

# Matched against `subregion`, lowercased. Order matters: first hit wins.
SUBREGION_LAYER = [
    ("primaxial", "primaxial"),
    ("preaxial", "preaxial"),
    ("postaxial", "postaxial"),
    ("superficial", "superficialis"),
    ("deep", "profundus"),
    ("middle palmar", "intermediate"),
    ("middle plantar", "intermediate"),
]


def main(write: bool) -> int:
    docs, seg_n, lay_n, inherit_n, missing = {}, 0, 0, 0, []
    records = {}

    for path in sorted(ROOT.glob("data/muscles-*.json")):
        doc = json.loads(path.read_text())
        docs[path] = doc
        for m in doc["muscles"]:
            records[m["id"]] = (path, m)
            seg = REGION_SEGMENT.get(m.get("region"))
            if seg and m.get("segment") != seg:
                m["segment"] = seg
                seg_n += 1

            if not m.get("layer"):
                sub = (m.get("subregion") or "").lower()
                hit = next((lay for key, lay in SUBREGION_LAYER if key in sub), None)
                if hit:
                    m["layer"] = hit
                    lay_n += 1

    # Second pass: a muscle named in an ancestral fin muscle's `derivatives`
    # inherits that muscle's layer. This is Diogo et al. (2016)'s own claim —
    # the tetrapod muscle IS a subdivision of that fin layer — so it is sourced
    # rather than inferred, and `layerSource` records where it came from.
    for _, anc in records.values():
        anc_layer = anc.get("layer")
        if anc.get("region") != "fin" or not anc_layer:
            continue
        if anc_layer not in ("superficialis", "profundus"):
            continue          # preaxial/postaxial/primaxial are positions, not layers
        for ids in (anc.get("derivatives") or {}).values():
            for did in ids:
                entry = records.get(did)
                if not entry or entry[1].get("layer"):
                    continue
                entry[1]["layer"] = anc_layer
                entry[1]["layerSource"] = {"from": anc["id"], "sources": ["diogo-etal-2016"]}
                inherit_n += 1

    for path, m in records.values():
        # Cranial muscles are organised by arch, not by layer; absence is correct.
        if not m.get("layer") and m.get("region") != "cranial":
            missing.append(f"{path.name}:{m['id']}  subregion={m.get('subregion')!r}")

    print(f"segment assigned/updated on {seg_n} records")
    print(f"layer read from subregion on {lay_n} records")
    print(f"layer inherited via `derivatives` from a fin ancestor on {inherit_n} records")
    print(f"\n{len(missing)} appendicular records still need `layer` from a source "
          f"(cranial records are excluded — they use `arch`):")
    for line in missing:
        print(f"  {line}")

    if not write:
        print("\nDry run. Re-run with --write to apply.")
        return 0

    # Keep key order stable and readable: insert segment/layer near the top.
    order = ["id", "name", "region", "subregion", "segment", "mass", "layer", "arch",
             "layerSource", "ancestralNode", "developmental", "synonyms", "consensus", "attachments",
             "occurrences", "derivatives", "homology", "sources"]
    for path, doc in docs.items():
        for i, m in enumerate(doc["muscles"]):
            doc["muscles"][i] = {**{k: m[k] for k in order if k in m},
                                 **{k: v for k, v in m.items() if k not in order}}
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"\nrewrote {len(docs)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
