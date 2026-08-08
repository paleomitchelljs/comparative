#!/usr/bin/env python3
"""One-shot migration: free-string `attachments` -> skeleton.json element ids.

The old `attachments` field held free strings at muscle level, which could not
express the thing that actually matters — that a muscle's attachment CHANGES
between taxa. This rewrites them as controlled ids and records provenance.

    python3 scripts/migrate_attachments.py           # report
    python3 scripts/migrate_attachments.py --write   # apply

After migration, `attachments` looks like:

    "attachments": {
      "origin":    ["scapula", "suprascapula"],
      "insertion": ["humerus"]
    }

with every string an id in data/skeleton.json. Taxon-specific divergence lives
on the occurrence rows (see scripts/derive_occurrence_attachments.py), so the
muscle-level list is explicitly the CONSENSUS, not a claim about any one taxon.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Old free string -> skeleton.json id. Where the old term was coarser than the
# ontology (e.g. "cranium"), it maps to the group element, not to a guess.
MAP = {
    "pectoral girdle": "pectoral-girdle", "pelvic girdle": "pelvic-girdle",
    "scapula": "scapula", "suprascapula": "suprascapula", "coracoid": "coracoid",
    "procoracoid": "procoracoid", "cleithrum": "cleithrum", "clavicle": "clavicle",
    "interclavicle": "interclavicle", "acromion": "acromion", "sternum": "sternum",
    "sternal keel": "sternal-keel", "humerus": "humerus", "radius": "radius",
    "ulna": "ulna", "ulnare": "ulnare", "carpals": "carpals", "pisiform": "pisiform",
    "metacarpals": "metacarpals", "phalanges": "phalanges-manus",
    "sesamoids": "sesamoids-manus", "femur": "femur", "tibia": "tibia",
    "fibula": "fibula", "tarsals": "tarsals", "calcaneum": "calcaneum",
    "metatarsals": "metatarsals", "patella": "patella", "ilium": "ilium",
    "ischium": "ischium", "pubis": "pubis", "obturator membrane": "obturator-membrane",
    "iliotibial tract": "iliotibial-tract", "fin radials": "fin-radials",
    "fin rays": "fin-rays", "axial skeleton": "axial-skeleton",
    "caudal vertebrae": "caudal-vertebrae", "lumbar vertebrae": "lumbar-vertebrae",
    "thoracic neural spines": "thoracic-neural-spines",
    "cervical transverse processes": "cervical-transverse-processes",
    "atlas transverse process": "atlas-transverse-process", "sacrum": "sacrum",
    "ribs": "ribs", "ventral ribs": "ribs", "body wall": "body-wall",
    "interosseous membrane": "interosseous-membrane",
    "palmar aponeurosis": "palmar-aponeurosis", "plantar aponeurosis": "plantar-aponeurosis",
    "flexor retinaculum": "flexor-retinaculum", "flexor tendons": "flexor-tendons",
    "extensor expansion": "extensor-expansion",
    "thoracolumbar fascia": "thoracolumbar-fascia", "nuchal ligament": "nuchal-ligament",
    "cervical fascia": "cervical-fascia", "occiput": "occiput",
    "cranium": "neurocranium", "neurocranium": "neurocranium",
    "otic capsule": "otic-capsule", "operculum": "operculum",
    "pyramidal eminence": "pyramidal-eminence", "temporal fossa": "temporal-fossa",
    "squamosal": "squamosal", "zygomatic arch": "zygomatic-arch",
    "pterygoid": "pterygoid", "quadrate": "quadrate", "palatoquadrate": "palatoquadrate",
    "mandible": "mandible", "coronoid process": "coronoid-process-mandible",
    "retroarticular process": "retroarticular-process",
    "Meckel's cartilage": "meckels-cartilage", "hyomandibula": "hyomandibula",
    "stapes": "stapes", "hyoid": "hyoid", "ceratohyal": "ceratohyal",
    "styloid process": "styloid-process", "branchial arches": "branchial-arches",
    "thyroid cartilage": "thyroid-cartilage", "cricoid cartilage": "cricoid-cartilage",
    "arytenoid cartilage": "arytenoid-cartilage", "spiracle": "spiracle",
    "orbit": "orbit", "optic foramen": "optic-foramen",
    "interorbital septum": "interorbital-septum", "sclera": "sclera",
    "eyelid": "eyelid", "tongue": "tongue", "skin": "skin",
    "midline raphe": "midline-raphe", "pharyngeal raphe": "pharyngeal-raphe",
    "propatagium": "propatagium",
}


def main(write: bool) -> int:
    skel = json.loads((ROOT / "data/skeleton.json").read_text())
    valid = {e["id"] for e in skel["elements"]}

    bad_targets = {v for v in MAP.values() if v not in valid}
    if bad_targets:
        sys.exit(f"MAP targets missing from skeleton.json: {sorted(bad_targets)}")

    unmapped, changed = set(), 0
    docs = {}
    for path in sorted(ROOT.glob("data/muscles-*.json")):
        doc = json.loads(path.read_text())
        docs[path] = doc
        for m in doc["muscles"]:
            att = m.get("attachments")
            if not att:
                continue
            for side in ("origin", "insertion"):
                out = []
                for term in att.get(side, []):
                    if isinstance(term, dict):  # already structured into rows
                        out.append(term)
                        continue
                    if term in valid:          # already an id
                        out.append(term)
                    elif term in MAP:
                        out.append(MAP[term]); changed += 1
                    else:
                        unmapped.add(term); out.append(term)
                if side in att:
                    att[side] = out

    if unmapped:
        print("UNMAPPED terms (add to MAP or skeleton.json):")
        for t in sorted(unmapped):
            print(f"  {t!r}")
        return 1

    print(f"{changed} attachment references mapped to skeleton ids")

    if not write:
        print("\nDry run. Re-run with --write to apply.")
        return 0

    for path, doc in docs.items():
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"rewrote {len(docs)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
