#!/usr/bin/env python3
"""Skeletal elements needed to score Walthall & Ashley-Ross (2006) attachments.

The Taricha description names attachment sites the ontology could not yet
resolve: the ypsiloid cartilage, the primitive tetrapod carpals and tarsals that
fuse or vanish in most amniotes, and transverse processes on trunk and caudal
vertebrae (the ontology had them only for the cervicals).

Two judgement calls are recorded here rather than buried:

* **The pubo-ischiac plate is not given its own element.** It is a fusion of the
  pubis and ischium, and the paper itself glosses it that way — the ischium is
  "the posterior portion of the pubo-ischiac plate". Giving it a row would put
  the salamander's puboischiofemoralis on a different bone from every other
  tetrapod's, which is the hyomandibula/stapes mistake. Attachments are scored on
  `pubis` and `ischium`, with the plate named in the occurrence note.

* **Carpal and tarsal intermedium are separate records.** They correspond
  serially, but a serial correspondence is not an identity — the same reason
  `radiale`/`tibiale` and `ulnare`/`fibulare` are already separate.

    python3 scripts/seed_walthall_skeleton.py           # report
    python3 scripts/seed_walthall_skeleton.py --write   # apply
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = "walthall-ashley-ross-2006"

NEW = [
    {
        "id": "ypsiloid-cartilage",
        "label": "Ypsiloid cartilage",
        "kind": "cartilage",
        "region": "pelvic",
        "segment": "girdle",
        "partOf": "pelvic-girdle",
        "presence": {
            "default": "no",
            "present": ["caudata"],
            "note": "Y-shaped cartilage projecting forward from the anterior margin of "
                    "the pubis. Anchors the anterior continuation of the rectus abdominis "
                    "and receives the m. ypsiloideus.",
            "sources": [SRC],
        },
    },
    {
        "id": "thoracic-transverse-processes",
        "label": "Transverse processes (trunk)",
        "kind": "bone",
        "region": "axial",
        "segment": "axial",
        "partOf": "thoracic-vertebrae",
        "presence": {"default": "yes"},
    },
    {
        "id": "caudal-transverse-processes",
        "label": "Transverse processes (caudal)",
        "kind": "bone",
        "region": "axial",
        "segment": "axial",
        "partOf": "caudal-vertebrae",
        "correlate": True,
        "presence": {
            "default": "yes",
            "note": "Origin of the caudofemoralis and of the tail-to-girdle muscles. In "
                    "Taricha the caudofemoralis takes the fourth and fifth caudal "
                    "transverse processes — a countable segmental address, which makes "
                    "this one of the few attachment sites that can be scored by position "
                    "along the column rather than by bone alone.",
            "sources": [SRC],
        },
    },
    {
        "id": "intermedium-manus",
        "label": "Intermedium (carpal)",
        "kind": "bone",
        "region": "forelimb",
        "segment": "autopod",
        "partOf": "carpals",
        "presence": {
            "default": "variable",
            "present": ["caudata"],
            "note": "Proximal carpal between radiale and ulnare, retained in salamanders "
                    "and reduced or fused in most amniotes. Serially corresponds to the "
                    "tarsal intermedium but is a separate element.",
            "sources": [SRC],
        },
    },
    {
        "id": "intermedium-pes",
        "label": "Intermedium (tarsal)",
        "kind": "bone",
        "region": "hindlimb",
        "segment": "autopod",
        "partOf": "tarsals",
        "presence": {
            "default": "variable",
            "present": ["caudata"],
            "note": "Proximal tarsal between tibiale and fibulare. Serial counterpart of "
                    "the carpal intermedium; separate element for the same reason "
                    "radiale and tibiale are separate.",
            "sources": [SRC],
        },
    },
    {
        "id": "centrale-pes",
        "label": "Centrale (tarsal)",
        "kind": "bone",
        "region": "hindlimb",
        "segment": "autopod",
        "partOf": "tarsals",
        "presence": {
            "default": "variable",
            "present": ["caudata"],
            "note": "Central tarsal of the primitive tetrapod ankle, retained in "
                    "salamanders.",
            "sources": [SRC],
        },
    },
    {
        "id": "distal-tarsals",
        "label": "Distal tarsals",
        "kind": "bone",
        "region": "hindlimb",
        "segment": "autopod",
        "partOf": "tarsals",
        "presence": {
            "default": "yes",
            "absent": ["chondrichthyes", "actinopterygii", "actinistia", "dipnoi"],
            "note": "Distal tarsal row. Origin of the intrinsic pedal muscles — the "
                    "serial counterpart of the distal carpal row in the manus.",
            "sources": [SRC],
        },
    },
    {
        "id": "linea-alba",
        "label": "Linea alba",
        "kind": "aponeurosis",
        "region": "axial",
        "segment": "axial",
        "presence": {
            "default": "yes",
            "note": "Midline aponeurosis separating the left and right rectus abdominis "
                    "and receiving the oblique and transverse layers of the body wall. A "
                    "soft-tissue attachment site that leaves no osteological trace.",
            "sources": [SRC],
        },
    },
]

# Element-level synonyms and taxon-specific names this paper supplies.
SYNONYMS = {
    "deltopectoral-crest": ["crista ventralis (Caudata)"],
}
TAXON_NAMES = {
    "deltopectoral-crest": [{"taxa": ["caudata"], "name": "Crista ventralis"}],
}


def main(write: bool) -> int:
    path = ROOT / "data/skeleton.json"
    doc = json.loads(path.read_text())
    have = {e["id"] for e in doc["elements"]}
    by_id = {e["id"]: e for e in doc["elements"]}

    added, skipped, touched = [], [], []
    for e in NEW:
        if e["id"] in have:
            skipped.append(e["id"])
            continue
        doc["elements"].append(e)
        added.append(e["id"])

    for eid, syns in SYNONYMS.items():
        el = by_id.get(eid)
        if not el:
            continue
        cur = el.setdefault("synonyms", [])
        for s in syns:
            if s not in cur:
                cur.append(s)
                touched.append(f"{eid} += synonym {s!r}")

    for eid, names in TAXON_NAMES.items():
        el = by_id.get(eid)
        if not el:
            continue
        cur = el.setdefault("taxonNames", [])
        claimed = {t for tn in cur for t in tn.get("taxa", [])}
        for tn in names:
            if not set(tn["taxa"]) & claimed:
                cur.append(tn)
                touched.append(f"{eid} += taxonName {tn['name']!r} for {tn['taxa']}")

    print(f"{len(added)} elements added:")
    for i in added:
        print(f"    {i}")
    if skipped:
        print(f"{len(skipped)} already present: {', '.join(skipped)}")
    for t in touched:
        print(f"    {t}")

    if not write:
        print("\nDry run. Re-run with --write to apply.")
        return 0
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"\nwrote {path} ({len(doc['elements'])} elements)")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
