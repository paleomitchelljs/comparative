#!/usr/bin/env python3
"""Merge homologous skeletal elements and restructure the axial series.

Two problems this fixes.

**Elements split by name.** `hyomandibula` and `stapes` were separate entries
with perfectly complementary presence — fish and tetrapods — which is the
signature of one element recorded under two names. Same for palatoquadrate and
quadrate. That is exactly the mistake the muscle records exist to avoid: a
record should be a homology group, with names as per-taxon attributes. Elements
now carry `taxonNames` for the same reason muscle occurrences do.

**The axial series mixed levels.** `sacrum`, `lumbar-vertebrae` and
`caudal-vertebrae` (whole vertebrae) sat alongside `thoracic-neural-spines` and
`cervical-transverse-processes` (parts of vertebrae), all as direct children of
`axial-skeleton`. Now: vertebral column -> regional series -> parts of those
vertebrae.

    python3 scripts/fix_skeleton_homology.py           # report
    python3 scripts/fix_skeleton_homology.py --write   # apply
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# old id -> surviving id. Every reference in data/muscles-*.json is rewritten.
MERGE = {
    "hyomandibula": "hyomandibula-stapes",
    "stapes": "hyomandibula-stapes",
    "palatoquadrate": "palatoquadrate-quadrate",
    "quadrate": "palatoquadrate-quadrate",
    "sacrum": "sacral-vertebrae",
}

# Elements added or rewritten wholesale.
REWRITE = {
    "hyomandibula-stapes": {
        "id": "hyomandibula-stapes", "label": "Hyomandibula / stapes", "kind": "bone",
        "region": "cranial", "segment": "cranial", "correlate": True,
        "synonyms": ["columella auris", "stapes", "hyomandibula"],
        "taxonNames": [
            {"taxa": ["chondrichthyes", "actinopterygii", "actinistia", "dipnoi",
                      "tetrapodomorpha-stem"], "name": "Hyomandibula"},
            {"taxa": ["caudata", "anura", "testudines", "lepidosauria", "crocodylia", "aves"],
             "name": "Columella (stapes)"},
            {"taxa": ["synapsida-stem", "monotremata", "theria"], "name": "Stapes"}],
        "transformation": "One element throughout. The hyomandibula braces the jaw joint against "
            "the braincase in fishes; with the tetrapod jaw suspension it is freed and becomes the "
            "sound-conducting columella, and the stapes of mammals. The muscle acting on it followed "
            "it the whole way — the depressor hyomandibulae of a shark is the stapedius of a mammal, "
            "still on the facial nerve.",
        "presence": {"default": "yes", "absent": ["myxini", "petromyzontida"],
                     "sources": ["ziermann-etal-2014", "ziermann-diogo-2019"]}},

    "palatoquadrate-quadrate": {
        "id": "palatoquadrate-quadrate", "label": "Palatoquadrate / quadrate", "kind": "bone",
        "region": "cranial", "segment": "cranial", "correlate": True,
        "synonyms": ["quadrate", "palatoquadrate", "incus"],
        "taxonNames": [
            {"taxa": ["chondrichthyes", "actinopterygii", "actinistia", "dipnoi"],
             "name": "Palatoquadrate"},
            {"taxa": ["caudata", "anura", "testudines", "lepidosauria", "crocodylia", "aves",
                      "synapsida-stem"], "name": "Quadrate"},
            {"taxa": ["monotremata", "theria"], "name": "Incus"}],
        "transformation": "The upper jaw cartilage of the first pharyngeal arch. Its posterior end "
            "ossifies as the quadrate and carries the jaw joint in non-mammals; in mammals it leaves "
            "the jaw entirely and becomes the incus, which is why the mammalian jaw joint is "
            "squamosal-dentary instead of quadrate-articular.",
        "presence": {"default": "yes", "absent": ["myxini", "petromyzontida"],
                     "sources": ["ziermann-etal-2014", "ziermann-diogo-2019"]}},

    "articular": {
        "id": "articular", "label": "Articular / malleus", "kind": "bone",
        "region": "cranial", "segment": "cranial", "partOf": "meckels-cartilage", "correlate": True,
        "synonyms": ["malleus"],
        "taxonNames": [
            {"taxa": ["chondrichthyes", "actinopterygii", "actinistia", "dipnoi", "caudata",
                      "anura", "testudines", "lepidosauria", "crocodylia", "aves", "synapsida-stem"],
             "name": "Articular"},
            {"taxa": ["monotremata", "theria"], "name": "Malleus"}],
        "transformation": "The ossified posterior end of Meckel's cartilage. It meets the quadrate "
            "at the jaw joint in non-mammals and becomes the malleus in mammals — the partner of the "
            "quadrate/incus, moving into the ear together with it.",
        "presence": {"default": "yes", "absent": ["myxini", "petromyzontida"],
                     "sources": ["ziermann-diogo-2019"]}},

    "meckels-cartilage": {
        "id": "meckels-cartilage", "label": "Meckel's cartilage", "kind": "cartilage",
        "region": "cranial", "segment": "cranial", "partOf": "mandible",
        "transformation": "The endoskeletal core of the lower jaw, present in every jawed vertebrate. "
            "In chondrichthyans it IS the lower jaw; in bony fishes and tetrapods a series of dermal "
            "bones ensheaths it, and it persists inside them.",
        "presence": {"default": "yes", "absent": ["myxini", "petromyzontida"],
                     "sources": ["ziermann-etal-2014"]}},

    "angular": {
        "id": "angular", "label": "Angular / ectotympanic", "kind": "bone",
        "region": "cranial", "segment": "cranial", "partOf": "mandible", "correlate": True,
        "synonyms": ["ectotympanic", "tympanic ring"],
        "taxonNames": [
            {"taxa": ["actinopterygii", "actinistia", "dipnoi", "caudata", "anura", "testudines",
                      "lepidosauria", "crocodylia", "aves", "synapsida-stem"], "name": "Angular"},
            {"taxa": ["monotremata", "theria"], "name": "Ectotympanic"}],
        "transformation": "A postdentary dermal bone that becomes the ring supporting the mammalian "
            "tympanic membrane.",
        "presence": {"default": "yes", "absent": ["myxini", "petromyzontida", "chondrichthyes"],
                     "sources": ["ziermann-diogo-2019"]}},
}

# Elements whose parent or presence changes without a merge.
REPARENT = {
    "surangular": "mandible", "coronoid": "mandible", "dentary": "mandible",
    "scapula": "pectoral-girdle", "coracoid": "pectoral-girdle",
}

# Fission: these elements come from a single ancestral element.
DERIVED_FROM = {
    "scapula": "scapulocoracoid",
    "coracoid": "scapulocoracoid",
}

AXIAL = [
    {"id": "vertebral-column", "label": "Vertebral column", "kind": "group",
     "region": "axial", "segment": "axial", "partOf": "axial-skeleton",
     "presence": {"default": "yes"}},
    {"id": "cervical-vertebrae", "label": "Cervical vertebrae", "kind": "bone",
     "region": "axial", "segment": "axial", "partOf": "vertebral-column",
     "presence": {"default": "yes", "absent": ["chondrichthyes", "actinopterygii",
                                               "actinistia", "dipnoi"],
                  "note": "A distinct cervical series requires the girdle to be freed from the skull, "
                          "which happens with the loss of the cleithrum along the tetrapod stem."}},
    {"id": "atlas", "label": "Atlas", "kind": "bone", "region": "axial", "segment": "axial",
     "partOf": "cervical-vertebrae", "correlate": True, "presence": {"default": "yes",
     "absent": ["chondrichthyes", "actinopterygii", "actinistia", "dipnoi"]}},
    {"id": "thoracic-vertebrae", "label": "Thoracic vertebrae", "kind": "bone",
     "region": "axial", "segment": "axial", "partOf": "vertebral-column",
     "presence": {"default": "yes"}},
    {"id": "lumbar-vertebrae", "label": "Lumbar vertebrae", "kind": "bone",
     "region": "axial", "segment": "axial", "partOf": "vertebral-column",
     "presence": {"default": "yes", "absent": ["chondrichthyes", "actinopterygii",
                                               "actinistia", "dipnoi", "aves"]}},
    {"id": "sacral-vertebrae", "label": "Sacral vertebrae", "kind": "bone",
     "region": "axial", "segment": "axial", "partOf": "vertebral-column", "correlate": True,
     "presence": {"default": "yes", "absent": ["chondrichthyes", "actinopterygii",
                                               "actinistia", "dipnoi"],
                  "note": "The sacrum is a tetrapod novelty: fishes have no vertebrae fused to a "
                          "pelvic girdle, because the pelvic fin girdle floats free of the axial "
                          "skeleton. Fusing them is what lets a hindlimb transmit thrust to the body.",
                  "sources": ["diogo-molnar-2014"]}},
    {"id": "caudal-vertebrae", "label": "Caudal vertebrae", "kind": "bone",
     "region": "axial", "segment": "axial", "partOf": "vertebral-column",
     "presence": {"default": "yes", "reduced": ["aves"], "absent": ["anura"],
                  "note": "Replaced by the urostyle in anurans and shortened to the pygostyle in "
                          "birds — both associated with caudofemoralis reduction."}},
]

# Vertebral PARTS, now hanging off the right regional series rather than off
# axial-skeleton directly.
PARTS = [
    ("thoracic-neural-spines", "Neural spines (thoracic)", "thoracic-vertebrae"),
    ("cervical-transverse-processes", "Transverse processes (cervical)", "cervical-vertebrae"),
    ("atlas-transverse-process", "Transverse process of atlas", "atlas"),
]


def main(write: bool) -> int:
    skel_path = ROOT / "data/skeleton.json"
    skel = json.loads(skel_path.read_text())
    by_id = {e["id"]: e for e in skel["elements"]}

    # 1. drop merged-away ids, then apply rewrites
    survivors = [e for e in skel["elements"]
                 if not (e["id"] in MERGE and MERGE[e["id"]] != e["id"])]
    out, seen = [], set()
    for e in survivors:
        e = REWRITE.get(e["id"], e)
        if e["id"] in seen:
            continue
        seen.add(e["id"])
        if e["id"] in REPARENT:
            e["partOf"] = REPARENT[e["id"]]
        if e["id"] in DERIVED_FROM:
            e["derivedFrom"] = DERIVED_FROM[e["id"]]
        out.append(e)
    for eid, spec in REWRITE.items():
        if eid not in seen:
            out.append(spec); seen.add(eid)

    # 2. axial restructure
    out = [e for e in out if e["id"] not in {a["id"] for a in AXIAL}]
    seen -= {a["id"] for a in AXIAL}
    out.extend(AXIAL)
    for a in AXIAL:
        seen.add(a["id"])
    for pid, label, parent in PARTS:
        e = next((x for x in out if x["id"] == pid), None)
        if e:
            e["partOf"] = parent
            e["label"] = label

    skel["elements"] = out

    # 3. rewrite every attachment reference
    rewrites = 0
    docs = {}
    for path in sorted(ROOT.glob("data/muscles-*.json")):
        doc = json.loads(path.read_text())
        docs[path] = doc
        for m in doc["muscles"]:
            for holder in [m] + list(m.get("occurrences", [])):
                att = holder.get("attachments") or {}
                for side in ("origin", "insertion"):
                    for row in att.get(side, []):
                        for key in ("element", "landmark"):
                            v = row.get(key)
                            if v in MERGE and MERGE[v] != v:
                                row[key] = MERGE[v]; rewrites += 1
                        # A row whose landmark now equals its element is redundant.
                        if row.get("landmark") == row.get("element"):
                            row.pop("landmark")

    ids = {e["id"] for e in out}
    dangling = sorted({p for e in out for p in [e.get("partOf"), e.get("derivedFrom")]
                       if p and p not in ids})

    print(f"elements: {len(skel['elements'])} (merged {len([k for k,v in MERGE.items() if k!=v])} away)")
    print(f"attachment references rewritten: {rewrites}")
    print(f"elements carrying taxonNames: {sum(1 for e in out if e.get('taxonNames'))}")
    if dangling:
        print(f"DANGLING parents: {dangling}")
        return 1

    if not write:
        print("\nDry run. Re-run with --write to apply.")
        return 0

    skel_path.write_text(json.dumps(skel, indent=2, ensure_ascii=False) + "\n")
    for path, doc in docs.items():
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"rewrote skeleton.json and {len(docs)} muscle files")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
